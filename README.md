# ✍️ Air Writing & Optical Character Recognition (OCR) System

An advanced, real-time Computer Vision application that allows users to write in the air using hand gestures and translates those drawings into digital text using OCR. 

Built with Python, OpenCV, and Google's MediaPipe, this project demonstrates robust state-management, real-time image processing, and machine learning integration.

## ✨ Features & Gesture Controls

This system uses an intuitive, state-based gesture control mechanism:

* **✏️ Write Mode (1 Finger):** Raise only your Index finger to draw on the virtual canvas.
* **🧽 Erase Mode (2 Fingers):** Raise your Index and Middle fingers together to erase mistakes with a thick stroke.
* **🛑 Hover Mode (Fist/Other):** Close your hand to lift the virtual pen and move your cursor without drawing.
* **🧹 Clear Canvas (Open Palm):** Show your entire hand to instantly wipe the board clean.
* **🔍 OCR Scan (Keyboard 's'):** Press the `s` key to capture the canvas, preprocess the image, and extract the written characters using Tesseract OCR.

## 🛠️ Technology Stack

* **Computer Vision:** OpenCV (`cv2`)
* **Hand Tracking:** MediaPipe (`mediapipe`)
* **Matrix Math & Masking:** NumPy (`numpy`)
* **Text Recognition:** PyTesseract (`pytesseract`)

## ⚙️ Installation & Setup

### 1. Prerequisites
* **Python 3.10 or 3.11** (Highly recommended for MediaPipe compatibility on Windows).
* **Tesseract OCR Engine:** You must install Tesseract on your system for the OCR to function.
    * *Windows:* Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
    * *Note:* Ensure you add Tesseract to your system's `PATH`, or update the executable path inside `src/ocr_engine.py`.

### 2. Clone the Repository

git clone [https://github.com/YourUsername/AirWritingProject.git](https://github.com/YourUsername/AirWritingProject.git)
cd AirWritingProject




3. Setup Virtual Environment
python -m venv venv
 Windows:
.\venv\Scripts\activate
 Mac/Linux:
source venv/bin/activate

4. Install Dependencies
Due to specific Protocol Buffer requirements with MediaPipe on Windows, please install the exact versions listed below:
Bash
pip install opencv-python mediapipe==0.10.9 protobuf==3.20.3 numpy pytesseract
🚀 Usage
Run the main application:
python main.py
 screenshot of working
<img width="1536" height="1024" alt="Hide face with stick" src="https://github.com/user-attachments/assets/5919176c-56c4-461c-a739-04205a0326de" />
