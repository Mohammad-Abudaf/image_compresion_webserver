import eventlet
import socketio
from lib.imageprocessing import ImageProcessing
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'assets/index.html'},
    '/original.jpg': {'content_type': 'image/jpeg', 'filename': 'assets/opencv_frame_0.png'},
    '/result.jpg': {'content_type': 'image/jpeg', 'filename': 'assets/resultImg.jpg'},
    '/cv.jpg': {'content_type': 'image/jpeg', 'filename': 'cv.jpg'}
})


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


def main():
    ImageProcessing.cap_image()
    ImageProcessing.compress('assets/opencv_frame_0.png', 0.05)

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
