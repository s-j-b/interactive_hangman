
"""
NAMES: Simon J. Bloch and Gibson R. Cook
DATE: 3-10-2015

PROGRAM: HANGMAN - Projects an interactive hangman game. Responsive to user drawn-letters
"""



import numpy as np
import cv2
from time import *
from copy import copy
from cvk2 import*
from os import listdir
import random

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
    
    playGame(cam,proj,win,h,w,H,test)
    
    # When everything done, release the capture
    cam.release()
    cv2.destroyAllWindows()



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # #         GAMEPLAY FUNCTIONS         # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



    
                
 # playGame - Plays through one game of Hangman
 #
 # TAKES: nothingYET
 #
 # RETURNS: nothing
 #
def playGame(cam,proj,win,h,w,H,test):
     
    #get the main word for the game
    word = getWord()
     
    length = len(word)
     
     
    #Initialize the letter input square
    sqRad = h/12
    sqCent = (w/2,9*h/10)
    pa=(sqCent[0]-sqRad,sqCent[1]-sqRad)
    pb=(sqCent[0]+sqRad,sqCent[1]+sqRad)
    
    
    #draw the hangman gameboard
    #drawBoard returns:
    #   -The location of all of the master word's letters
    #   -The locations of every letter in the alphabet
    letterSpots,alphLocations = drawBoard(proj,win,h,w,length,sqRad,sqCent)
    
    #Initialize list of guessed letters
    guessed = []
     
    #Get guesses until loss or victory
    fails = 0
    while (fails <= 6):
     
        #Y component of word
        wordY = sqCent[1]-12*sqRad/7
        
        #new display word
        updatedword = displayWord(word,guessed,letterSpots,proj,win,wordY)
         
        #if user guesses word successfully
        if (updatedword == list(word)):
            removePrompt(proj,pa,pb,w,h)
            txt = "!!You win!"
            displayPrompt(txt,proj,pa,pb,h)
            break
    
        removePrompt(proj,pa,pb,w,h)
        displayPrompt("<--Please wait",proj,pa,pb,h)
    
        #get letter from the user
        guess = getLetter(proj,cam,H,pa,pb,win,w,h,test)
    
        removeText(proj,alphLocations)
    
    
        # Checking that the letter hasn't been guessed before
        if(guess in guessed):
            
            removePrompt(proj,pa,pb,w,h)
            displayPrompt("<--Guessed already",proj,pa,pb,h)
         
        else:
            letterMatch = checkGuess(word,guess)
            
            removeLetter(proj,alphLocations,guess)
            
            if (letterMatch):
                guessed.append(guess)
            
                displayText("MATCHED",proj,alphLocations)
             
             
            else:
                fails += 1
                drawBody(fails, proj, (h/3-h/40,h/3+h/13), h/2)
                guessed.append(guess)
                displayText("MISSED",proj,alphLocations)

    if fails > 6:
        removePrompt(proj,pa,pb,w,h)
        txt = "You lose!"
        displayPrompt(txt,proj,pa,pb,h)

    guessed = list(word)
    updatedword = displayWord(word,guessed,letterSpots,proj,win,wordY)

    cv2.imshow(win,proj)
    cv2.waitKey(1)



    i = 0
    max=400
    while i<max:
        if i % 40 == 0:
            displayPrompt(txt,proj,pa,pb,h)
        elif i % 20 == 0:
            removePrompt(proj,pa,pb,w,h)

        cv2.imshow(win,proj)
        cv2.waitKey(1)
        i+=1

    return

# getWord - Get a random word from the dictionary
#           This word will become the object of the Hangman game
#
# TAKES: nothing
#
# RETURNS: The all-caps word for hangman
#
def getWord():
    # Importing a library of the 1000 most common english words
    # These contain no apostrophes
    allWords = open('words.txt')
    allWords = allWords.read()
    allWords = allWords.splitlines()
    
    # randomly pick a number in the range
    randNum = random.randint(0, 998)
    
    # return the uppercase form of the word at that position
    return allWords[randNum].upper()


# checkGuess - Checks whether a guessed letter is in the word
#
# TAKES: The master word and the guessed letter
#
# RETURNS: Whether the letter is in the word
#
def checkGuess(word,guess):
    
    word = list(word)
    
    for letter in word:
        if guess == letter:
            # guessed letter is in word
            return True
    # guessed letter not in word
    return False



