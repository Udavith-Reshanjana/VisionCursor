# VisionCursor

**VisionCursor** is a Python 3.10-based tool that lets you control your mouse cursor using hand gestures in real time through your webcam. Built with **MediaPipe**, **OpenCV**, and **PyAutoGUI**, it enables touchless human-computer interaction — ideal for accessibility, demos, or experimental user interface projects.

---

## ✨ Supported Gestures

| Fingers Up | Meaning     | Mouse Action           |
|------------|-------------|------------------------|
| 1 (Index)  | Move Cursor | `moveTo()`             |
| 2          | Drag        | `mouseDown()` / `mouseUp()` |
| 3          | Right Click | `rightClick()`         |
| 5          | Left Click  | `click()`              |

---

## ⚙️ Requirements

- **Python 3.10** (recommended)
- Webcam (built-in or external)
- Packages:
  - `opencv-python`
  - `mediapipe`
  - `pyautogui`

---

## 🔧 Installation & Setup

1. **Install Python 3.10**  
   [Download Python 3.10](https://www.python.org/downloads/release/python-3100/)

2. **Install the required packages**

```bash
pip install opencv-python mediapipe pyautogui

## 🚀 Running the Application

1. **Clone this repository:**

```bash
git clone https://github.com/Udavith-Reshanjana/VisionCursor.git
cd VisionCursor

2. **Run the main script:**

```bash
python vision_cursor.py

