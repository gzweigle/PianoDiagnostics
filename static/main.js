// Gregary C. Zweigle
// 2020

import { UserIO } from './userIO.js';
import { Notification } from './notification.js';
import { Titlebar } from './titlebar.js';
import { Waveform } from './waveform.js';
var socket = io.connect("http://localhost:5000");

let userIO = new UserIO(document);
let notification = new Notification(document);
let titlebar = new Titlebar(document);
let waveform = new Waveform(document);

window.addEventListener('resize', function(event) {
        notification.setWidth();
        titlebar.setWidth(window.innerWidth - 36);
        titlebar.setHeight(50);
        waveform.setWidth();
});
window.dispatchEvent(new Event('resize'));

// Start the client.
socket.emit('client_ready', {
    'recordMode': userIO.getRecordMode(),
    'recordDirectory': userIO.getRecordDirectory(),
    'recordStartNote' : userIO.getRecordStartNote(),
    'playbackMode' : userIO.getPlaybackMode(),
    'playbackDirectory' : userIO.getPlaybackDirectory(),
    'playbackStartNote' : userIO.getPlaybackStartNote()
});

// When get data from the client, do something,
// then, tell the client to run again.
socket.on('data_from_server', function (data_from_server) {

    titlebar.draw();
    notification.draw(data_from_server, userIO.getRecordStatusMessage());
    waveform.draw(data_from_server);

    socket.emit('client_ready', {
        'recordMode': userIO.getRecordMode(),
        'recordDirectory': userIO.getRecordDirectory(),
        'recordStartNote' : userIO.getRecordStartNote(),
        'playbackMode' : userIO.getPlaybackMode(),
        'playbackDirectory' : userIO.getPlaybackDirectory(),
        'playbackStartNote' : userIO.getPlaybackStartNote()
    });

});