import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Messages
from accounts.models import User

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.count = 0
        return super().__init__(*args, **kwargs)

    def fetch_old_messages(self, data):
        messages = Messages.last_10_messages(times=self.count)
        if messages:
            self.count += 1
        else:
            self.count -= 1
            messages = Messages.last_10_messages(times=self.count)

        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def fetch_messages(self, data):
        self.count = 0
        messages = Messages.last_10_messages(self.count)
        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        author = data["from"]
        parent_user = User.objects.get(username=author)
        message = Messages.objects.create(
            parent_user=parent_user,
            message_text=data["message"],
        )
        content = {"command": "new_message", "message": self.message_to_json(message)}
        return self.send_chat_message(content)

    commands = {
        "fetch_old_messages": fetch_old_messages,
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.parent_user.first_name,
            "author_profile_img": message.parent_user.profile_photo.image.url,
            "content": message.message_text,
            "timestamp": str(message.date_posted),
        }

    def connect(self):
        self.room_name = 'room'
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))