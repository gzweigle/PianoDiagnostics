// Gregary C. Zweigle
// 2020

export class Titlebar {
    constructor(document) {
        this.canvas = document.getElementById("canvasTitlebar");
        this.context = this.canvas.getContext("2d");
    }
    setDimensions(height) {
        this.canvas.width = window.innerWidth - 36;
        this.canvas.height = height;
    }
    draw() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.context.beginPath();
        this.context.strokeStyle = "#000000";
        this.context.lineWidth = 1;
        this.context.rect(0, 0, this.canvas.width, this.canvas.height);
        this.context.stroke()
        this.context.font = "18px Courier";
        this.context.fillStyle = "#000000";
        this.context.fillText('Greg\'s totally awesome Piano Diagnostics', 2, 28);
    }
}