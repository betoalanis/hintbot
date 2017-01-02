import os
import skimage.io as io
# from sklearn.utils import shuffle
import numpy as np
import colorutils

inputImages = []
targetImages = []

# for each folder in datadir
# filter for images that have "@2x" in their name
# if the version without the @2x isn't present, ignore them
# add the large version of the image to the main data array
# and the small version of the image to the result array
def loadImages(datadir, maxDirectoryCount=10, split=0.9):
    for dirPath, dirNames, fileNames in os.walk(datadir):
        if (maxDirectoryCount != 0):
            fullSizeFileNames = [fileName for fileName in fileNames if fileName.endswith("@2x.png") and (fileName.replace("@2x","") in fileNames)]
            for fullSizeFileName in fullSizeFileNames:
                inputImage = io.imread(dirPath + "/" + fullSizeFileName)
                targetImage = io.imread(dirPath + "/" + fullSizeFileName.replace("@2x",""))
                # print(dirPath + "/" + fullSizeFileName)
                inputSlices, targetSlices = sliceImages(inputImage, targetImage)
                # print("got", len(inputSlices), "input splices and",len(targetSlices),"targetSlices")
                inputImages.extend(inputSlices)
                targetImages.extend(targetSlices)
            maxDirectoryCount -= 1
    x, y = np.asarray(inputImages), np.asarray(targetImages)
    x_train = x[:int(len(x) * split)]
    y_train = y[:int(len(y) * split)]
    x_test = x[int(len(x) * split):]
    y_test = y[int(len(y) * split):]
    # Shuffle training data so that repeats aren't in the same batch
    # x_train, y_train = shuffle(x_train, y_train, random_state=0)
    return (x_train, y_train, x_test, y_test)

def sliceImages(inputImage, targetImage):
    inputSlices = []
    targetSlices = []
    sliceSize = 32
    for y in range(0,inputImage.shape[1]//sliceSize):
        for x in range(0,inputImage.shape[0]//sliceSize):
            inputSlice = inputImage[x*sliceSize:(x+1)*sliceSize,y*sliceSize:(y+1)*sliceSize]
            targetSlice = targetImage[x*sliceSize//2:(x+1)*sliceSize//2,y*sliceSize//2:(y+1)*sliceSize//2]
            # only add slices if they're not just empty space
            if (np.any(targetSlice)):
                # Reweight smaller sizes
                # for i in range(0,max(1,128//inputImage.shape[1])**2):
                inputSlices.append(inputSlice)
                targetSlices.append(targetSlice)
                # Augment data with flips
                inputSlices.append(np.fliplr(inputSlice))
                targetSlices.append(np.fliplr(targetSlice))
    # return two arrays of images in a tuple
    return (inputSlices, targetSlices)