# displayWord - Displays the "discovered" letters so far
#
# TAKES: The word and the guessed letters
#
# RETURNS: The word to be displayed
#
def displayWord(word,guessed,letterSpots,proj,win,wordY):
    
    word = list(word)
    
    fontScale = (letterSpots[0][1] - letterSpots[0][0])/16
    
    #Initialize blank display
    display = list(len(word)*' ')
    
    #Check for found letters in the word
    for i in range(len(word)):
        if word[i] in guessed:
            display[i] = word[i]
            
            
            cv2.putText(proj, word[i], (letterSpots[i][0],wordY), cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale, (0,0,0))



    # return the in-progress word
    return display



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # #         DISPLAY FUNCTIONS         # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def displayPrompt(text,proj,pa,pb,h):
    
    botLeft = (pb[0]+h/14,pb[1])
    
    cv2.putText(proj, text, botLeft, cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 3)


def removePrompt(proj,pa,pb,w,h):
    
    botLeft = (pb[0]+h/14,h)
    topRight = (w,pa[1])
    proj[topRight[1]:h,botLeft[0]:topRight[0]] = 255*np.ones((h-topRight[1],topRight[0]-botLeft[0]), dtype='uint8')



def displayText(text,proj,alphLocations):

    lWid = alphLocations["B"][0]-alphLocations["A"][0]
    lHei = alphLocations["I"][1]-alphLocations["A"][1]

    #bottom left corner of text block
    botLeft = (alphLocations["Z"][0]+3*lWid,alphLocations["Z"][1]+lHei)
    
    cv2.putText(proj, text, botLeft, cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 3)
                 

def removeText(proj,alphLocations):
    
    lWid = alphLocations["B"][0]-alphLocations["A"][0]
    lHei = alphLocations["I"][1]-alphLocations["A"][1]
    
    pt = alphLocations["Z"]
    
    proj[pt[1]:pt[1]+11*lHei/10,pt[0]+lWid:pt[0]+7*lWid] = 255*np.ones((11*lHei/10, 6*lWid), dtype='uint8')



def removeLetter(proj,alphLocations,guess):

    lWid = alphLocations["B"][0]-alphLocations["A"][0]
    lHei = alphLocations["I"][1]-alphLocations["A"][1]

    pt = alphLocations[guess]
    
    proj[pt[1]:pt[1]+lHei,pt[0]:pt[0]+lWid] = 255*np.ones((lHei, lWid), dtype='uint8')



# drawBoard - Draws the gallows, alphabet, and master word spots on the board
#
# TAKES: The main projected image and board dimensions/object specifics
#
# RETURNS: The locations of all the letters in the word, AND the locations of
#          alphabet letters
#
def drawBoard(proj,win,h,w,numLetters,sqRad,sqCent):
    
    #corners of the alphabet rectangle
    alphTR = (w-h/15,h/15)
    alphBL = (alphTR[0]-2*w/5,alphTR[1]+2*h/5)
    
    letterDict = drawAlph(proj,h,w,alphTR,alphBL)
    
    #bottom edge, for use in drawLines
    alphBottomEdge = alphTR[1]+2*h/5
    
    #draw the alphabet rectangle
    cv2.rectangle(proj, alphTR, alphBL, (0,0,0), 4)
    
    #draws gallows, and saves right edge for use in drawLines
    gallowsRightEdge = drawGallows(proj,h,w)+w/12
    
    #top of user input square, for use in drawLines
    sqTop = sqCent[1]-3*sqRad/2
    
    #right wall, for use in drawLines
    rightEdge = w-h/15
    
    #draws word lines and saves letter addresses
    letterSpots = drawLines(proj,h,w,alphBottomEdge,gallowsRightEdge,sqTop,rightEdge,numLetters)
    
    return (letterSpots,letterDict)







