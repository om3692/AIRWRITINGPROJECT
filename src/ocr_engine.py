import pytesseract
import cv2
import numpy as np
import sys

# WINDOWS CONFIGURATION
# Uncomment the line below and check the path if on Windows!
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCREngine:
    def __init__(self):
        # Whitelist: Only read numbers and uppercase letters
        self.config = '--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def predict(self, paint_window):
        # Preprocessing for robustness
        gray = cv2.cvtColor(paint_window, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        
        # Dilate to make strokes thicker
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        # Invert (Black text on White BG)
        inverted = cv2.bitwise_not(dilated)
        
        try:
            prediction = pytesseract.image_to_string(inverted, config=self.config)
            return prediction.strip()
        except Exception as e:
            return "Err"