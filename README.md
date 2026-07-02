# Persona 5 Desktop Typing Bubble

A lightweight, portable Python script that displays live-updating Persona 5-style speech bubbles on your Windows desktop as you type!

## Features
- **Persona 5 Aesthetic**: Beautifully styled transparent overlay bubbles.
- **Stacking & Fading**: Bubbles smoothly push each other up (up to 3) and fade away gently.
- **Breathing Animation**: The UI elements float and "breathe" dynamically, recreating the kinetic UI of the game.
- **Unikey Anti-Ghosting**: Includes a custom algorithm tailored for Vietnamese IME (Unikey/EVKey) to eliminate duplicate/ghost characters while typing.
- **Auto-Capitalization**: First letters are capitalized for maximum style.

## Requirements
- Python 3
- Windows OS

## Installation
1. Clone the repository.
2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
3. Run the script:
   ```cmd
   pythonw p5bubble.py
   ```

## Note
Make sure `bubble.png` is in the same directory as the script.
