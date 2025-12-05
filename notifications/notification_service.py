class NotificationService:
    @staticmethod
    def send_notification(user, order_data, message):
        # Simulate sending a notification
        detailed_message = (
            f"{message}\n"
            f"Shipping Address: {order_data.shipping_address}\n"
            f"Product: {order_data.product}\n"
            f"Total Amount: ${order_data.total_amount:.2f}\n"
            f"Status: {order_data.status}\n"
            f"Created At: {order_data.created_at}"
        )
        print(f"Sending notification to User {user}:\n{detailed_message}")

    @staticmethod
    def send_pulsar_notification(message):
        # Simulate sending a notification
        detailed_message = (
            f"{message}"
        )
        print(f"Sending Pulsar notification to Slack:\n{detailed_message}")

