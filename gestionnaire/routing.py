from django.urls import re_path
from channels.routing import ProtocolTypeRouter 


from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/frame/(?P<frame_id>\w+)/$', consumers.FrameConsumer_sync),
]