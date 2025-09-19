from abc import ABC, abstractmethod

# 1. The Abstract Base Class (The Contract)
class NotificationSender(ABC):
    """
    An abstract base class that defines the contract for all
    notification sending classes.
    """
    @abstractmethod
    def send(self, message: str):
        """
        Send a notification. All subclasses must implement this method.
        """
        pass


# 2. Concrete Implementation for Email
class EmailSender(NotificationSender):
    """A concrete class that sends notifications via email."""
    def send(self, message: str):
        """Implements the send method for email."""
        print(f"📧 Sending email: {message}")


# 3. Concrete Implementation for SMS
class SMSSender(NotificationSender):
    """A concrete class that sends notifications via SMS."""
    def send(self, message: str):
        """Implements the send method for SMS."""
        print(f"📱 Sending SMS: {message}")


# 4. Concrete Implementation for Push Notifications
class PushNotificationSender(NotificationSender):
    """A concrete class that sends notifications via push."""
    def send(self, message: str):
        """Implements the send method for push notifications."""
        print(f"🔔 Sending push notification: {message}")


# --- Testing ---
email_sender = EmailSender()
sms_sender = SMSSender()
push_sender = PushNotificationSender()

# A list of objects that all conform to the NotificationSender interface
senders = [email_sender, sms_sender, push_sender]
message_to_send = "Your order has been shipped!"

# This function can work with ANY NotificationSender object,
# even ones that might be created in the future.
def send_notification_to_all(sender_list, message):
    for sender in sender_list:
        sender.send(message)

send_notification_to_all(senders, message_to_send)

# What happens if you try to create an object from the ABC?
# Uncommenting the line below will raise a TypeError because you can't
# instantiate an abstract class with abstract methods.
# faulty_sender = NotificationSender()