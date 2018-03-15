from flask import Flask, session, request, redirect, render_template, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

# config
app.config.from_object('config')

# tool
socketio = SocketIO(app)
db = SQLAlchemy(app)
Session(app)

# model
from model import User
from model import Chat


@app.route('/')
def index():
    if session.get('auth') is None:
        return redirect(url_for('auth'), 200)

    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        auth = request.form

        if auth.get('type') == '1':
            user_id = auth.get('id')

            user = None

            if user is None:
                pass

            # name = user.name
            name = 'User'
        else:
            user_id = None
            name = auth.get('name') if auth.get('name') else 'Guest'

        session['auth.id'] = user_id
        session['auth.name'] = name

        return redirect(url_for('index'), 200)

    return render_template('auth.html')

@socketio.on('send message', namespace='/chat')
def chat(message):
    if session.get('auth') is not None:
        # TODO save to DB
        data = {
            'name': session['auth.name'],
            'data': message['data']
        }
        emit('show message', data, broadcast=True)


@socketio.on('connect', namespace='/chat')
def connect():
    if session.get('auth') is not None:
        emit('show message', {'data': '<' + session['auth.name'] + '>成功连接'})


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    print('Client disconnected')


@app.route('/create_db')
def create_db():
    print(db)
    db.create_all()

    return 'success'

@app.route('/get_all')
def get_all():
    print(User.query.all())

    return 'get'


if __name__ == '__main__':
    socketio.run(app, port=4500, host='0.0.0.0')
