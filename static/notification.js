// Gregary C. Zweigle
// 2020

export class Notification {
    constructor(document) {
        this.canvas = document.getElementById("canvasNotification");
        this.context = this.canvas.getContext("2d");
        this.cell = document.getElementById("Notification");
    }
    setDimensions() {
        this.canvas.width = this.cell.offsetWidth - 36;
    }
    draw(data_from_server, recordStatusMessage) {

        // Clear old values, then make a box around the waveform display region.
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.context.beginPath();
        this.context.strokeStyle = "#000000";
        this.context.lineWidth = 1;
        this.context.rect(0, 0, this.canvas.width, this.canvas.height);
        this.context.stroke()

        // Get messages from the server.
        let status_msg = data_from_server['status_msg'];
        let error_msg = data_from_server['error_msg'];
        let peak_msg = data_from_server['peak_msg'];

        // Display notifications.
        this.context.font = "16px Courier";
        this.context.fillStyle = "#000000";
        this.context.fillText('Record Details', 2, 16);
        this.context.fillText("User Input Status: " + recordStatusMessage, 20, 32);
        this.context.fillText("Server Status:     " + status_msg, 20, 48);
        this.context.fillText("Server Errors:     " + error_msg, 20, 64);
        this.context.fillText("Present Peak:      " + peak_msg, 20, 80);
    }
}