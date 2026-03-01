# 🕐 Terminal Clock

An elegant analog clock rendered in your terminal. Built with pure Python, no dependencies.

<img width="443" height="483" alt="Screenshot" src="https://github.com/user-attachments/assets/220d04c4-06b2-4473-928b-b386980c675f" />

## Features

- 🎨 ASCII art analog clock with Unicode characters
- ⏱️ Real-time updates every second
- 🔴 Colored second hand (red accent)
- 🖥️ Full terminal control with ANSI codes
- ⚡ Lightweight and zero dependencies

## Quick Start

**Requirements:** Python 3.6+, terminal with ANSI support (macOS, Linux, Windows Terminal)

**Option 1: Clone & Run**
```bash
git clone https://github.com/gubarvlad/terminal-clock.git
cd terminal-clock
python clock.py
```

**Option 2: Run Directly (macOS/Linux)**
```bash
curl -s https://raw.githubusercontent.com/gubarvlad/terminal-clock/main/clock.py | python3
```

**Option 3: Run Directly (Windows)**
```powershell
curl.exe -s https://raw.githubusercontent.com/gubarvlad/terminal-clock/main/clock.py | python
```

Press `Ctrl+C` to exit.

**Note:** Terminal must be at least 42×21 characters.

## How It Works

Uses pure Python with:
- 2D canvas rendering for the clock face
- Trigonometry for hand positioning
- Unicode line drawing for visuals
- ANSI escape codes for terminal control

## License

© vladgubar, 2026
