from channels.generic.websocket import WebsocketConsumer

class InferenceConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)

    def send_message(self, message_type, message):
        self.send(text_data=json.dumps({
            'message_type': message_type,
            'message': message
        }))