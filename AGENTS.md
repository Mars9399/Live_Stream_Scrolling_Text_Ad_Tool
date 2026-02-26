# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This is a single-file PyQt5 desktop GUI application ("直播间滚动字幕广告工具" — Live Stream Scrolling Text Ad Tool). The entire application lives in `main.py`. See `README.md` for full feature details.

### Dependencies

- Python 3.6+ (system Python 3.12 available)
- PyQt5 (`pip install PyQt5`)
- No `requirements.txt` exists; the sole dependency is PyQt5

### Running the application

```bash
python main.py
```

The app opens a file dialog on startup asking for a `.txt` file with ad lines (one per line). A sample test file can be created:

```bash
echo -e "欢迎关注直播间\n限时特价活动" > test_ads.txt
```

### Display requirements

This is a GUI application. In headless environments, install `xvfb` and related Qt xcb libraries:

```bash
sudo apt-get install -y xvfb libxkbcommon-x11-0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libegl1 fonts-wqy-zenhei
```

For the Desktop pane (display `:1`), launch with `DISPLAY=:1 python main.py`. For headless testing use Xvfb on `:99`.

### Lint / Test / Build

- No linter, test framework, or build system is configured in this project.
- No automated tests exist.
- The project has no build step; it runs directly via `python main.py`.

### Gotchas

- The default font is `Microsoft YaHei` (Windows-only). On Linux, `fonts-wqy-zenhei` is a good CJK substitute and is automatically picked up by Qt.
- The app uses `Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint`, so it has no title bar and always stays on top.
- The file dialog on startup is blocking; the app won't proceed until a file is selected or the dialog is cancelled.
