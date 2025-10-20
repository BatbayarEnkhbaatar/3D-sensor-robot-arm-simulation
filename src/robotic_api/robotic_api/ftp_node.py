import os
import ftplib
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ament_index_python.packages import get_package_share_directory
from robotic_msgs.action import TesseraVueTasks
# from robot import controlRobot


class FTPClientNode(Node):
    def __init__(self):

        
        super().__init__('ftp_client_node')
        # Action Client Setup
        self._action_client = ActionClient(self, TesseraVueTasks, "TesseraVueTasks")
        # self._action_client.wait_for_server()

        self.get_logger().info("TesseraVue Action Server is Ready...")
        
        # FTP server details
        self.ftp_server = '10.10.10.96'
        self.ftp_username = 'haanvision'
        self.ftp_password = 'haanvision'
        self.ftp_directory = '/'  # Directory on the FTP server
        self.latest_pcd = None
        self.latest_bmp = None
        self.new_pcd = None
        self.new_bmp = None


        # Get the package's shared directory
        package_name = 'robotic_api'
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'data/')  # Shared directory in your package

        # Create the local directory if it doesn't exist
        os.makedirs(self.local_directory, exist_ok=True)

        # FTP connection handle
        self.ftp = None

        # Initialize the FTP connection and timer
        # self.connect_to_ftp()

        self.timer = self.create_timer(1.0, self.check_ftp_server)


    def check_ftp_server(self):

        """Check for new files on the FTP server and download them."""
       
        
        if self.ftp is None:
            self.connect_to_ftp()
            return

        try:
                # List files in the FTP directory
            file_list = self.ftp.nlst()  # Get the list of files in the current FTP directory
            for filename in file_list:
                local_file = os.path.join(self.local_directory, filename)
                # Download the file if it doesn't exist locally
                
                if not os.path.exists(local_file):
                    # self.download_file(filename, local_file)
                    # Ensure the file is stable before downloading
                    attempt =0
                    if not self.is_file_stable(filename):
                        self.get_logger().warn(f"File {filename} is not stable. Retrying...")
                        time.sleep(2)
                        continue
                    with open(local_file, 'wb') as f:
                        self.get_logger().info(f"Downloading file {filename} (attempt {attempt + 1})...")
                        self.ftp.retrbinary(f"RETR {filename}", f.write)
                        self.get_logger().info(f"Downloaded {filename} to {local_file}")
                # Store latest .pcd and .bmp file paths
                    if filename.endswith('.pcd'):
                        self.latest_pcd = local_file
                        self.new_pcd = True
                        self.get_logger().info(f"waiting for file: .BMP")
                    elif filename.endswith('.bmp'):
                        self.latest_bmp = local_file
                        self.new_bmp = True
                        self.get_logger().info(f"waiting for file: .PCD")
                    if(self.new_pcd==True and self.new_bmp==True):
                        self.get_logger().info("Both files received. Sending action goal...")
                        self._send_action_goal([self.latest_pcd, self.latest_bmp])
                        self.new_pcd = False
                        self.new_bmp = False
                        self.latest_pcd = None
                        self.latest_bmp = None
                        return
            
        except Exception as e:
            self.get_logger().error(f"Failed to retrieve file list: {str(e)}")

    def connect_to_ftp(self):
        """Establish an FTP connection."""
        try:
            self.ftp = ftplib.FTP(self.ftp_server)
            self.ftp.login(self.ftp_username, self.ftp_password)
            self.get_logger().info('Successfully connected to the FTP server.')
            self.ftp.cwd(self.ftp_directory)
        except Exception as e:
            self.get_logger().error(f"Failed to connect to FTP server: {str(e)}")
            self.ftp = None

    def is_file_stable(self, filename):
        """Check if a file's size remains stable over a short period."""
        try:
            size1 = self.ftp.size(filename)
            time.sleep(0.5)  # Wait for half a second
            size2 = self.ftp.size(filename)
            return size1 == size2
        except Exception as e:
            self.get_logger().error(f"Failed to check size for {filename}: {str(e)}")
            return False

    def download_file(self, filename, local_file):
        """Download a file from the FTP server with retries."""
        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                # Ensure the file is stable before downloading
                if not self.is_file_stable(filename):
                    self.get_logger().warn(f"File {filename} is not stable. Retrying...")
                    time.sleep(2)
                    continue
                with open(local_file, 'wb') as f:
                    self.get_logger().info(f"Downloading file {filename} (attempt {attempt + 1})...")
                    self.ftp.retrbinary(f"RETR {filename}", f.write)
                    downloaded  = True
                    self.get_logger().info(f"Downloaded {filename} to {local_file}")
                return  
            except Exception as e:
                self.get_logger().error(f"Attempt {attempt + 1} failed to download {filename}: {str(e)}")
                time.sleep(1) 

        return downloaded

    def _send_action_goal(self, goal):
        """Send the action goal to the server."""
        self.get_logger().info("Sending goal to the action server...")
        # self.runRobot()
        goal_msg = TesseraVueTasks.Goal()
        goal_msg.lastshots = goal
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        self.get_logger().info(str(goal))
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().info('File Transaction rejected :(')
                return

            self.get_logger().info('File Transaction accepted :)')
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.get_result_callback)
        except Exception as e:
            self.get_logger().error(f"File Transaction response callback failed: {str(e)}")

    def get_result_callback(self, future):
        try:
            result = future.result().result
            self.get_logger().info(f'File Transaction : {result.ftpsuccess}')
        except Exception as e:
            self.get_logger().error(f"File transaction callback failed: {str(e)}")

    def __del__(self):
        """Ensure the FTP connection is closed when the node is destroyed."""
        if self.ftp:
            self.ftp.quit()


def main(args=None):
    rclpy.init(args=args)
    node = FTPClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
    # controlRobot.main()
