
import cv2
import numpy as np


win = 'hangMan'
    
    
#calling the named window
cv2.namedWindow(win)

cam = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()
        
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    # Display the resulting frame
    cv2.imshow(win,gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    if cv2.waitKey(1) & 0xFF == ord('g'):
        background = np.copy(gray)
        bool = True
        print "LEGGO"


cam.release()
cv2.destroyAllWindows()