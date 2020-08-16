# Piano Diagnostics

### Basic Features:
Step user through acquisition of 88 notes from a piano.
Aid the playing of each note so intensity and duration are consistent.
Store notes.
Perform signal processing.
Option of user-driven or MIDI-driven playing of the notes.

### User IO:
Enter the directory for storing the recorded notes.
Enter the start note (1 = lowest A, 88 = highest C).
Select whether user plays the notes on the piano or MIDI automatically plays the notes.
The user is expected to incrementally play notes by semitone. MIDI does this automatically.
It is ok to switch between user input and MIDI input at any time.

### Waveform display:
The waveform display shows the audio input being received in real-time.
The upper chart is left channel and the lower chart is right channel.
The signal must be in between the two ranges shown on the chart in order to trigger saving the note.
When the note is being saved, the waveform turns red.

### Goals:
Analysis of piano sound timbre.
Track changes in acoustic piano over time.

### Architecture:
Similar to an architecture I have been using for many of my musical computer science projects (very, very few are on github). Python for server. Javascript or Typescript for client. Simple socket interface. HTML canvas for graphics. Mostly I spend my time on applications not the infrastructure.

### Versions:
1 Initial work. Fair amount of experimenting in the code.
2 Get most initial release features running.