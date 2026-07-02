"""Persona 5 speech bubble - Ultimate version with Unikey anti-ghosting."""
import tkinter as tk
import threading
import time
import queue
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pynput import keyboard

import os

DIALOG_PATH  = os.path.join(os.path.dirname(__file__), "bubble.png")
DIALOG_SCALE = 0.28
FADE_AFTER   = 1.5
FADE_DURATION = 0.4
FONT_SIZE    = 20
SPACING      = -10

def get_font(size):
    for p in [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

FONT = get_font(FONT_SIZE)

raw = Image.open(DIALOG_PATH).convert("RGBA")
dw  = int(raw.width  * DIALOG_SCALE)
dh  = int(raw.height * DIALOG_SCALE)
base_dialog = raw.resize((dw, dh), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)

def render(char):
    bg = Image.new("RGBA", (dw, dh), (1, 1, 1, 255))
    bg.paste(base_dialog, mask=base_dialog.split()[3])
    img  = bg.convert("RGB")
    if char:
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), char, font=FONT)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        cx, cy = int(dw * 0.48), int(dh * 0.50)
        tx, ty = cx - tw//2, cy - th//2
        draw.text((tx+1, ty+1), char, font=FONT, fill=(0,0,0))
        draw.text((tx,   ty  ), char, font=FONT, fill=(255,255,255))
    return img

key_queue = queue.Queue()

def on_press(key):
    try:
        c = key.char
        if c and c.isalnum():
            key_queue.put(('TYPE', c.lower(), time.time()))
    except AttributeError:
        if key in (keyboard.Key.space, keyboard.Key.enter):
            key_queue.put(('FINISH', None, time.time()))
        elif key == keyboard.Key.backspace:
            key_queue.put(('DEL', None, time.time()))

def start_listener():
    with keyboard.Listener(on_press=on_press) as lst:
        lst.join()

def main():
    root = tk.Tk()
    root.withdraw()
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    wx = sw - dw - 20
    BASE_Y = 70 + 2 * (dh + SPACING)
    
    class Bubble:
        def __init__(self, char):
            self.win = tk.Toplevel(root)
            self.win.overrideredirect(True)
            self.win.attributes("-topmost", True)
            self.win.configure(bg="#010101")
            self.win.wm_attributes("-transparentcolor", "#010101")
            
            self.label = tk.Label(self.win, bg="#010101", bd=0, highlightthickness=0)
            self.label.pack()
            
            self.char = char
            self.slot = 0
            self.target_y = BASE_Y
            self.current_y = BASE_Y + 15
            self.alpha = 1.0
            self.created_at = time.time()
            self.force_fade = False
            
            self.refresh_image()
            self.win.geometry(f"{dw}x{dh}+{wx}+{int(self.current_y)}")
            self.win.deiconify()
            self.win.lift()
            
        def refresh_image(self):
            # Capitalize visually only, buffer remains exactly as typed
            display_text = self.char.capitalize() if self.char else ""
            self.img = render(display_text)
            self.tk_img = ImageTk.PhotoImage(self.img)
            self.label.configure(image=self.tk_img)

        def update_position(self):
            self.target_y = BASE_Y - self.slot * (dh + SPACING)
            
        def update(self):
            import math
            self.current_y += (self.target_y - self.current_y) * 0.35
            if abs(self.current_y - self.target_y) < 0.5:
                self.current_y = self.target_y
                
            # Animation: Breathing / Floating effect (Reduced movement)
            t = time.time()
            phase = self.created_at
            breath_y = math.sin(t * 2.5 + phase) * 1.5
            breath_x = math.cos(t * 1.5 + phase) * 1.0
            
            display_y = int(self.current_y + breath_y)
            display_x = int(wx + breath_x)
            
            self.win.geometry(f"{dw}x{dh}+{display_x}+{display_y}")
            
            elapsed = time.time() - self.created_at
            if self.force_fade or elapsed > FADE_AFTER:
                if self.force_fade and elapsed < FADE_AFTER:
                    self.created_at = time.time() - FADE_AFTER
                    elapsed = time.time() - self.created_at
                
                fade = (elapsed - FADE_AFTER) / FADE_DURATION
                self.alpha = max(0.0, 1.0 - fade)
                
            self.win.attributes("-alpha", min(1.0, self.alpha))
            return self.alpha > 0.01

    bubbles = []
    active_bubble = [None]
    pending_events = []

    def update_loop():
        nonlocal pending_events
        while not key_queue.empty():
            pending_events.append(key_queue.get_nowait())
            
        now = time.time()
        events_to_process = []
        
        # Unikey Anti-Ghosting algorithm
        idx = 0
        while idx < len(pending_events):
            ev, val, t = pending_events[idx]
            
            if ev == 'TYPE':
                has_subsequent_del = False
                if idx + 1 < len(pending_events):
                    if pending_events[idx+1][0] == 'DEL' and (pending_events[idx+1][2] - t) < 0.05:
                        has_subsequent_del = True
                        
                if has_subsequent_del:
                    # Unikey swallowed this key to compose a character. Drop the physical keystroke.
                    idx += 1
                    continue
                else:
                    if now - t < 0.05:
                        # Wait 50ms to be absolutely sure Unikey doesn't swallow it
                        break
                    else:
                        events_to_process.append((ev, val))
            else:
                events_to_process.append((ev, val))
            
            idx += 1
            
        pending_events = pending_events[idx:]
        
        # Process confirmed keystrokes
        for ev, val in events_to_process:
            if ev == 'TYPE':
                if active_bubble[0] is None:
                    # New bubble
                    for b in bubbles:
                        b.slot += 1
                        b.update_position()
                        if b.slot >= 3:
                            b.force_fade = True
                    active_bubble[0] = Bubble(val)
                    bubbles.append(active_bubble[0])
                else:
                    b = active_bubble[0]
                    b.char += val
                    if len(b.char) > 15:
                        b.char = b.char[:15]
                    b.refresh_image()
                    b.created_at = time.time()
                    
            elif ev == 'DEL':
                if active_bubble[0]:
                    b = active_bubble[0]
                    if len(b.char) > 0:
                        b.char = b.char[:-1]
                        b.refresh_image()
                        b.created_at = time.time()
                    
            elif ev == 'FINISH':
                active_bubble[0] = None

        alive_bubbles = []
        for b in bubbles:
            if b.update():
                alive_bubbles.append(b)
            else:
                if b is active_bubble[0]:
                    active_bubble[0] = None
                b.win.destroy()
        
        bubbles.clear()
        bubbles.extend(alive_bubbles)
        root.after(20, update_loop)

    # Demo
    key_queue.put(('TYPE', 'p', time.time()))
    key_queue.put(('TYPE', '5', time.time()))
    
    threading.Thread(target=start_listener, daemon=True).start()
    update_loop()
    root.mainloop()

if __name__ == "__main__":
    main()
