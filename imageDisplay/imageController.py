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
        self.imageDisplayView.setLoadedImage(self.imageListModel.getCurrentImage(), self.imageListModel.ind+1, len(self.imageListModel.imageList))
        self.imageDisplayView.reinitDrawList(width=self.imageDisplayView.loadedImage.newWidth, height=self.imageDisplayView.loadedImage.newHeight)

        # Setup callbacks
        dpg.set_item_callback(self.imageDisplayView.prevBtn, self.prevImageCallback)
        dpg.set_item_callback(self.imageDisplayView.nextBtn, self.nextImageCallback)
        with dpg.handler_registry() as double_click_reg:
            dpg.add_key_press_handler(key=dpg.mvKey_Left, callback=self.leftArrowCallback)
            dpg.add_key_press_handler(key=dpg.mvKey_Right, callback=self.rightArrowCallback)


    def handleWindowResize(self, maxWidth, maxHeight):
        self.imageDisplayView.handleWindowResize(maxWidth, maxHeight)

    def prevImageCallback(self, sender, data):
        newImage = self.imageListModel.getPrevImage()
        self.imageDisplayView.setLoadedImage(newImage, self.imageListModel.ind+1, len(self.imageListModel.imageList))
        self.imageDisplayView.reinitDrawList(self.imageDisplayView.loadedImage.newWidth, self.imageDisplayView.loadedImage.newHeight)

    def nextImageCallback(self, sender, data):
        newImage = self.imageListModel.getNextImage()
        self.imageDisplayView.setLoadedImage(newImage, self.imageListModel.ind+1, len(self.imageListModel.imageList))
        self.imageDisplayView.reinitDrawList(self.imageDisplayView.loadedImage.newWidth, self.imageDisplayView.loadedImage.newHeight)

    def leftArrowCallback(self, sender, data):
        # Decrement image
        self.prevImageCallback(None, None)

    def rightArrowCallback(self, sender, data):
        # Increment image
        self.nextImageCallback(None, None)