# drawAlph - Draws the alphabet on the board
#
# TAKES: The main projected image, board dimensions, and alphabet box
#
# RETURNS: The right edge position of the gallows for later use in drawLines
#
def drawAlph(proj,h,w,alphTR,alphBL):
    
    #read image and normalize it
    alphabet = cv2.imread('alphabet.png',cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    
    
    alphabet = cv2.threshold(alphabet, 50, 255, cv2.THRESH_BINARY)[1]
    
    alphabet = cv2.resize(alphabet, (alphTR[0]-alphBL[0],alphBL[1]-alphTR[1]))
    
    #position and write gallows over the original image
    xOffset = alphBL[0]+3
    yOffset = alphTR[1]+3
    
    proj[yOffset:yOffset+alphabet.shape[0],xOffset:xOffset+alphabet.shape[1]] = alphabet
    
    lWid = (alphTR[0]-alphBL[0])/8-4
    lHei = (alphBL[1]-alphTR[1])/4-4
    
    letterDict = {}
    
    alphIndex = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    
    for i in range(26):
        displacement=0
        if i%8>3:
            displacement=lWid/2
        letterDict[alphIndex[i]] = (xOffset+(i%8)*lWid+displacement,yOffset+(i/8)*lHei)
    
    
    return letterDict



# drawGallows - Draws the gallows on the board
#
# TAKES: The main projected image and board dimensions
#
# RETURNS: The right edge position of the gallows for later use in drawLines
#
def drawGallows(proj,h,w):
    
    #read image and normalize it
    gallows = cv2.imread('gallows2.png',cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    gallows = cv2.threshold(gallows, 50, 255, cv2.THRESH_BINARY)[1]
    
    galHeight = gallows.shape[1]
    
    heightRatio = 1.0*h/galHeight
    
    gallows = cv2.resize(gallows, (w/5,2*h/3))
    
    #position and write gallows over the original image
    xOffset = h/20
    yOffset = h/4
    
    proj[yOffset:yOffset+gallows.shape[0],xOffset:xOffset+gallows.shape[1]] = gallows
    
    #return the right edge of the shown gallows image
    return xOffset+gallows.shape[1]



# drawLines - Draws the letter spots for the the main hangman word on the board
#
# TAKES: The main projected image, important board specific values, and the number
#        of letters
#
# RETURNS: A list of the addresses of all the letters in the main word
#
def drawLines(proj,h,w,top,left,bottom,right,numL):
    
    #free space
    s = right-left
    
    #special constant for calculating letter width (see README for details)
    n = (numL-1)/3.0+numL
    
    #array of letter addresses for later gameplay use
    letterSpots = []
    
    #if letters will fill free space
    if numL >= 6:
        
        #width of one letter in pixels
        letterWidth = int(s/n)
        
        #width of one space
        spaceWidth = letterWidth/3
        
        #for every letter, compute left and right edge, and draw line in place
        for i in range(numL):
            
            leftEdge = left+i*(letterWidth+spaceWidth)
            
            rightEdge = leftEdge + letterWidth
            
            cv2.line(proj, (leftEdge,bottom), (rightEdge,bottom), (0,0,0),4)
            
            #add location of letter to the list.
            letterSpots.append((leftEdge,rightEdge))

    #if letters will NOT fill free space
    else:
    
        n = 5/3.0+6
        
        letterWidth = int(s/n)
        
        spaceWidth = letterWidth/3
        
        extra = s - ((numL)*(letterWidth+spaceWidth)-spaceWidth)
        
        #for every letter, compute left and right edge, and draw line in place
        for i in range(numL):
            
            leftEdge = left+extra/2+i*(letterWidth+spaceWidth)
            
            rightEdge = leftEdge + letterWidth
            
            cv2.line(proj, (leftEdge,bottom), (rightEdge,bottom), (0,0,0),4)
            
            #add location of letter to the list.
            letterSpots.append((leftEdge,rightEdge))

    #return that list of all the letter locations
    return letterSpots


def drawBody(failNumber, proj, noosePoint, Hgallows):
    
    # Thickness and color for hangman lines
    thickness = 6
    color = (0,0,0)
    
    # Defining the proporions of the hanged man
    htotal = Hgallows
    w = htotal/2
    hHead = Hgallows/5
    hNeck = hHead/2
    hTorso = Hgallows/4
    hLeg = Hgallows/4
    
    # Key Points
    headCenter = (noosePoint[0],noosePoint[1]+hHead/2)
    neckTop = (noosePoint[0],noosePoint[1]+hHead)
    neckBottom = (noosePoint[0],noosePoint[1]+hHead+hNeck)
    torsoBottom = (neckBottom[0],neckBottom[1]+hTorso)
    leftHand = (noosePoint[0]-w/2, neckTop[1])
    rightHand = (noosePoint[0]+w/2, neckTop[1])
    leftFoot = (noosePoint[0]-w/3, torsoBottom[1]+hLeg)
    rightFoot = (noosePoint[0]+w/3, torsoBottom[1]+hLeg)
    
    if failNumber == 0:
        return False
    
    elif failNumber == 1:
        # draw head
        cv2.circle(proj, headCenter, hHead/2, color, thickness)
    
    elif failNumber == 2:
        # draw neck
        cv2.line(proj, neckTop, neckBottom, color, thickness)
    
    elif failNumber == 3:
        # draw left arm
        cv2.line(proj, neckBottom, leftHand, color, thickness)
    
    elif failNumber == 4:
        # draw right arm
        cv2.line(proj, neckBottom, rightHand, color, thickness)
    
    elif failNumber == 5:
        # draw torso
        cv2.line(proj, neckBottom, torsoBottom, color, thickness)
    
    elif failNumber == 6:
        # draw left leg
        cv2.line(proj, torsoBottom, leftFoot, color, thickness)
    
    elif failNumber == 7:
        # draw right leg
        cv2.line(proj, torsoBottom, rightFoot, color, thickness)
    
    return True







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # #         CHARACTER RECOGNITION FUNCTIONS         # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



# getLetter - Gets a user input letter and returns the user's guess
#
# TAKES: display specific parameters, the camera, the homography, and the window
#
# RETURNS: the guessed letter
#
def getLetter(proj,cam,H,pa,pb,win,w,h,test):
    
    letterPic = getLetterPic(proj,cam,H,pa,pb,win,w,h,test)

    letter = matchLetter(letterPic)

    return letter
                 
                 
    
# matchLetter - Find the letter that the input image matches to
#
# TAKES: picture of letter
#
# RETURNS: the char of best match
#
def matchLetter(letterPic):
    
    #read in database of letters 
    library = listdir("./TIKI2")
    
    #remove irrelevant file from list
    library.remove(".DS_Store")
    
    template = letterPic
    
    #compare template with every picture in library, and save score
    scores = []
    for element in library:
        #read the image
        image = cv2.imread('TIKI2/'+element)
        image = cv2.split(image)[0]
        
        #match the image with the template, output should be a single pixel
        #the value of the pixel is the score for that match
        m = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
        score = m[0][0]
    
        #save this score
        scores.append(score)
    
    #find the filename corresponding to the best match
    best = library[scores.index(max(scores))]

    #return the char letter that the input picture best matched to
    return best[0]

        

# normalizeLetter - Transform image into 100x100 square with no
#                   empty space around letter
#
# TAKES: original image
#
# RETURNS: the normalized image
#
def normalizeLetter(original):
    
    test = 'test'
    cv2.namedWindow(test)
    cv2.moveWindow(test, 950, 0)
    
    #gets all nonzero pixels in image
    whitePix = np.nonzero(original)
    
    #corner points of what will be the bounding box
    imptPts = []
    
    #get limits to nonzero pixels in image
    xMax = max(whitePix[0])
    xMin = min(whitePix[0])
    yMax = max(whitePix[1])
    yMin = min(whitePix[1])
    
    #find points around bounding box
    imptPts.append([[xMin,yMin]])
    imptPts.append([[xMin,yMax]])
    imptPts.append([[xMax,yMin]])
    imptPts.append([[xMax,yMax]])
    
    #crop to contain ONLY nonzero pixels
    cropped = original[xMin:xMax, yMin:yMax]
    
    #resize
    final = cv2.resize(cropped, (100, 100))

    return final



# getLetterPic - Get a normalized, user-drawn, picture of a letter guess
#
# TAKES: Specific dimensions, homography
#
# RETURNS: A normalized picture of the user's letter guess
#
def getLetterPic(proj,cam,H,pa,pb,win,w,h,test):

    #Homography test display
    ret, testIm = cam.read()
    testIm = cv2.warpPerspective(testIm, H[0], (w,h))
    testIm = cv2.resize(testIm, (w/5,h/5))
    cv2.imshow(test,testIm)
    cv2.waitKey(20)
    
    #Get full stable image of board with letter
    letterWithBorder = getStableImage(cam,H,proj,win,w,h,pa,pb,test)
    
    

    
    #squeeze in box of nonzero pixels, and scale so letter fits in 100X100px box
    letterToID = normalizeLetter(letterWithBorder)

    return letterToID


# getStableImage - Get a stable image with a drawn letter guess and return it
#
# TAKES: Specific dimensions (including UI box), and the homographies
#
# RETURNS: a stable thresholded image with the letter in it
#
def getStableImage(cam,H,proj,win,w,h,pa,pb,test):

    #structuring element for later erosion
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19))
    
    e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    
    cv2.rectangle(proj, pa, pb, (200,200,200), 4)

    #Display plain image
    cv2.imshow(win,proj)
    cv2.waitKey(15)
    
    #establish background
    i=0
    while i<15:
        ret, bg = cam.read()
        i+=1
    #map the background to the "computer" perspective
    bg = cv2.warpPerspective(bg, H[0], (w,h))

    background = bg[0:h,2*w/5:3*w/5]

    removePrompt(proj,pa,pb,w,h)
    displayPrompt("<-- Write letter",proj,pa,pb,h)

    cv2.imshow(win,proj)
    cv2.waitKey(5)

    #We don't leave the loop until:
    #   -We've drawn something
    #   -We've achieved stability
    drawn = False
    stable = False
    while not (stable and drawn):
        for i in range(5):
            # Capture frame-by-frame
            ret, im= cam.read()
    
        #transform the image so it fits to just the display window
        im = cv2.warpPerspective(im, H[0], (w,h))

        image = im[0:h,2*w/5:3*w/5]

        #initialize and compute the difference image between the background
        diff = image.copy()
        cv2.absdiff(background, image, diff)

        #Binarize and erode image.
        bW = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        bin = cv2.threshold(bW, 75, 255, cv2.THRESH_BINARY)[1]
        final = cv2.erode(bin,k)
        final= cv2.split(final)[0]

        #get the contours in the cleaned up absdiff image
        contours = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_TC89_KCOS)

        #Check to see if we've drawn anything
        if not drawn:
            if contours[0]:
                drawn = True

        #If we think we've drawn something, start waiting for stability
        else:
            #if we're stable, make sure something got drawn
            if not contours[0]:
                
                letterSq = im[pa[1]+3:pb[1]-3,pa[0]+3:pb[0]-3]

                clean = cleanCamImage(letterSq)


                empty = testEmptyPix(clean)

                if empty:
                    
                    drawn = False
                
                else:
                    stable = True


    #erase rectangle so we just have clean image with the now drawn letter
    cv2.rectangle(proj, pa, pb, (255,255,255), 4)

    removePrompt(proj,pa,pb,w,h)
    displayPrompt("<--Step away",proj,pa,pb,h)


    #Display image and capture
    cv2.imshow(win,proj)
    cv2.waitKey(10)
    
    i=0
    while i<10:
        ret, image = cam.read()
        i+=1

    #Format image with letter and return
    fullImage = cv2.warpPerspective(image, H[0], (w,h))

    colorLetter = fullImage[pa[1]+3:pb[1]-3,pa[0]+3:pb[0]-3]

    binLetter = cleanCamImage(colorLetter)

    return binLetter

