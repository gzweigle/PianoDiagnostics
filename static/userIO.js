// Gregary C. Zweigle
// 2020

// TODO - this file needs work!!

export class UserIO {
    constructor(document) {
        this.recordButton = document.getElementById("recordButton");
        this.recordButton.addEventListener("click", (e) => { this.clickRecord(); });
        this.playbackButton = document.getElementById("playbackButton");
        this.playbackButton.addEventListener("click", (e) => { this.clickPlayback(); });
        this.recordRedo = document.getElementById("recordRedo");
        this.recordRedo.addEventListener("click", (e) => { this.clickRecordRedo(); });
        this.playbackRedo = document.getElementById("playbackRedo");
        this.playbackRedo.addEventListener("click", (e) => { this.clickPlaybackRedo(); });
        this.recordMode = false;
        this.playbackMode = false;
        this.recordDirectory = "test";
        this.recordStartNote = "21";
        this.recordStatusMessage = "Ok";
        this.playbackDirectory = "test";
        this.playbackStartNote = "21";
        this.playbackStatusMessage = "Ok";
    }
    clickRecord() {
        if (this.recordMode == false && this.playbackMode == false) {
            this.recordDirectory = document.getElementById("recordInput").value;
            this.recordStartNote = document.getElementById("recordStartNote").value;
            this.recordStartNote = Number(this.recordStartNote)
            if (this.recordStartNote >= 0 && this.recordStartNote < 88 &&
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
            if (this.playbackMode == true) {
                this.recordStatusMessage = "Cannot record while in playback.";
            }
        }
    }
    clickPlayback() {
        if (this.playbackMode == false && this.recordMode == false) {
            this.playbackDirectory = document.getElementById("playbackInput").value;
            this.playbackStartNote = document.getElementById("playbackStartNote").value;
            this.playbackStartNote = Number(this.playbackStartNote)
            if (this.playbackStartNote >= 0 && this.playbackStartNote < 88 &&
                this.localCheckForLetters(this.playbackDirectory)) {
                    this.playbackButton.innerHTML = "Stop";
                    this.playbackMode = true;
            }
            else {
                this.playbackButton.innerHTML = "Start";
                this.playbackMode = false;
            }
        }
        else {
            this.playbackButton.innerHTML = "Start";
            this.playbackMode = false;
        }
    }
    clickRecordRedo() { }
    clickPlaybackRedo() { }

    // Getters.
    getRecordMode() { return this.recordMode; }
    getRecordDirectory() { return this.recordDirectory; }
    getRecordStartNote() { return this.recordStartNote; }
    getRecordStatusMessage() {return this.recordStatusMessage;}
    getPlaybackMode() { return this.playbackMode; }
    getPlaybackDirectory() { return this.playbackDirectory; }
    getPlaybackStartNote() { return this.playbackStartNote; }

    // Local utility functions.
    localCheckForLetters(str) {
        let returnBoolean;
        if (str.match("^[A-Za-z0-9]+$") == null) {
            returnBoolean = false;
        }
        else {
            returnBoolean = true;
        }
        return returnBoolean;
    }
}