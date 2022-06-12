import dearpygui.dearpygui as dpg
from labels.labelsModel import AllLabelData
from labels.labelsView import LabelsView
from imageDisplay.imageView import ImageDisplayView
from imageDisplay.imageModel import ImageListModel
import json


class MainWindowController:
    def __init__(self):
        winDims = [1200, 800]
        self.modeDict = {'WAITING': 0, 'NEW_LABEL': 1, 'FIRST_CLICK': 2, 'FURTHER_CLICKS': 3}
        self.mode = self.modeDict['WAITING']

        dpg.create_context()
        dpg.create_viewport(title='Image Labeller', width=winDims[0], height=winDims[1], min_width=1, min_height=1)

        # Load config file
        self.config = json.load(open('config.json', 'r'))
        self.imgDir = self.config['imgDir']
        self.heightOffset = 35 * 2

        # Create main window
        self.mainWindow = dpg.add_window(tag="Main")
        dpg.set_viewport_height(700)
        dpg.set_viewport_width(1000)

        # Create horizontal group
        self.horzGroup = dpg.add_group(horizontal=True, parent=self.mainWindow)

        # ===== Labels ===== #
        # Create label data store
        self.imageLabelData = AllLabelData(labelTypeList=self.config['labelItems'])

        # Create labels view
        self.labelsView = LabelsView(parent=self.horzGroup, listBoxWidth=258, numItems=30, labelItems=self.imageLabelData.labelTypeList)

        # ===== Image Display ===== #
        # Create data store
        self.imageListModel = ImageListModel(self.imgDir)

        # Create view
        self.imageDisplayView = ImageDisplayView(parent=self.horzGroup)

        # Load first image
        plotHeight = dpg.get_viewport_height() - self.heightOffset
        self.imageDisplayView.setLoadedImage(self.imageListModel.getCurrentImage(), self.imageListModel.ind + 1, len(self.imageListModel.imageList))
        self.imageDisplayView.reinitPlot(plotHeight)


        # Set callbacks
        dpg.set_item_callback(self.labelsView.addBtn, self.addLabelCallback)
        dpg.set_item_callback(self.labelsView.delBtn, self.removeLabelCallback)
        dpg.set_item_callback(self.imageDisplayView.prevBtn, self.prevImageCallback)
        dpg.set_item_callback(self.imageDisplayView.nextBtn, self.nextImageCallback)
        with dpg.handler_registry() as double_click_reg:
            dpg.add_key_press_handler(key=dpg.mvKey_Left, callback=self.leftArrowCallback)
            dpg.add_key_press_handler(key=dpg.mvKey_Right, callback=self.rightArrowCallback)
            dpg.add_mouse_click_handler(callback=self.handleMouseClick)

        # Fix startup sizes
        dpg.set_viewport_resize_callback(self.resizeViewportCallback)
        self.handleWindowResize([dpg.get_viewport_width(), dpg.get_viewport_height()], dpg.get_viewport_width(),
                                dpg.get_viewport_height())



    def resizeViewportCallback(self, sender, data):
        data = dpg.get_item_rect_size("Main")
        # Extra margin needed as current size is delayed if user moves the mouse too quickly
        maxWidth = data[0] - self.labelsView.listBoxWidth - 50
        maxHeight = data[1] - (35*2)
        self.handleWindowResize(data, maxWidth, maxHeight)

    def addLabelCallback(self, sender, data):
        # Update data
        selectorValue = dpg.get_value(self.labelsView.labelCombo)
        if selectorValue == 'Car 3D':
            labelName = selectorValue + '-%i' % self.imageLabelData.labelCounts[selectorValue]
            labelType = '3D'
            xys = [[0, 0], [100, 0], [100, 100], [0, 100]]
            self.imageLabelData.add3DBoxLabel(selectorValue, labelName, xys)
        else:
            labelName = selectorValue + '-%i' % self.imageLabelData.labelCounts[selectorValue]
            labelType = '2D'
            xys = [[0, 0], [100, 0], [100, 100], [0, 100]]
            self.imageLabelData.add2DBoxLabel(selectorValue, labelName, xys)

        # Update label view
        newItemList = [item.labelName for item in self.imageLabelData.labels]
        self.labelsView.updateLabelListView(newItemList)

    def removeLabelCallback(self, sender, data):
        # Get current list selection
        listBoxValue = dpg.get_value(self.labelsView.labelListBox)
        currLabels = [item.labelName for item in self.imageLabelData.labels]

        if len(currLabels) > 0:
            currInd = currLabels.index(listBoxValue)
            if currInd > 0:
                nextVal = currLabels[currInd - 1]
                dpg.configure_item(self.labelsView.labelListBox, default_value=nextVal)

            # Update data
            self.imageLabelData.deleteLabelByName(listBoxValue)

            # Update view
            newItemList = [item.labelName for item in self.imageLabelData.labels]
            self.labelsView.updateLabelListView(newItemList)


    def handleMouseClick(self, sender, data):
        print(dpg.get_plot_mouse_pos())

    def handleWindowResize(self, data, maxWidth, maxHeight):
        self.labelsView.handleWindowResize(data)
        self.imageDisplayView.handleWindowResize(maxWidth, maxHeight)

    def prevImageCallback(self, sender, data):
        newImage = self.imageListModel.getPrevImage()
        plotHeight = dpg.get_viewport_height() - self.heightOffset
        self.imageDisplayView.setLoadedImage(newImage, self.imageListModel.ind+1, len(self.imageListModel.imageList))
        self.imageDisplayView.reinitPlot(plotHeight)

    def nextImageCallback(self, sender, data):
        newImage = self.imageListModel.getNextImage()
        plotHeight = dpg.get_viewport_height() - self.heightOffset
        self.imageDisplayView.setLoadedImage(newImage, self.imageListModel.ind+1, len(self.imageListModel.imageList))
        self.imageDisplayView.reinitPlot(plotHeight)

    def leftArrowCallback(self, sender, data):
        # Decrement image
        self.prevImageCallback(None, None)

    def rightArrowCallback(self, sender, data):
        # Increment image
        self.nextImageCallback(None, None)

    def addLabel(self, labelName, labelType, xys):
        self.imageDisplayView.addLabel(labelName, labelType, xys)



# Create main controller
mainWindowController = MainWindowController()


# Launch window
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()

