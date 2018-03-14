from flask import Flask, session, request, redirect, render_template, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

# config
app.config['SECRET_KEY'] = "Z'Nf91\x07wL\xf5\x12\x87~:#\x8aLpZW95\xdc\x1d"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host/db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SESSION_FILE_DIR'] = 'dump/session'
app.config['SESSION_TYPE'] = 'filesystem'

socketio = SocketIO(app)
db = SQLAlchemy(app)
Session(app)


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


if __name__ == '__main__':
    socketio.run(app, port=4500, host='0.0.0.0', debug=True)
