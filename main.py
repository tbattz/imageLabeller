import dearpygui.dearpygui as dpg
from labels.labelsController import LabelsController
from imageDisplay.imageController import ImageController
import json


class MainWindowController:
    def __init__(self):
        winDims = [1200, 800]
        dpg.create_context()
        dpg.create_viewport(title='Image Labeller', width=winDims[0], height=winDims[1], min_width=1, min_height=1)

        # Load config file
        self.config = json.load(open('config.json', 'r'))

        # Create main window
        self.mainWindow = dpg.add_window(tag="Main")
        dpg.set_viewport_height(700)
        dpg.set_viewport_width(1000)

        # Create horizontal group
        self.horzGroup = dpg.add_group(horizontal=True, parent=self.mainWindow)

        # Create controllers
        self.labelController = LabelsController(self.config, viewParent=self.horzGroup)
        self.imageController = ImageController(self.config, viewParent=self.horzGroup)

        # Fix sizes
        dpg.set_viewport_resize_callback(self.resizeViewportCallback)
        self.labelController.handleWindowResize([dpg.get_viewport_width(), dpg.get_viewport_height()])


    def resizeViewportCallback(self, sender, data):
        self.labelController.handleWindowResize(data)
        data = dpg.get_item_rect_size("Main")
        # Extra margin needed as current size is delayed if user moves the mouse too quickly
        maxWidth = data[0] - self.labelController.labelsView.listBoxWidth - 50
        maxHeight = data[1] - (35*2)
        self.imageController.handleWindowResize(maxWidth, maxHeight)


# Create main controller
mainWindowController = MainWindowController()


# Launch window
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()

