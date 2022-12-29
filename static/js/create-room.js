// Get the list of active rooms
fetch('/rooms')
.then(response => response.json())
.then(data => {
  // Populate the select input with the list of rooms
  const select = document.getElementById('room-select');
  data.rooms.forEach(room => {
    const option = document.createElement('option');
    option.value = room;
    option.text = room;
    select.add(option);
  });
});