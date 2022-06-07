import os



class ImageListModel:
    def __init__(self, directory):
        """
        Get a list of images in the given directory.

        :param directory: The directory to search through for images.
        """
        self.directory = directory
        self.imageList = []
        self.ind = 0

        self.findImages()

    def findImages(self):
        self.imageList = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if any([f.endswith(ext) for ext in ['.png', '.jpg']])]

        print('Found %i images' % len(self.imageList))

    def getNextImage(self):
        self.ind += 1
        if self.ind > len(self.imageList) - 1:
            self.ind = 0

        return self.imageList[self.ind]

    def getPrevImage(self):
        self.ind -= 1
        if self.ind < 0:
            self.ind = len(self.imageList) - 1

        return self.imageList[self.ind]

    def getCurrentImage(self):
        return self.imageList[self.ind]
