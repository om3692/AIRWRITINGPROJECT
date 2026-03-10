import cv2
import sys
from src.hand_tracker import HandDetector
from src.canvas import VirtualCanvas
from src.ocr_engine import OCREngine

def main():
    print("Initializing Air Writing System...")
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) 
    cap.set(4, 720)  
    
    window_name = "Air Writing Portfolio Project"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    
    detector = HandDetector(detection_con=0.8)
    canvas = VirtualCanvas(width=1280, height=720)
    ocr = OCREngine()
    
    predicted_text = ""

    while True:
        success, frame = cap.read()
        if not success:
            break
            
        frame = cv2.flip(frame, 1)
        
        frame = detector.find_hands(frame)
        lm_list = detector.find_position(frame)
        
        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1], lm_list[8][2]   
            
            fingers = detector.fingers_up(lm_list)
            
            # --- THE SIMPLIFIED STATE MACHINE ---
            
            # STATE 1: CLEAR ALL (Whole Palm / All Fingers UP)
            # We check if at least the 4 main fingers are up (thumb detection can sometimes be rigid)
            if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                canvas.clear()
                predicted_text = ""
                cv2.putText(frame, "CANVAS CLEARED", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
            # STATE 2: ERASER (Exactly 2 Fingers UP: Index and Middle)
            elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                cv2.circle(frame, (x1, y1), 40, (0, 0, 0), cv2.FILLED)
                cv2.circle(frame, (x1, y1), 40, (255, 255, 255), 2)
                canvas.add_point((x1, y1), color=(0, 0, 0), thickness=60)
                cv2.putText(frame, "ERASING", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # STATE 3: DRAWING (Exactly 1 Finger UP: Index)
            elif fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
                cv2.circle(frame, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
                canvas.add_point((x1, y1), color=(255, 0, 0), thickness=10)
                
            # STATE 4: HOVER / LIFT PEN (Any other gesture, e.g., closed fist)
            else:
                canvas.lift_pen()
                # Show a small pink dot so you still know where your cursor is
                cv2.circle(frame, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
                
        # Merge canvas with live frame
        frame = canvas.update_canvas(frame)
        
        # UI Overlays
        cv2.putText(frame, f"Prediction: {predicted_text}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "1 Finger=Draw | 2 Fingers=Erase | Palm=Clear | Fist=Hover", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow(window_name, frame)

        # --- BULLETPROOF WINDOW CLOSE FIX ---
        key = cv2.waitKey(1) & 0xFF
        
        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE) == -1:
                break
        except cv2.error:
            break

        # Keyboard Triggers
        if key == ord('s'): 
            print("Scanning Canvas...")
            predicted_text = ocr.predict(canvas.paint_window)
            print(f"Detected: {predicted_text}")
            
        elif key == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Application closed gracefully.")

if __name__ == "__main__":
    main()