#!/usr/bin/env python3
"""
Haanvision Bin‑Picking TCP client – pipeline‑accurate   (2025‑04)

• Full 3‑axis 3D point cloud + PCD writer
• Proper context‑manager support (with … as cli:)
"""

from __future__ import annotations
import argparse, enum, logging, selectors, socket, struct, time
from pathlib import Path
from typing import List, Tuple

import lz4.block
import numpy as np
from PIL import Image
import datetime
_LOG = logging.getLogger("binpicking")


# ──────────────────────────── low‑level I/O ────────────────────────────
def _read_exact(sock: socket.socket, length: int, timeout: float) -> bytes:
    sel = selectors.DefaultSelector()
    sel.register(sock, selectors.EVENT_READ)
    buf = bytearray()
    start = time.perf_counter()
    while len(buf) < length:
        if timeout and (time.perf_counter() - start) > timeout:
            raise TimeoutError("read timeout")
        if not sel.select(timeout=max(0, timeout - (time.perf_counter() - start))):
            continue
        chunk = sock.recv(length - len(buf))
        if not chunk:
            raise ConnectionError("connection closed by peer")
        buf.extend(chunk)
    return bytes(buf)


def _send_all(sock: socket.socket, data: bytes, timeout: float) -> None:
    sel = selectors.DefaultSelector()
    sel.register(sock, selectors.EVENT_WRITE)
    view = memoryview(data)
    start = time.perf_counter()
    while view:
        if timeout and (time.perf_counter() - start) > timeout:
            raise TimeoutError("write timeout")
        if not sel.select(timeout=max(0, timeout - (time.perf_counter() - start))):
            continue
        sent = sock.send(view)
        view = view[sent:]


def _set_keepalive(sock: socket.socket) -> None:
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    except OSError:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, struct.pack("I", 1))


# ───────────────────────── commands enum ─────────────────────────
class CMD(str, enum.Enum):
    INIT            = "INIT"
    SETROI          = "SETROI"
    TRIGGER         = "TRIGGER"
    GRAB2D          = "GRAB2D_"           # + idx
    GETVERTEX_X     = "GETVERTEX_X"
    GETVERTEX_DEPTH = "GETVERTEX_DEPTH_TCP"
    CONFIG          = "CONFIG"
    HDR             = "HDR"
    SET_MODEL       = "SET_MODEL"


