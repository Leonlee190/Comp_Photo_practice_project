import cv2 as cv
import numpy as np
import brush_color as fc

print("Welcome to the painterly rendering program.")
print("This program takes in a single image and renders it into a pointillism painterly way")
print("\n")
fileName = input('Enter in image name (Including the extension): ')

# Read in the source image
src = cv.imread(fileName)

if src is None:
    print("No image found. \nPlease restart the program with a correct photo.")

else:
    # Extract height and width of the image
    height, width = src.shape[:2]

    # Create blank canvas with the same source image size
    canvas = np.zeros((height, width, 3), np.uint8)

    # Initialize brush things
    brushList, lowestBrush = fc.brushCreate(width, height)
    numBrush = len(brushList)

    # Print image information
    print("Image name: " + str(fileName))
    print("Image width: " + str(width))
    print("Image height: " + str(height))
    print("Lowest brush radius: " + str(lowestBrush))

    # Iterate through all the brush sizes
    for i in range(len(brushList)):
        radius = int(brushList[i])

        # GaussianBlur function doesn't accept even number for some reason
        if radius % 2 == 0:
            radius = radius + 1

        # Color and Draw!
        canvas = fc.coloring(width, height, radius, lowestBrush, src, canvas, 0)

        # When it's the last coloring with smallest brush
        if i == (len(brushList) - 1):
            canvas = fc.coloring(width, height, radius, lowestBrush, src, canvas, 1)

        # To see the in between phases of the coloring
        if i == int(numBrush*0.25) or i == int(numBrush*0.75):
            cv.imwrite(str(fileName) + "_canvas" + str(i) + ".png", canvas)

    # see the final
    cv.imwrite(str(fileName) + "_canvas_finalized.png", canvas)