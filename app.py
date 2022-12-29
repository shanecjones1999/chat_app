from flask import Flask, session, render_template, request, redirect, jsonify, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.secret_key = 'my_secret_key'
socketio = SocketIO(app)

rooms = {
    'room1': [],
    'room2': []
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect('/create-room')
    return render_template('index.html')

@app.route('/create-room', methods=['GET', 'POST'])
def create_room():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        room = request.form['room-name']
        session['room'] = room
        rooms[room] = []
        return redirect(url_for('room', room=room))
    return render_template('create-room.html', username=session.get('username'))

@app.route('/<room>')
def room(room):
    if 'username' not in session:
        return redirect('/')
    return render_template('room.html', room=room, username=session.get('username'))

@app.route('/rooms')
def get_rooms():
  return jsonify({'rooms': list(rooms.keys())})

@socketio.on('join')
def on_join():
    username = session.get('username')
    room = session.get('room')
    rooms[room].append(username)
    join_room(room)
    emit('message', {'username': 'Server', 'message': f'{username} has joined the room.'}, room=room)

@socketio.on('disconnect')
def on_disconnect():
  room = session.get('room')
  if room:
    username = session.get('username')
    rooms[room].remove(username)
    leave_room(room)
    socketio.emit('message', {'username': 'Server', 'message': f'{username} has left the room.'}, room=room)

@socketio.on('message')
def on_message(data):
    username = session.get('username')
    room = session.get('room')
    message = data['message']
    emit('message', {'username': username, 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