# ──────────────────────────── client ────────────────────────────
class BinpickingClient:
    DEFAULT_TIMEOUT = 5.0

    def __init__(self, ip: str, port: int = 1024, *, timeout: float = DEFAULT_TIMEOUT):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self._tcp: socket.socket | None = None
        self.channels: int | None = None
        self.width: int | None = None
        self.height: int | None = None

    # ── context manager ─────────────────────────────────────────
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ── connect / close ─────────────────────────────────────────
    def connect(self) -> None:
        if self._tcp and self._tcp.fileno() != -1:
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        try:
            sock.connect((self.ip, self.port))
        except BlockingIOError:
            pass
        sel = selectors.DefaultSelector()
        sel.register(sock, selectors.EVENT_WRITE)
        if not sel.select(self.timeout):
            raise TimeoutError("connect timeout")
        _set_keepalive(sock)
        self._tcp = sock
        _LOG.info("TCP connected → %s:%d", self.ip, self.port)

    def close(self) -> None:
        if not self._tcp:
            return
        try:
            _send_all(self._tcp, b"\x00", self.timeout)
            self._tcp.setsockopt(socket.SOL_SOCKET,
                                 socket.SO_LINGER,
                                 struct.pack("ii", 1, 0))
            self._tcp.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self._tcp.close()
        self._tcp = None
        _LOG.info("Disconnected")

    # ── framing ───────────────────────────────────────────────────
    def _write(self, payload: bytes) -> None:
        if not self._tcp:
            raise ConnectionError("not connected")
        if len(payload) > 255:
            raise ValueError("payload too long")
        _send_all(self._tcp, bytes([len(payload)]) + payload, self.timeout)

    def _read(self) -> bytes:
        if not self._tcp:
            raise ConnectionError("not connected")
        length = _read_exact(self._tcp, 1, self.timeout)[0]
        return _read_exact(self._tcp, length, self.timeout)

    def write_cmd(self, cmd: str | CMD, *params: str) -> None:
        text = cmd.value if isinstance(cmd, CMD) else cmd
        payload = text + ("," + ",".join(params) if params else "")
        self._write(payload.encode())

    def read_reply(self) -> str:
        return self._read().decode()

    # ── sensor API ──────────────────────────────────────────────
    def init(self) -> Tuple[int,int,int]:
        self.write_cmd(CMD.INIT)
        ch,w,h = map(int, self.read_reply().split(","))
        self.channels, self.width, self.height = ch, w, h
        self.set_roi(0,0,w,h)
        self.device_config(7,12,3)
        return ch,w,h

    def set_roi(self, x:int, y:int, w:int, h:int) -> None:
        self.write_cmd(CMD.SETROI)
        _ = self.read_reply()
        self._write(f"{x},{y},{w},{h}".encode())
        _ = self.read_reply()

    def trigger(self) -> Tuple[int,int]:
        self.write_cmd(CMD.TRIGGER)
        parts = list(map(int, self.read_reply().split(",")))
        return parts[0], parts[1] if len(parts)>1 else 0

    # def grab_2d(self, idx:int, *, save_png=True) -> bytes:
    #     assert self.width and self.height
    #     self.write_cmd(f"{CMD.GRAB2D.value}{idx}")
    #     length = struct.unpack("<I", _read_exact(self._tcp,4,self.timeout))[0]
    #     blob = _read_exact(self._tcp,length,self.timeout)
    #     img  = blob[-self.width*self.height:]
    #     if save_png:
    #         Image.frombytes("L",(self.width,self.height),img).save(f"cam{idx}.png")
    #         _LOG.info("saved cam%d.png",idx)
    #     return img

    def grab_2d(self, idx: int, *, save_png=True, save_path: Path | None = None) -> bytes:
        assert self.width and self.height
        self.write_cmd(f"{CMD.GRAB2D.value}{idx}")
        length = struct.unpack("<I", _read_exact(self._tcp, 4, self.timeout))[0]
        blob = _read_exact(self._tcp, length, self.timeout)
        img = blob[-self.width * self.height:]
        
        if save_png:
            if save_path is None:
                save_path = Path(f"cam{idx}.png")
            Image.frombytes("L", (self.width, self.height), img).save(save_path)
            _LOG.info("saved %s", save_path)
        
        return img


    # def grab_2d_all(self) -> List[bytes]:
    #     assert self.channels is not None
    #     return [self.grab_2d(i) for i in range(self.channels)]
    def grab_2d_all(self, save_dir,  prefix ) -> List[bytes]:
        assert self.channels is not None
        save_dir = Path(save_dir)
        save_path = ""
    #     return [
    #         self.grab_2d(
    #             i, 
    #             save_path=save_dir / f"{prefix}{i}.png"
    #         ) for i in range(self.channels)
    # ]
        imgs_path = []
        for i in range(self.channels):
            img_path = save_dir / f"{prefix}{i}.png"
            self.grab_2d(i, save_path=img_path)
            imgs_path.append(str(img_path))

        return imgs_path

    def get_pcd(self,
                *,
                save: bool = True,
                pcd_path: Path | None = None
               ) -> Tuple[List[float],List[float],List[float],List[int]]:
        assert self.width and self.height
        # Trigger a new 3D capture
        self.trigger()
        # Request the packed PCD via TCP
        self.write_cmd(CMD.GETVERTEX_X)
        hdr = _read_exact(self._tcp, 10, self.timeout)
        orig, comp = struct.unpack_from("<II", hdr, 2)
        blob = lz4.block.decompress(_read_exact(self._tcp, comp, self.timeout),
                                    uncompressed_size=orig)

        n = self.width * self.height
        ints = np.frombuffer(blob, dtype="<i4", count=n*3).astype(np.float32)

        X = ints[0:n]   * 1e-2   # metres
        Y = ints[n:2*n] * 1e-2
        Z = ints[2*n:]  * 1e-2
        depth = np.frombuffer(blob, dtype=np.uint8, count=n, offset=3*n*4)

        print(f"X range {X.min():.3f}→{X.max():.3f} m, "
        f"Y range {Y.min():.3f}→{Y.max():.3f} m, "
        f"Z range {Z.min():.3f}→{Z.max():.3f} m")

        if save:
            pcd_path = pcd_path or Path("frame.pcd")
            self._save_pcd(X, Y, Z, depth, pcd_path)
            _LOG.info("saved %s", pcd_path)

        return X.tolist(), Y.tolist(), Z.tolist(), depth

    # ── config handshakes ────────────────────────────────────────
    def _handshake(self, cmd:CMD, payload:str) -> None:
        self.write_cmd(cmd)
        _ = self.read_reply()
        self._write(payload.encode())
        _ = self.read_reply()

    def config(self, bright:int, exp_ms:int, proj_mA:int) -> None:
        self._handshake(CMD.CONFIG, f"{bright},{exp_ms},{proj_mA}")

    def hdr(self, enable:bool) -> None:
        self._handshake(CMD.HDR, "true" if enable else "false")

    def set_model(self, m:float, i:float, r:float) -> None:
        self._handshake(CMD.SET_MODEL, f"{m},{i},{r}")

    def device_config(self, bright:int, exp_ms:int, step:int) -> None:
        assert self.width
        proj = ((step+1)*25 if self.width==640 else (7-step)*30+60)
        exp  = max(10 if self.width==640 else 9,
                   min(exp_ms, 50 if self.width==640 else 20)) * 10
        if exp % 100 == 0:
            exp += 5
        bright = max(1, min(bright,10))
        self.config(bright, exp, proj)

    @staticmethod
    def _save_pcd(x: np.ndarray,
                  y: np.ndarray,
                  z: np.ndarray,
                  depth: List[int],
                  path: Path,
                  *,
                  scale: float = 1.0,
                  binary: bool = True
                 ) -> None:
        n = x.shape[0]
        header = (
            "# .PCD v0.7 - generated by Python client\n"
            "VERSION .7\n"
            "FIELDS x y z rgb\n"
            "SIZE 4 4 4 4\n"
            "TYPE F F F U\n"
            "COUNT 1 1 1 1\n"
            f"WIDTH {n}\n"
            "HEIGHT 1\n"
            "VIEWPOINT 0 0 0 1 0 0 0\n"
            f"POINTS {n}\n"
            f"DATA {'binary' if binary else 'ascii'}\n"
        )
        with path.open("wb") as fp:
            fp.write(header.encode())
            if binary:
                gray = np.array(depth, dtype=np.uint8).astype(np.uint32)
                rgbv = (gray<<16)|(gray<<8)|gray
                arr = np.empty(n, dtype=[('x','<f4'),('y','<f4'),('z','<f4'),('rgb','<u4')])
                arr['x'],arr['y'],arr['z'],arr['rgb'] = x*scale, y*scale, z*scale, rgbv
                arr.tofile(fp)
            else:
                for xi, yi, zi, di in zip(x, y, z, depth):
                    rgbv = (di<<16)|(di<<8)|di
                    fp.write(f"{xi:.6f} {yi:.6f} {zi:.6f} {rgbv}\n".encode())


