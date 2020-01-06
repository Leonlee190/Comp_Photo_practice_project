import cv2 as cv
import numpy as np
import random
import math


# Initializing brush size and brush queue
# Smallest brush size depends on the size of the image
# Brush queue is scaled with the smallest brush size
def brushCreate(width, height):
    lowestBrush = int(math.sqrt((width * height) / 30000))
    numBrush = 20
    brushList = np.arange(1, numBrush, dtype=int)
    brushList = brushList * lowestBrush
    brushList[::-1].sort()

    return brushList, lowestBrush


# Coloring the canvas with the brush size
def coloring(width, height, radius, lowestBrush, src, canvas, status):
    # Apply Gaussian blur on the source image to smooth out the color transition
    reference = cv.GaussianBlur(src, (radius, radius), 0)

    if status == 0:
        # Random brush strokes are bigger before final refining
        diffMap = cv.subtract(reference, canvas)
        randSize = lowestBrush * 3
    else:
        # Last iteration with the smallest brush size
        # This allows the darker spot such as retina or shadows to be seen in the difference map
        # Random brush strokes are smaller during final refining
        diffMap = cv.subtract(canvas, reference)
        randSize = lowestBrush

    # Iterate through the difference map in radius + 1 steps to have a slight overlapping
    for x in range(0, width, (radius+1)):
        for y in range(0, height, (radius+1)):
            if x < width and y < height:
                # Give some randomness in randomness to create more rigidness
                xRand = random.randint(0, randSize)
                yRand = random.randint(0, randSize)

                # Extract color from the reference image
                tempColor = np.array(reference[y, x])
                red = tempColor[0]
                green = tempColor[1]
                blue = tempColor[2]

                # If the color difference threshold is passed
                if sum(diffMap[y, x]) > 3:
                    # Draw on the canvas with an ellipse with random radius
                    cv.ellipse(canvas, (int(x), int(y)), (int(radius + xRand), int(radius + yRand)), int(0), int(0),
                               int(360), (int(red), int(green), int(blue)), -1, cv.LINE_AA)

    return canvas