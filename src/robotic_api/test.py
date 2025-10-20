import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow ,QGraphicsDropShadowEffect,QDialog
from PySide6.QtGui import QColor
import json
from ui_mainwindow import Ui_MainWindow
# from ui_3dpop import Ui_MainWindow as Ui_3dpopup
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import cv2
import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import requests
import fonts_rc
import image_rc


from popup_viewer import PopupViewer


#with open("data.json", "r") as f :
#    data = json.load(f)

# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.abspath(relative_path)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.replace_label()
        self.setWindowTitle("Empty Qt Python App")
        self.ui.pushButton_manual.clicked.connect(self.on_button_manual_clicked)
        self.ui.pushButton_auto.clicked.connect(self.on_button_auto_clicked)
        self.ui.pushButton_3dpop.clicked.connect(self.on_button_3dpop_clicked)
        self.ui.pushButton_Shoot.clicked.connect(self.on_button_shoot_clicked)
        self.ui.pushButton_connect.clicked.connect(self.on_pushButton_connect_clicked)
        self.ui.pushButton_disconnect.clicked.connect(self.on_pushButton_disconnect_clicked)
        self.ui.pushButton_Run.clicked.connect(self.on_pushbutton_run_clicked)

        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(2.67, 2.67)
        shadow.setBlurRadius(3.33)
        shadow.setColor(QColor(255, 255, 255, int(255 * 0.2)))
        self.ui.pushButton_connect.setGraphicsEffect(shadow)
        self.manual = 0
        self.auto = 0

        self.ui.pushButton_connect.setIcon(QIcon(":/image/ui_image/connect.png"))
        self.ui.pushButton_connect.setIconSize(QSize(35, 35))
        self.ui.pushButton_disconnect.setIcon(QIcon(":/image/ui_image/disconnect.png"))
        self.ui.pushButton_disconnect.setIconSize(QSize(28, 28))


        self.ui.pushButton_Shoot.setIcon(QIcon(":/image/ui_image/tesseravue.png"))
        self.ui.pushButton_Shoot.setIconSize(QSize(100, 100))
        self.ui.pushButton_Shoot.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.ui.pushButton_Shoot.setStyleSheet("""
        QToolButton {
            background-color:#4c4d53;
            border-radius: 7px;
            padding-top: 20px;
            padding-bottom: 20px;
            color : white;
        }
        """)

        self.ui.pushButton_Run.setIcon(QIcon(":/image/ui_image/robot_arm.png"))
        self.ui.pushButton_Run.setIconSize(QSize(100, 100))
        self.ui.pushButton_Run.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.ui.pushButton_Run.setStyleSheet("""
        QToolButton {
            background-color:#4c4d53;
            border-radius: 7px;
            padding-top: 20px;
            padding-bottom: 20px;
            color : white;
        }
        """)



        self.image = np.zeros((1554, 2048, 3), dtype=np.uint8)
        self.boxes_image = self.image.copy()
        self.ui.pushButton_disconnect.setStyleSheet("""
            QPushButton {
                background-Color: #4c4d53;
                border-radius: 30px;
                color : white;
            }
            QPushButton:hover {
                background-color: #9da0aa;
            }
        """)
        self.ui.pushButton_connect.setStyleSheet("""
            QPushButton {
                background-Color: #4c4d53;
                border-radius: 30px;
                color : white;
            }
            QPushButton:hover {
                background-color: #9da0aa;
            }
        """)

    def on_button_manual_clicked(self) :
        self.manual = 1
        self.auto = 0
        self.ui.pushButton_manual.setStyleSheet("""
                QPushButton {
                    border-image: url(":/image/ui_image/menual_select.png");
                    color : #2f3033;

                }

            """)
        self.ui.pushButton_auto.setStyleSheet("""
                QPushButton {
                    border-image: url(":/image/ui_image/auto_deselect.png");
                    color : white;

                }

            """)



        self.ui.label_image.setScaledContents(True)
        self.ui.pushButton_auto.setEnabled(True)
        self.ui.pushButton_manual.setEnabled(False)


    def on_button_auto_clicked(self) :
        self.manual = 0
        self.auto = 1

        self.ui.pushButton_manual.setStyleSheet("""
                QPushButton {
                    border-image: url(":/image/ui_image/menual_deselect.png");
                    color : white;
                }

            """)
        self.ui.pushButton_auto.setStyleSheet("""
                QPushButton {
                    border-image: url(":/image/ui_image/auto_select.png");
                    color : #2f3033;;
                }
            """)


        self.ui.label_image.setScaledContents(True)
        self.ui.pushButton_auto.setEnabled(False)
        self.ui.pushButton_manual.setEnabled(True)


    def on_button_shoot_clicked(self) :
        self.bbox_list = [[]]
        resp = requests.get("http://localhost:5000/capture")
        resp.raise_for_status()
        data_prefix = resp.json()

        self.ui.label_points.setText("")
        #self.image = cv2.imread("gui_app/data/"+data_prefix["prefix"]+".png")
        self.image = cv2.imread("image_25.bmp")
        self.pcd_path = "gui_app/data/"+data_prefix["prefix"]+".pcd"

        #image를 제대로 읽지 못했을 경우
        if self.image is None:
            print("❌ 이미지 읽기 실패. 검정 화면으로 대체합니다.")
            self.image = np.zeros((1554, 2048, 3), dtype=np.uint8)

        h,w, c = self.image.shape
        print(w, h, c)
        cp_image = self.image.copy()


        resp2 = requests.get("http://localhost:5000/detect")
        resp2.raise_for_status()
        self.data_detect = resp2.json()

        points_text = "전체 포인터에 대한 데이터\n\n"

        if len(self.data_detect["objects"]) > 0 :
            for i in range(len(self.data_detect["objects"])) :
                btR = self.data_detect["objects"][i]["bounding_box"]["bottom_right"]
                topL = self.data_detect["objects"][i]["bounding_box"]["top_left"]

                x = np.round(self.data_detect["objects"][i]["center_point"]["x"],2)
                y = np.round(self.data_detect["objects"][i]["center_point"]["y"],2)
                z = np.round(self.data_detect["objects"][i]["center_point"]["z"],2)
                p = int(self.data_detect["objects"][i]["ICP"]["euler_angles"]["pitch"])
                r = int(self.data_detect["objects"][i]["ICP"]["euler_angles"]["roll"])
                yaw = int(self.data_detect["objects"][i]["ICP"]["euler_angles"]["yaw"])
                id = self.data_detect["objects"][i]["id"]

                points_text+=f"Point{id} : [{x}, {y}, {z}, {p}, {r}, {yaw}]\n"
                cp_image = cv2.rectangle(cp_image, topL, btR, (255,255,255), 3)
                print

            qimg = QImage(cp_image.data, w, h, w*c, QImage.Format_BGR888)
            self.boxes_image = cp_image
        else :
            self.boxes_image = self.image.copy()
            qimg = QImage(self.image.data, w, h, w*c, QImage.Format_BGR888)
            self.ui.label_select_pt.setText("No Detect")
        self.ui.label_image.setPixmap(QPixmap(qimg))
        self.ui.label_image.setScaledContents(True)

        self.ui.label_points.setText(points_text)


    def on_button_3dpop_clicked(self) :
        
        self.viewer_popup = PopupViewer(self.pcd_path)
        self.viewer_popup.show()  # 팝업창 띄우기

    def on_pushButton_connect_clicked(self) :
        self.ui.pushButton_connect.setStyleSheet("""
            QPushButton {
                background-Color: #732a34;
                border-radius: 30px;
                color : white;
            }
            QPushButton:hover {
                background-color: #aa6571;
            }
        """)

    def on_pushButton_disconnect_clicked(self) :
        self.ui.pushButton_connect.setStyleSheet("""
            QPushButton {
                background-Color: #4c4d53;
                border-radius: 30px;
                color : white;
            }
            QPushButton:hover {
                background-color: #9da0aa;
            }
        """)



    def on_label_clicked(self, event):  # QLabel에 mousePressEvent 재정의 필요
        label_width = self.ui.label_image.width()
        label_height = self.ui.label_image.height()
        # self.image = cv2.imread("image_25.bmp")
        image_width = self.image.shape[1]  # 2048
        image_height = self.image.shape[0]  # 1554

        # 마우스 클릭 위치 (QMouseEvent)
        pos = event.position()
        x_label = event.pos().x()
        y_label = event.pos().y()

        # 비례 변환
        scale_x = image_width / label_width
        scale_y = image_height / label_height

        x_image = int(x_label * scale_x)
        y_image = int(y_label * scale_y)

        print(f"이미지 내 좌표: ({x_image}, {y_image})")


        self.boxes_image_copy = self.boxes_image.copy()
        h,w,c = self.boxes_image_copy.shape


        for i in range(len(self.data_detect["objects"])):
            btR = self.data_detect["objects"][i]["bounding_box"]["bottom_right"]
            topL = self.data_detect["objects"][i]["bounding_box"]["top_left"]
            if (topL[0]<x_image<btR[0] and topL[1]<y_image<btR[1]):
                #선택된 id
                self.select_points_id = self.data_detect["objects"][i]["id"]
                #새로운 이미지

                self.select_boxes_image = cv2.rectangle(self.boxes_image_copy, topL, btR, (255,0,0), 3)


                label_text = f"ID: {self.select_points_id}"

                text_position = (btR[0] - 80, topL[1] - 10)

                cv2.putText(self.boxes_image_copy, label_text, text_position,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=(255, 0, 0),
                            thickness=2)



                self.qimg = QImage(self.select_boxes_image.data, w, h, w*c, QImage.Format_BGR888)
                self.ui.label_image.setPixmap(QPixmap(self.qimg))
                self.ui.label_image.setScaledContents(True)



                #선택된 데이터 x,y,z,p,r,yaw
                x = np.round(self.data_detect["objects"][i]["center_point"]["x"],2)
                y = np.round(self.data_detect["objects"][i]["center_point"]["y"],2)
                z = np.round(self.data_detect["objects"][i]["center_point"]["z"],2)
                p = int(self.data_detect["objects"][i]["ICP"]["euler_angles"]["pitch"])
                r = int(self.data_detect["objects"][i]["ICP"]["euler_angles"]["roll"])
                yaw = int(self.data_detect["objects"][i]["ICP"]["euler_angles"]["yaw"])


                self.ui.label_select_pt.setText(f"Selected Point : [{x}, {y}, {z}, {p}, {r}, {yaw}]")
                self.target_points = {
                    "target_point":[self.data_detect["objects"][i]["center_point"]["x"],
                                    self.data_detect["objects"][i]["center_point"]["y"],
                                    self.data_detect["objects"][i]["center_point"]["z"]]
                                    }




                print(f"선택된 id : {self.select_points_id}")
                break
            else:

                #다른점을 클릭 했을경우 원래 이미지로 돌아가기
                self.qimg = QImage(self.boxes_image_copy.data, w, h, w*c, QImage.Format_BGR888)
                self.ui.label_image.setPixmap(QPixmap(self.qimg))
                self.ui.label_image.setScaledContents(True)
                self.ui.label_select_pt.setText("선택된 포인트 데이터 : no point")
                print("선택된 포인트 데이터 : no point")

    def on_pushbutton_run_clicked(self) :
        if self.manual == 1 and self.auto == 0 :
            print(self.target_points)
            self.mode_init()
        elif self.manual == 0 and self.auto == 1 :
            print("auto")
            self.mode_init()
        else :
            print("Not select")

    def mode_init(self) :
        self.maunal = 0
        self. auto = 0
        self.ui.pushButton_auto.setStyleSheet("""
                QPushButton {
                    border-image: url(":/image/ui_image/auto_deselect.png");
                    color : white;

                }

            """)

        self.ui.pushButton_manual.setStyleSheet("""
                QPushButton {
                    border-image: url(":/image/ui_image/menual_deselect.png");
                    color : white;
                }

            """)







    def replace_label(self) :
        self.old_label = self.ui.label_image
        self.clickable = ClickableLabel(self)
        self.clickable.setObjectName("label_image")
        self.clickable.setScaledContents(True)
        self.clickable.setFixedSize(self.old_label.size())
        self.clickable.setSizePolicy(self.old_label.sizePolicy())
        self.clickable.setMinimumSize(self.old_label.minimumSize())
        self.clickable.setMaximumSize(self.old_label.maximumSize())
        self.clickable.setStyleSheet("""background-color: #393a3e;border-radius: 7px;""")

        self.layout = self.ui.main_layout.layout()
        self.layout.replaceWidget(self.old_label, self.clickable)
        self.old_label.deleteLater()

        self.ui.label_image = self.clickable
        self.ui.label_image.clicked.connect(self.on_label_clicked)

