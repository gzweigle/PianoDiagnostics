// Gregary C. Zweigle
// 2020

import { Notification } from './notification.js';
import { Titlebar } from './titlebar.js';
import { UserIO } from './userIO.js';
import { Waveform } from './waveform.js';
var socket = io.connect("http://localhost:5000");

let notification = new Notification(document);
let titlebar = new Titlebar(document);
let userIO = new UserIO(document);
let waveform = new Waveform(document);

window.addEventListener('resize', function(event) {
        notification.setDimensions();
        titlebar.setDimensions(50);
        waveform.setDimensions(300);
});
window.dispatchEvent(new Event('resize'));

// Start the client.
socket.emit('client_ready', {
    'recordMode': userIO.getRecordMode(),
    'recordDirectory': userIO.getRecordDirectory(),
    'recordStartNote' : userIO.getRecordStartNote(),
    'recordMidi' : userIO.getRecordMidi(),
});

// When get data from the client, do something,
// then, tell the client to run again.
socket.on('data_from_server', function (data_from_server) {

    notification.draw(data_from_server, userIO.getRecordStatusMessage());
    titlebar.draw();
    waveform.draw(data_from_server);

    socket.emit('client_ready', {
        'recordMode': userIO.getRecordMode(),
        'recordDirectory': userIO.getRecordDirectory(),
        'recordStartNote' : userIO.getRecordStartNote(),
        'recordMidi' : userIO.getRecordMidi()
    });

});