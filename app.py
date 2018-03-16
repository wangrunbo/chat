from datetime import datetime
from flask import Flask, session, request, redirect, render_template, url_for, escape
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
        return redirect(url_for('auth'))

    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        auth = request.form

        if auth.get('type') == '1':
            user_id = auth.get('id')

            user = User.query.filter_by(uid=user_id).first()

            if user is None:
                return render_template('auth.html', user_id=user_id)

            user_id = user.id
            name = user.name
        else:
            user_id = None
            name = auth.get('name') if auth.get('name') else 'Guest'

        session['auth'] = {
            'id': user_id,
            'name': name
        }

        return redirect(url_for('index'))

    return render_template('auth.html')


@socketio.on('send message', namespace='/chat')
def chat(message):
    if session.get('auth') is not None:
        chat = Chat(user_id=session['auth']['id'], name=session['auth']['name'], datetime=datetime.now(), content=message['data'])

        db.session.add(chat)
        db.session.commit()

        __emit('show message', {'name': chat.name, 'data': chat.content}, broadcast=True)


@socketio.on('connect', namespace='/chat')
def connect():
    if session.get('auth') is not None:
        __emit('show message', {'data': '<' + session['auth']['name'] + '>成功连接'})


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    print('Client disconnected')


def __emit(event, data, *args, **kwargs):
    emit(event, __escape(data), *args, **kwargs)


def __escape(data):
    if type(data) is str:
        escape_data = escape(data)
    elif type(data) is list:
        escape_data = []
        for element in data:
            escape_data.append(__escape(element))
    elif type(data) is dict:
        escape_data = {}
        for k, v in data.items():
            escape_data[__escape(k)] = __escape(v)
    else:
        return data

    return escape_data


if __name__ == '__main__':
    socketio.run(app, port=4500, host='0.0.0.0')
