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

### Method 1: Using the Pre-built Executable (Easy)
1. Go to the **Releases** tab on the right side of this GitHub page.
2. Download `P5_Bubble_Typing.exe`.
3. Double click the `.exe` file to run it. No installation required!

### Method 2: Running from Source Code
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
If you are running from source, make sure `bubble.png` is in the same directory as the script. The pre-built `.exe` already has the image bundled inside.
