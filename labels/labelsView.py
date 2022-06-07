import dearpygui.dearpygui as dpg
import math



class LabelsView:
    def __init__(self, parent, listBoxWidth=150, numItems=30, labelItems=[]):
        self.parent = parent
        self.labelItems = labelItems
        self.listBoxWidth = listBoxWidth
        self.labelTypeComboWidth=150

        # Create left group for labels
        self.groupLeft = dpg.add_group(label="Left", parent=self.parent)
        dpg.add_text("Labels", parent=self.groupLeft)
        self.labelListBox = dpg.add_listbox(tag='labelsList', items=[], width=self.listBoxWidth, num_items=numItems, parent=self.groupLeft)
        self.labelFuncHorzGroup = dpg.add_group(horizontal=True, parent=self.groupLeft)
        self.addBtn = dpg.add_button(label="Add new label", tag="addLabelBtn", parent=self.labelFuncHorzGroup)
        self.labelCombo = dpg.add_combo(tag="labelTypeCombo", items=self.labelItems, width=self.labelTypeComboWidth, default_value=self.labelItems[0], parent=self.labelFuncHorzGroup)
        self.delBtn = dpg.add_button(label="Delete Label", parent=self.groupLeft)


    def handleWindowResize(self, newSize):
        # Set new label list box height
        newHeight = newSize[1]
        reservedH = 28*3
        remainH = newHeight - reservedH
        numItems = math.floor(remainH / 17.45)
        dpg.configure_item("labelsList", num_items=numItems)

    def updateLabelListView(self, itemList):
        dpg.configure_item(self.labelListBox, items=itemList)

