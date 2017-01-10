
import numpy as np
import cv2
from time import *
from copy import copy
from cvk2 import*

# TODO:

# Print statements to prompt user for letter write
#

def main():
    #naming the window
    win = 'hangMan'
    test = 'test'
    
    #calling the named window
    cv2.namedWindow(win)
    
    cv2.namedWindow(test)
    cv2.moveWindow(test, 950, 0)

    
    #set the size (width or height) of the image
    h = 600
    w = 940
    
    cv2.resizeWindow(test, w/5, h/5)

    proj = 255*np.ones((h, w), dtype='uint8')
    
    cam = cv2.VideoCapture(0)

    H = findHomog(cam,proj,win,h,w)
    
    pa=(w/3,2*h/3)
    pb=(w/3+w/12,2*h/3+w/12)
    
    
    #draws that red rectangle, with thickness = 1 pixel
    cv2.rectangle(proj, pa, pb, (200,200,200), 4)

    
    letter = getLetter(proj,cam,H,pa,pb,win,w,h,test)

    #charLetter = analyze(letter)

    print "END"

    # When everything done, release the capture
    cam.release()
    cv2.destroyAllWindows()


def normalizeLetter(original):
    
    border = cv2.split(original)[0]
    
    whitePix = np.nonzero(border)
    
    
    imptPts = []
    
    xMax = max(whitePix[0])
    xMin = min(whitePix[0])
    yMax = max(whitePix[1])
    yMin = min(whitePix[1])
    
    imptPts.append([[xMin,yMin]])
    imptPts.append([[xMin,yMax]])
    imptPts.append([[xMax,yMin]])
    imptPts.append([[xMax,yMax]])
    
    cropped = original[xMin:xMax, yMin:yMax]
    
    
    final = cv2.resize(cropped, (100, 100))
    
    return final

def getLetter(proj,cam,H,pa,pb,win,w,h,test):
    
    #Homography test
    ret, testIm = cam.read()
    testIm = cv2.warpPerspective(testIm, H[0], (w,h))
    testIm = cv2.resize(testIm, (w/5,h/5))
    cv2.imshow(test,testIm)
    cv2.waitKey(20)
    
    #Get full stable image of board
    folder = "UNCLETIKI"
    i=176
    while True:
        fullImage = getStableImage(cam,H,proj,win,w,h,pa,pb)

        binImage = cv2.adaptiveThreshold(fullImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 5)

        letterWithBorder = binImage[pa[1]:pb[1],pa[0]:pb[0]]
    
        letter = normalizeLetter(letterWithBorder)
        
        cv2.imshow(win,letter)
        cv2.waitKey()
        
        name = folder+"/"+str(i)+".png"
        
        cv2.imwrite(name,letter)
    
        i+=1

    return letter

def getStableImage(cam,H,proj,win,w,h,pa,pb):
    
    cv2.rectangle(proj, pa, pb, (200,200,200), 4)
    
    #Proj is what we're projecting:
    #The current white background with a projected empty rectangle
    
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19))

    #Display plain image
    cv2.imshow(win,proj)
    cv2.waitKey(15)
    
    i=0
    while i<15:
        ret, background = cam.read()
        i+=1

    background = cv2.warpPerspective(background, H[0], (w,h))

    #Main booleans for this loop
    drawn = False
    stable = False

    while not (stable and drawn):
        for i in range(5):
            # Capture frame-by-frame
            ret, image= cam.read()
    
        image = cv2.warpPerspective(image, H[0], (w,h))

        diff = image.copy()
        cv2.absdiff(background, image, diff)

        #Binarize and erode image.
        bW = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        bin = cv2.threshold(bW, 75, 255, cv2.THRESH_BINARY)[1]
        final = cv2.erode(bin,k)
        final= cv2.split(final)[0]
        
        contours = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_TC89_KCOS)
        
        if not drawn:
            print "#"
            if contours[0]:
                drawn = True
        else:
            print "W"
            if not contours[0]:
                print "pizza."
                stable = True

    cv2.rectangle(proj, pa, pb, (255,255,255), 4)
    
    #Display plain image
    cv2.imshow(win,proj)
    cv2.waitKey(10)
    
    i=0
    while i<50:
        ret, image = cam.read()
        i+=1

    image = cv2.warpPerspective(image, H[0], (w,h))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image= cv2.split(image)[0]
    return image

def findHomog(cam,white,win,h,w):
    img = white.copy()
    
    #compPts - Projected points
    compPts = np.zeros((12,2), dtype=np.float32)
    #livePts - Camera recognized points
    livePts = np.zeros((12,2), dtype=np.float32)
    
    tuplPts = []
    
    #Establishing the projected points (compPts)
    ind = 0
    for i in range(w/10,w,w/3-(w/10)):
        for j in range(w/10,h,h/2-(w/10)):
            compPts[ind][0]=1.0*i
            compPts[ind][1]=1.0*j
            tuplPts.append((i,j))
            ind+=1

    #Display plain image
    cv2.imshow(win,white)
    cv2.waitKey(5)
    
    
    i=0
    while i<120:
        # Capture frame-by-frame
        ret, background = cam.read()
        i+=1

    ind=0
    for pt in tuplPts:
        cv2.circle(img, pt, 16, (0,0,0), -1, cv2.CV_AA )
        cv2.imshow(win,img)
        cv2.waitKey(300)
        
        i=0
        while i<10:
            # Capture frame-by-frame
            ret, pointIm = cam.read()
            i+=1

        contPoint = getPointFromImage(pointIm,background)
        
        livePts[ind][0]=contPoint[0]
        livePts[ind][1]=contPoint[1]
        
        ind+=1

        cv2.circle(img, pt, 40, (255,255,255), -1, cv2.CV_AA )

    print livePts
    print compPts
    H2C = cv2.findHomography(livePts, compPts, 0)
    H2L = cv2.findHomography(compPts, livePts, 0)


    H = [H2C[0],H2L[0]]
    return H

def getPointFromImage(pointIm,background):
    #initialize and make the absdiff image
    diff = pointIm.copy()
    cv2.absdiff(background, pointIm, diff)
    
    #threshold the absdiff image
    postThresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
    
    #split the output image so we can find contours
    finalIm= cv2.split(postThresh)[0]
    
    #get contours using Teh-Chin chain approximation algorithm
    contours = cv2.findContours(finalIm, cv2.RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_TC89_KCOS)
    
    
    contPoint = getContourPoint(contours[0])
    
    return contPoint

def getContourPoint(contours):
    cPoints = []
    cAreas = []
            
    for contour in contours:
        s00 = cv2.moments(contour)['m00']
        if (s00==0.0):
            s00 += .0001
    
        # Compute info for contour.
        info = getcontourinfo(contour,s00)
        
        mapPt = a2ti(info['mean'])
        
        cPoints.append(mapPt)
        cAreas.append(s00)
    circIndex = cAreas.index(max(cAreas))

    return cPoints[circIndex]

main()