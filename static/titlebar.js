// Gregary C. Zweigle
// 2020

export class Titlebar {
    constructor(document) {
        this.canvas = document.getElementById("canvasTitlebar");
        this.context = this.canvas.getContext("2d");
    }
    setWidth(width) {
        this.canvas.width = width;
    }
    setHeight(height) {
        this.canvas.height = height;
    }
    draw() {
        // Clear old values, then make a box around the waveform display region.
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.context.beginPath();
        this.context.strokeStyle = "#000000";
        this.context.lineWidth = 1;
        this.context.rect(0, 0, this.canvas.width, this.canvas.height);
        this.context.stroke()

        // Title
        this.context.font = "18px Courier";
        this.context.fillStyle = "#000000";
        this.context.fillText('Greg\'s totally awesome Piano Diagnostics', 2, 28);

    }
}