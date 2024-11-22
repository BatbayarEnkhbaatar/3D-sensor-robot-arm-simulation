import os
import ftplib
import rclpy
from rclpy.node import Node
from rclpy.timer import Timer
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory

class FTPClientNode(Node):
    def __init__(self):
        super().__init__('ftp_client_node')

        # FTP server details
        self.ftp_server = '192.168.0.100'
        self.ftp_username = '4division'
        self.ftp_password = 'ubuntu'
        self.ftp_directory = '/'  # Directory on the FTP server

        # Get the package's shared directory
        package_name = 'robotic_actions'
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'downloaded_files')  # Shared directory in your package

        # Create the local directory if it doesn't exist
        if not os.path.exists(self.local_directory):
            os.makedirs(self.local_directory)

        # Timer to check for new files every second
        self.timer = self.create_timer(1.0, self.check_ftp_server)

        # FTP connection handle
        self.ftp = None

        # Initialize the FTP connection
        self.connect_to_ftp()

    def connect_to_ftp(self):
        """Connect to the FTP server."""
        try:
            self.ftp = ftplib.FTP(self.ftp_server)
            self.ftp.login(self.ftp_username, self.ftp_password)
            self.get_logger().info('Successfully connected to the FTP server.')
            self.ftp.cwd(self.ftp_directory)
        except Exception as e:
            self.get_logger().error(f"Failed to connect to FTP server: {str(e)}")

    def check_ftp_server(self):
        """Check for new files on the FTP server and download them."""
        if self.ftp is None:
            self.get_logger().warn('FTP connection is not established.')
            return

        try:
            # List files in the FTP directory
            file_list = self.ftp.nlst()  # Get the list of files in the current FTP directory
            self.get_logger().info(f"Files available on the FTP server: {file_list}")

            for filename in file_list:
                local_file = os.path.join(self.local_directory, filename)
                if not os.path.exists(local_file):  # Download file if not already downloaded
                    self.download_file(filename, local_file)
                else:
                    self.get_logger().info(f"File {filename} already downloaded.")
        except Exception as e:
            self.get_logger().error(f"Failed to retrieve file list: {str(e)}")

    def download_file(self, filename, local_file):
        """Download a file from the FTP server."""
        try:
            with open(local_file, 'wb') as f:
                self.get_logger().info(f"Downloading file {filename}...")
                self.ftp.retrbinary(f"RETR {filename}", f.write)
                self.get_logger().info(f"Downloaded {filename} to {local_file}")
        except Exception as e:
            self.get_logger().error(f"Failed to download {filename}: {str(e)}")

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
