# Mass Effect NOMAD-ND1 RC Vehicle Control

The Mass Effect NOMAD-ND1 collectible RC model vehicle was released back in 2017. This is very nicely-built vehicle with a fatal flaw - it was controlled over WiFi with either an iOS or Android app.

Fast-forward to 2024 and the iOS app is no longer downloadable and the Android app is marked as incompatible with most modern Android devices. Using an APK from an APK download site, this project aims to reverse-engineer the communication and control protocol and re-implement it in Python.

## Usage:
Connect your PC WiFi to the RC car's netwrok and run the Python script. Use keyboard for controls.

## Current state:
- Motion controls fully implemented with keyboard.

    | Control                 | Key                   | 
    | :-----------------------|:---------------------:| 
    | Direction               | [Up]/[Down] arrow     | 
    | Turn                    | [Left]/[Right] arrow  | 
    | Boost speed             | hold [Shift]          | 
    | Boost turn radius       | hold [Space]          | 
    | Exit                    | [Esc]                 | 

## TODO:
- Implement trim
- Implement LED control
- Implement video/audio streaming (hard??)
