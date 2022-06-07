import dearpygui.dearpygui as dpg
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
        self.imageDisplayView.setLoadedImage(self.imageListModel.getCurrentImage())

        # Setup callbacks
        dpg.set_item_callback(self.imageDisplayView.prevBtn, self.prevImageCallback)
        dpg.set_item_callback(self.imageDisplayView.nextBtn, self.nextImageCallback)


    def handleWindowResize(self, maxWidth, maxHeight):
        self.imageDisplayView.handleWindowResize(maxWidth, maxHeight)

    def prevImageCallback(self, sender, data):
        newImage = self.imageListModel.getPrevImage()
        self.imageDisplayView.setLoadedImage(newImage)

    def nextImageCallback(self, sender, data):
        newImage = self.imageListModel.getNextImage()
        self.imageDisplayView.setLoadedImage(newImage)



