# ⚡🔋 Cool Battery Charging Animations

A funny animation for your Windows PC charging battery icon - when it starts exceeding 100%, the "liquid battery" starts speeling around your task bar and flooding it!

<img width="172" height="72" alt="Screenshot 2026-11-07 194429" src="https://github.com/user-attachments/assets/4e4afec8-74cd-4441-9e81-0d907e877ef2" />

<img width="416" height="75" alt="Screenshot 2026-11-07 195016" src="https://github.com/user-attachments/assets/16a36ed5-e437-4e96-b440-4ecdd449a7ff" />

<img width="251" height="51" alt="Screenshot 2026-11-07 194714" src="https://github.com/user-attachments/assets/6f91a479-f970-4dbb-a609-938caeba85cc" />

## ✨ Features
- **Fluid Charging Physics:** Smooth liquid level animations that react to your battery percentage.
- **Overcharge Overflow Effect:** When charging past 100%, the battery bar bulges under pressure, vibrates gently, and drips glowing liquid onto the taskbar.
- **Taskbar Liquid Wave:** Falling droplets accumulate at the bottom edge of the screen and flow smoothly across your taskbar.
- **100% Click-Through Overlay:** Built with Windows transparency API flags (`WS_EX_TRANSPARENT`) so your mouse clicks pass right through to the Start menu, icons, and open windows.
- **Instant Preview Mode:** Starts at `96%` by default so you can immediately see the full charging and overflow animation without waiting for a full battery cycle.

## 🚀 Getting Started

### Prerequisites
- Windows 10 or Windows 11
- Python 3.8 or higher

### Installation & Running
1. **Clone or download this repository:**
   ```bash
   git clone https://github.com
   cd fun-battery-tray
   ```

2. **Install the required library:**
   ```bash
   python -m pip install psutil
   ```

3. **Run the animation:**
   ```bash
   python main.py
   ```
   *(To stop the animation, press `Ctrl + C` in the terminal or close the console window).*

## ⚙️ Customization
You can easily tweak the animation behavior inside `main.py`:
- `self.demo_mode = True`: Change to `False` to trigger the animation only when your laptop is physically plugged into a power source.
- `self.charge = 96.0`: Adjust the starting percentage for the preview mode.
- `base_x = self.width - 142`: Fine-tune the horizontal alignment if your taskbar battery icon sits slightly further left or right.

## 📦 Building a Standalone Executable (`.exe`)
To compile the project into a single `.exe` file that runs with a double-click (no Python required):

1. **Install PyInstaller:**
   ```bash
   python -m pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   python -m PyInstaller --noconsole --onefile --name CoolBatteryAnimation main.py
   ```

3. Find your compiled `CoolBatteryAnimation.exe` inside the `dist/` folder.

## 🤝 Contributing
Want to add more cool charging animations (like plasma bolts, lava, coffee cup, or neon pulse)? Feel free to fork this repo and submit a Pull Request!
