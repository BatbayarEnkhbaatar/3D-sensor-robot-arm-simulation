#include <rclcpp/rclcpp.hpp>
#include <memory>
#include <iostream>
#include <cstring>
#include <spdlog/spdlog.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define HOST_IP "192.168.0.10"
#define PORT_NUM 1024

class BinpickingClient : public rclcpp::Node {
public:
    BinpickingClient() : Node("binpicking_client"), tcp_sock(-1) {
        spdlog::info("Attempting to connect to 3D Sensor[{}:{}]", HOST_IP, PORT_NUM);

        tcp_sock = socket(AF_INET, SOCK_STREAM, 0);
        if (tcp_sock < 0) {
            spdlog::error("Failed to create socket");
            return;
        }

        struct sockaddr_in server_addr;
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(PORT_NUM);
        inet_pton(AF_INET, HOST_IP, &server_addr.sin_addr);

        if (connect(tcp_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            spdlog::error("Connection failed");
            close(tcp_sock);
            return;
        }

        spdlog::info("Connection successful");
        connection = true;
    }

    ~BinpickingClient() {
        if (tcp_sock >= 0) {
            close(tcp_sock);
        }
    }

private:
    bool connection;
    int tcp_sock;
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<BinpickingClient>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
