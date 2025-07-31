Hand Gesture Control System
This project is an innovative, real-time hand gesture control system that allows users to interact with their computer using intuitive hand movements. By leveraging advanced computer vision and machine learning, it translates specific hand poses into fundamental system commands, including mouse cursor control, volume adjustment, and screen scrolling.
The system is built on a modular architecture, utilizing Google's MediaPipe framework for robust hand tracking and various Python libraries for system integration. This touchless interface provides an accessible and modern alternative to traditional input devices, suitable for presentations, gaming, and ergonomic computing.

🌟 Features

Real-time Hand Tracking: Accurately detects and tracks 21 anatomical landmarks of a single hand.
Mouse Cursor Control: Navigate the on-screen cursor smoothly with the movement of your index finger.
Gesture-based Clicks: Perform left and right mouse clicks using distinct gestures (e.g., pinching thumb and index finger for left click).
Volume Control: Adjust the system's master volume by changing the distance between your thumb and index finger.
Scrolling: Scroll up and down in applications or web pages by moving your index and middle fingers vertically.
Intuitive Interface: Provides clear on-screen visual feedback to guide user interaction.

⚙️ Prerequisites

Before you begin, ensure you have the following installed on your system:
Python 3.x: The project is developed and tested with Python 3.
Windows OS: The pycaw library used for volume control is specific to Windows.

🚀 Installation

Follow these steps to get the project up and running on your local machine.


1. Clone the Repository
   
First, clone this GitHub repository to your local machine using git:
git clone https://github.com/your_username/hand-gesture-control.git
cd hand-gesture-control


3. Install Dependencies

The project relies on several Python libraries. You can install all of them at once using pip:
pip install opencv-python mediapipe pyautogui pycaw numpy


opencv-python: For webcam access and image processing.
mediapipe: The core library for hand detection and tracking.
pyautogui: For controlling the mouse and scrolling.
pycaw: For managing system volume (Windows-specific).
numpy: For mathematical operations, such as interpolation.
🎮 Usage
To start the hand gesture control system, simply run the main.py script from your terminal.
python main.py


A window titled "Hand LiveFeed" will open, displaying your webcam's video feed. The system will start in Neutral mode.
Controls:
The system uses keyboard shortcuts to switch between different control modes.
c: Activate Cursor mode.
Mouse Movement: Move the on-screen cursor with the position of your index finger.
Left Click: Pinch your thumb and index finger together, or your thumb and pinky finger.
Right Click: Pinch your thumb and middle finger together.
v: Activate Volume mode.
Volume Adjustment: Change the system volume by adjusting the distance between your thumb and index finger. A larger distance decreases the volume, while a smaller distance increases it.
s: Activate Scroll mode.
Scroll Up: Point your index and middle fingers up and move them upwards.
Scroll Down: Point your index and middle fingers up and move them downwards.
n: Switch back to Neutral mode. In this mode, no gestures are recognized as commands.
q: Quit the application.

📂 File Structure

HandTrackingModule.py: Contains the HandDetector class, which acts as an abstraction layer for MediaPipe's hand tracking functionality. It is responsible for detecting hands and extracting landmark coordinates.
main.py: The main application script. It initializes the webcam, integrates the HandDetector module, and contains the core logic for gesture recognition, mode switching, and system control using pyautogui and pycaw.

⏭️ Future Scope

This project serves as a strong foundation, and there are many exciting possibilities for future development:
Additional Gestures: Add more gestures for drag-and-drop, zooming, and application switching.
Multi-Hand Support: Implement support for two-handed gestures to enable more complex interactions.
Customizable Gestures: Allow users to define and train their own gestures for personalized control.
Cross-Platform Compatibility: Extend volume control to macOS and Linux.
Enhanced UI: Develop a graphical user interface for a more user-friendly experience.

🤝 Contributing

We welcome contributions! Feel free to fork this repository, create a new branch, and submit a pull request with your changes. Please ensure your code follows a clean and consistent style.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
