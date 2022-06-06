import os
from imageDisplay.imageModel import ImageListModel
from imageDisplay.imageView import ImageDisplayView



class ImageController:
    def __init__(self, config, viewParent):
        self.config = config
        self.viewParent = viewParent
        self.imgDir = config['imgDir']

        # Create data store
        self.imageListModel = ImageListModel(self.imgDir)

        # Create view
        self.imageDisplayView = ImageDisplayView(parent=self.viewParent)

        # Load first image
        self.imageDisplayView.setLoadedImage(os.path.join(self.imgDir, self.imageListModel.getCurrentImage()))

    def handleWindowResize(self, maxWidth, maxHeight):
        self.imageDisplayView.handleWindowResize(maxWidth, maxHeight)