def cleanCamImage(camIm):
    bW3C= cv2.cvtColor(camIm, cv2.COLOR_RGB2GRAY)
    bW = cv2.split(bW3C)[0]
    
    
    #Binarize and eliminate everything but the picture of the letter
    binImage = cv2.adaptiveThreshold(bW, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 5)




    e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    
    border = cv2.erode(binImage,e)
    border = cv2.dilate(border,d)
    
    cv2.threshold(border,10,255,cv2.THRESH_BINARY,border)

    return border


def testEmptyPix(binLetter):

    e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    
    eroded = cv2.erode(binLetter,e)
    final = cv2.dilate(eroded,d)
    
    cv2.threshold(final,10,255,cv2.THRESH_BINARY,final)
    
    #gets all nonzero pixels in image
    whitePix = np.nonzero(final)



    if len(whitePix[0])>600:
        #not empty
        return False

    else:
        #empty
        return True





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # #         HOMOGRAPHY FUNCTIONS        # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




# getProjPts - makes a list of the projected points for findHomog, and
#              returns in iterable form and numpy array form
#
# TAKES: the camera input, the blank display, the window, and the dimensions
#
# RETURNS: the homography from computer to live and vice-versa
#
def findHomog(cam,white,win,h,w):
    
    #blank copy on which points will be drawn
    img = white.copy()
    
    #compPts - Projected points
    compPts = np.zeros((12,2), dtype=np.float32)
    #livePts - Camera recognized points
    livePts = np.zeros((12,2), dtype=np.float32)
    
    #make grid of 12 projected points
    compPts, compPtsTupl = getProjPts(w,h,compPts)
    
    #Display plain image
    cv2.imshow(win,white)
    cv2.waitKey(5)
    
    #establish background
    i=0
    while i<60:
        # Capture frame-by-frame
        ret, background = cam.read()
        i+=1

    #Iterate through each of the 12 points and extract perceived pixel address
    #Save these points in livePts
    ind=0
    for pt in compPtsTupl:
        
        #draw black circle
        cv2.circle(img, pt, 16, (0,0,0), -1, cv2.CV_AA )
        cv2.imshow(win,img)
        cv2.waitKey(100)
        
        #read drawn point image
        i=0
        while i<10:
            # Capture frame-by-frame
            ret, pointIm = cam.read()
            i+=1

        #get the center of the drawn black dot
        contPoint = getPointFromImage(pointIm,background)
    
        #fill in next point address in list
        livePts[ind][0]=contPoint[0]
        livePts[ind][1]=contPoint[1]

        #cover up that circle
        cv2.circle(img, pt, 40, (255,255,255), -1, cv2.CV_AA )

        ind+=1

    #Use points to get the homography matrix and its reverse
    H2C = cv2.findHomography(livePts, compPts, 0)
    H2L = cv2.findHomography(compPts, livePts, 0)

    #return both H matrices
    H = [H2C[0],H2L[0]]
    return H



