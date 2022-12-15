import socketio
import eventlet


class WebServer:
    server = socketio.Server()
    app = socketio.WSGIApp(server, static_files={
        '/': {'contact_type': 'text/html', 'filename': 'index.html'},
        'image': {'contact_type': '', 'filename': 'result.jpg'}
    })

    @server.event
    def connect(self, sid, environ):
        print('connect ', sid)

    @server.event
    def my_message(sid, data):
        print('message ', data)

    @server.event
    def disconnect(sid):
        print('disconnect ', sid)

    @staticmethod
    def run_webserver():
        eventlet.wsgi.server(eventlet.listen(('', 5000)), WebServer.app)
