// Gregary C. Zweigle
// 2020

export class UserIO {
    constructor(document) {
        this.recordButton = document.getElementById("recordButton");
        this.recordButton.addEventListener("click",
        (e) => { this.clickRecord(); });
        this.recordMidiButton = document.getElementById("recordMidiButton");
        this.recordMidiButton.addEventListener("click", (e) =>
        { this.clickRecordMidiButton(); });
        this.recordMode = false;
        this.recordDirectory = "test";
        this.recordStartNote = "21";
        this.recordMidi = false;
        this.recordStatusMessage = "Ok";
    }
    clickRecord() {
        if (this.recordMode == false) {
            this.recordDirectory = document.getElementById("recordInput").value;
            this.recordStartNote = document.getElementById("recordStartNote").value;
            this.recordStartNote = Number(this.recordStartNote)
            if (this.recordStartNote > 0 && this.recordStartNote <= 88 &&
                this.localCheckForLetters(this.recordDirectory)) {
                this.recordButton.innerHTML = "Stop";
                this.recordMode = true;
                this.recordStatusMessage = "Everthing is a-ok!";
            }
            else {
                this.recordButton.innerHTML = "Start";
                this.recordMode = false;
                this.recordStatusMessage = "Directory name or start note error.";
            }
        }
        else {
            this.recordButton.innerHTML = "Start";
            this.recordMode = false;
        }
    }
    clickRecordMidiButton() {
        if (this.recordMidi == true) {
            this.recordMidi = false;
            this.recordMidiButton.innerHTML = "User";
        }
        else {
            this.recordMidi = true;
            this.recordMidiButton.innerHTML = "Midi";
        }
    }

    getRecordMode() { return this.recordMode; }
    getRecordDirectory() { return this.recordDirectory; }
    getRecordStartNote() { return this.recordStartNote; }
    getRecordStatusMessage() {return this.recordStatusMessage;}
    getRecordMidi() {return this.recordMidi;}

    localCheckForLetters(str) {
        let result;
        if (str.match("^[A-Za-z0-9]+$") == null) {
            result = false;
        }
        else {
            result = true;
        }
        return result;
    }
}