# getProjPts - makes a list of the projected points for findHomog, and
#              returns in iterable form and numpy array form
#
# TAKES: image dimensions and empty numpy array
#
# RETURNS: list of homography calibration points in tuple list and array form
#
def getProjPts(w,h,cPts):
    
    #initialize array of points in tuple format
    cPtsTupl = []
    
    #Establishing the grid of projected points (will become compPts)
    ind = 0
    for i in range(w/10,w,w/3-(w/10)):
        for j in range(w/10,h,h/2-(w/10)):
            cPts[ind][0]=1.0*i
            cPts[ind][1]=1.0*j
            cPtsTupl.append((i,j))
            ind+=1
    #return both list of points in both format
    return cPts,cPtsTupl



# getPointFromImage - returns the pixel address of the center of a displayed point
#
# TAKES: image WITH the drawn point and background WITHOUT the drawn point
#
# RETURNS: the pixel address of the drawn point
#
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
    
    #returns the pixel address of the displayed point
    contPoint = getCenterPoint(contours[0])
    return contPoint



# getContourPoint - returns the center of mass of a shape, for use in findHomography
#
# TAKES: list of contours
#
# RETURNS: the center of mass of the largest shape in the contour list
#
def getCenterPoint(contours):
    
    #list of the centers of every contour
    cPoints = []
    
    #list of the areas of every contour
    cAreas = []
    
    #get data for the above lists
    for contour in contours:
        s00 = cv2.moments(contour)['m00']
        if (s00==0.0):
            s00 += .0001
    
        # Compute info for contour.
        info = getcontourinfo(contour,s00)
        
        mapPt = a2ti(info['mean'])
        
        #add contour data to lists
        cPoints.append(mapPt)
        cAreas.append(s00)

    #get the index of the shape with largest area
    circIndex = cAreas.index(max(cAreas))

    #return the center of mass of that shape
    return cPoints[circIndex]





main()



