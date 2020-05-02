import json
from channels.generic.websocket import WebsocketConsumer

class FrameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': 10
        }))
	# def receive(self, data):
		# data_json=json.loads(data)
		# j1_add=data_json['j1_add']
		# j2_add=data_json['j2_add']
		