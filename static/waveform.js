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
    }
    setDimensions(height) {
        this.canvas.width = window.innerWidth - 36;
        this.canvas.height = height;
        this.displayDataL = [];
        this.displayDataR = [];
        for (let k = 0; k < this.canvas.width; k++) {
            this.displayDataL.push(0);
            this.displayDataR.push(0);
            this.displayColor.push("#000000");
        }
        this.center_data_l = this.canvas.height/4;
        this.center_data_r = 3*this.canvas.height/4;
        // Fit the entire +/- 32768 range into L and R regions.
        this.displayScaling = this.canvas.height/32768 / 4;
        // Expect typical signals in the range of
        // +/- about 3000 so scale by 10.
        this.displayScaling *= 10;
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
            this.displayDataL.push(data_l[k]*this.displayScaling);
            this.displayDataR.shift();
            this.displayDataR.push(data_r[k]*this.displayScaling);
            this.displayColor.shift();
            if (recording_now) 
                this.displayColor.push("#FF0000");  // Red.
            else
                this.displayColor.push("#000000");  // Black.
        }

        // Draw left and right channel waveforms. Offset them vertically.
        this.drawWaveform(this.displayDataL, this.center_data_l);
        this.drawWaveform(this.displayDataR, this.center_data_r);

        // Draw ranges that the signal must meet in order to trigger a capture.
        let range = data_from_server['range'];
        this.drawRange( range[0]*this.displayScaling + this.center_data_l);
        this.drawRange( range[1]*this.displayScaling + this.center_data_l);
        this.drawRange(-range[0]*this.displayScaling + this.center_data_l);
        this.drawRange(-range[1]*this.displayScaling + this.center_data_l);
        this.drawRange( range[0]*this.displayScaling + this.center_data_r);
        this.drawRange( range[1]*this.displayScaling + this.center_data_r);
        this.drawRange(-range[0]*this.displayScaling + this.center_data_r);
        this.drawRange(-range[1]*this.displayScaling + this.center_data_r);

    }
    drawRange(rangeValue) {
        this.context.linewidth = 1;
        this.context.strokeStyle = "#A0A0A0";
        this.context.beginPath();
        this.context.moveTo(0, rangeValue);
        this.context.lineTo(this.canvas.width, rangeValue);
        this.context.stroke();
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