class ClickableLabel(QLabel):
    clicked = Signal(QMouseEvent)

    def mousePressEvent(self, event):
        self.clicked.emit(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont(":/fonts/fonts/NotoSansKR-Medium.ttf")
    font_family = QFontDatabase.applicationFontFamilies(font_id)
    app.setFont(QFont(font_family, 10))

    window = MainApp()
    window.show()
    sys.exit(app.exec())



    # class PopupWindow(QMainWindow) :
    #     def __init__(self):
    #         super().__init__()
    #         self.bbox_list = [[]]
    #         self.ui = Ui_3dpopup()
    #         self.ui.setupUi(self)
    #         self.setWindowTitle("3D 팝업")


    #     def run_viewer(self,pcd_file):
    #         gui.Application.instance.initialize()

    #         window = gui.Application.instance.create_window("3D Viewer")
    #         scene_widget = gui.SceneWidget()
    #         scene_widget.scene = rendering.Open3DScene(window.renderer)

    #         pcd = o3d.io.read_point_cloud(pcd_file)
    #         points = np.asarray(pcd.points)
    #         colors = np.asarray(pcd.colors)
    #         mask = ((points[:,0] <1000) & (points[:,1] <1000) & (points[:,2] <1000))
    #         pcd_points_filter = points[mask]
    #         pcd_colors_filter = colors[mask]
    #         pcd_filter = o3d.geometry.PointCloud()
    #         pcd_filter.points = o3d.utility.Vector3dVector(pcd_points_filter)
    #         pcd_filter.colors = o3d.utility.Vector3dVector(pcd_colors_filter)
    #         mat = rendering.MaterialRecord()
    #         mat.shader = "defaultUnlit"

    #         scene_widget.scene.add_geometry("pcd", pcd_filter, mat)
    #         scene_widget.setup_camera(60.0, pcd_filter.get_axis_aligned_bounding_box(), [0,0,0])
    #         print(pcd_filter.get_axis_aligned_bounding_box())
    #         window.add_child(scene_widget)
    #         gui.Application.instance.run()
