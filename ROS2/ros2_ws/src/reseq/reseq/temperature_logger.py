import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from datetime import datetime


class TemperatureLogger(Node):
    def __init__(self, filename: str):
        super().__init__('temperature_logger')

        self.log_file = open(filename, 'a', encoding='utf-8')

        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.callback,
            10
        )

    def callback(self, temperature: Float32):
        value = temperature.data

        if value >= 50.0:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f'[{timestamp}] Temperature: {value:.2f} °C'

            self.get_logger().info(message)
            self.log_file.write(message + '\n')
            self.log_file.flush()

    def destroy_node(self):
        self.log_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    logger = TemperatureLogger('log.txt')

    try:
        rclpy.spin(logger)
    except KeyboardInterrupt:
        pass
    finally:
        logger.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
