from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins="*")  # 允许跨域


@socketio.on('connect')
def on_connect():
    print("Client connected")
    emit('server_message', {'message': 'Welcome, client!'})


# 处理客户端发送的消息
@socketio.on('message')
def handle_message(data):
    print("Message from client: {data['message']}")
    emit('server_message', {'message': "Server received: {data['message']}"}, broadcast=True)


# 处理客户端断开连接
@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected")


def push_to_frontend(event, data):
    if data is not None:
        socketio.emit(event, data)


def start_websocket(app):
    # 将 socketio 实例绑定到 Flask 应用
    socketio.init_app(app)
    # 启动 WebSocket 监听服务
    socketio.run(app, allow_unsafe_werkzeug=True, host="0.0.0.0", port=5000)
