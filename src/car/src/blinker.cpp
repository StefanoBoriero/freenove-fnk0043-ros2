#include <rclcpp/rclcpp.hpp>
#include <rclcpp/executors.hpp>

#include <pigpiod_if2.h>

class MyNode: public rclcpp::Node
{
public:
    MyNode(): Node("cpp_test")
    {

        pi = PigpioSetup();

        if (pi >= 0) {
            RCLCPP_INFO(this->get_logger(),"Deamon interface started ok at %d", pi);
        } else {
            RCLCPP_ERROR(this->get_logger(),"Failed to init GPIO0");
        }
        RCLCPP_INFO(this->get_logger(), "Hello in cpp");
        counter_ = 0;
        timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&MyNode::timer_callback, this));
    }
private:
    const int LED = 16;
    int pi = -1;
    void timer_callback()
    {
        counter_++;
        if (counter_ % 2 == 0) {
            RCLCPP_INFO(this->get_logger(), "Turning led ON..");
            gpio_write(pi, LED, 1);
        } else {
            RCLCPP_INFO(this->get_logger(), "Turning led OFF..");
            gpio_write(pi, LED, 0);
        }
    }

    
    int PigpioSetup() {
        char *addStr = NULL;
        char *portStr = NULL;

        int pi = pigpio_start(addStr, portStr);

        set_mode(pi, LED, PI_OUTPUT);

        gpio_write(pi, LED, 0);

        return pi;
    }
    rclcpp::TimerBase::SharedPtr timer_;
    int counter_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
