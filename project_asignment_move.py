import cv2
import os


video_path = "/Users/gimhuijun/Library/Mobile Documents/com~apple~CloudDocs/대학수업/2023_4_2/로봇비전/robot_visionProject/IMG_3390.mp4"
paused = False

def onMouse(evnet , x , y , flags, param):
    global paused
    if evnet == cv2.EVENT_LBUTTONDOWN:
        paused = not paused
        if paused:
            idx = 0
            while True:
                fileName = f'./robot_visionProject/paused_frame{idx}.png'
                if not os.path.exists(fileName):

                    cv2.imwrite(fileName, frame)
                    print(f'Frame sved to {fileName}')
                    break
                idx += 1
            
            

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()
    
cv2.namedWindow("Video")
cv2.setMouseCallback("Video",onMouse)

while True:
    if not paused:
        retval, frame = cap.read()
        if not retval:        
            print("Info: End of vide.")
            break
    
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(30) & 0xFF == 27:
        break
    
cap.release()
cv2.destroyAllWindows()