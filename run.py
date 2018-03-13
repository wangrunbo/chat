from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = b"Z'Nf91\x07wL\xf5\x12\x87~:#\x8aLpZW95\xdc\x1d"
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send message', namespace='/chat')
def chat(message):
    emit('show message', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/chat')
def connect():
    emit('show message', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/chat')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, port=4500, debug=True)