# ─────────────────────────── CLI ────────────────────────────────
def _cli(ip, tcp, strPath):
    with BinpickingClient(ip, tcp) as cli:
        print("Commands: init | grab2d <idx>|all | trigger | pcd | depth | config | hdr | model | roi | quit")
        filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        # line = input("binpick> ").strip()
        ch, w, h = cli.init()
        print(f"channels={ch} size={w}x{h}")
        img_path = cli.grab_2d_all(strPath, filename) 
        print("all saved")
        s,m = cli.trigger()
        print(f"scan={s} ms model={m} ms")
        pcd_path=Path(str(strPath + "/"+ filename+".pcd"))
        x,y,z,d = cli.get_pcd(save=True, pcd_path=pcd_path)
        print(f"{len(x)} points → {filename}")
        x,y,z,d = cli.get_pcd(save=False)
        Image.frombytes("L",(cli.width,cli.height),bytes(d)).save(str(strPath+"/"+"depth_"+ filename+".png"))
        print(f"Depthm image saved : depth_{filename}")
        quit = "quit"
        cli.write_cmd(quit)
    return img_path[0], str(pcd_path)

# if __name__ == "__main__":
#     _cli(ip="192.168.0.10", tcp=1024, strPath= "/home/ubuntu/Documents/my_work_1/install/robotic_3dsensor/share/robotic_3dsensor/data")
