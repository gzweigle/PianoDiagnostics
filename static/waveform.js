// Gregary C. Zweigle
// 2020

export class Waveform {
    constructor(document) {
        this.canvas = document.getElementById("canvasWaveform");
        this.context = this.canvas.getContext("2d");
        this.cell = document.getElementById("Waveform");
        this.displayDataL = [];
        this.displayDataR = [];
        this.displayColor = [];
        this.displayScaling = 128;
    }
    setWidth() {
        this.canvas.width = this.cell.offsetWidth - 36;
        this.displayDataL = [];
        this.displayDataR = [];
        for (let k = 0; k < this.canvas.width; k++) {
            this.displayDataL.push(0);
            this.displayDataR.push(0);
            this.displayColor.push("#000000");
        }
    }
    draw(data_from_server) {

        // Clear old values, then make a box around the waveform display region.
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.context.beginPath();
        this.context.strokeStyle = "#000000";
        this.context.lineWidth = 1;
        this.context.rect(0, 0, this.canvas.width, this.canvas.height);
        this.context.stroke()

        // Push data values from the server into a buffer that represents
        // the pixels on the screen. Also, store the line color so it
        // changes when recording or not recording.
        let data_l = data_from_server['data_l_down'];
        let data_r = data_from_server['data_r_down'];
        let recording_now = data_from_server['recording_now']
        for (let k = 0; k < data_l.length; k++) {
            this.displayDataL.shift();
            this.displayDataL.push(data_l[k]/this.displayScaling);
            this.displayDataR.shift();
            this.displayDataR.push(data_r[k]/this.displayScaling);
            this.displayColor.shift();
            if (recording_now) 
                this.displayColor.push("#FF0000");  // Red.
            else
                this.displayColor.push("#000000");  // Black.
        }

        // Draw left and right waveforms. Offset them vertically.
        this.drawWaveform(this.displayDataL, 50);
        this.drawWaveform(this.displayDataR, 100);

    }
    // Draw the waveforms. And, when switching colors need to end the
    // present path, stroke, then start a new path.
    drawWaveform(displayData, offset) {
        this.context.linewidth = 1;
        this.context.strokeStyle = this.displayColor[0];
        this.context.beginPath();
        this.context.moveTo(0, displayData[0] + offset);
        for (let k = 1; k < displayData.length; k++) {
            this.context.lineTo(k, displayData[k] + offset);
            if (this.displayColor[k] != this.displayColor[k-1]) {
                this.context.stroke();
                this.context.strokeStyle = this.displayColor[k];
                this.context.beginPath();
            }
        }
        this.context.stroke();
    }
}