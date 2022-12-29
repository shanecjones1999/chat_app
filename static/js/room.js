const socket = io.connect();

socket.emit('join');

// Handle the 'message' event
socket.on('message', data => {
    const li = document.createElement('li');
    li.innerHTML = `${data.username}: ${data.message}`;
    document.getElementById('messages').appendChild(li);
});

document.getElementById('message-form').onsubmit = e => {
    e.preventDefault();
    const input = document.getElementById('message');
    const message = input.value;
    socket.emit('message', {'message': message});
    input.value = '';
};