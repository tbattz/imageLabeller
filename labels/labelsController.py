import dearpygui.dearpygui as dpg
from labels.labelsModel import AllLabelData
from labels.labelsView import LabelsView


class LabelsController:
    def __init__(self, config, viewParent):
        self.config = config
        self.viewParent = viewParent

        # Create data store
        self.imageLabelData = AllLabelData(labelTypeList=config['labelItems'])

        # Create view
        self.labelsView = LabelsView(parent=self.viewParent, listBoxWidth=258, numItems=30, labelItems=self.imageLabelData.labelTypeList)

        # Set callbacks
        dpg.set_item_callback(self.labelsView.addBtn, self.addLabelCallback)
        dpg.set_item_callback(self.labelsView.delBtn, self.removeLabelCallback)


    def addLabelCallback(self, sender, data):
        # Update data
        selectorValue = dpg.get_value(self.labelsView.labelCombo)
        if selectorValue == 'Car 3D':
            labelName = selectorValue + '-%i' % self.imageLabelData.labelCounts[selectorValue]
            self.imageLabelData.add3DBoxLabel(selectorValue, labelName, [[0,0],[1,1],[2,2],[3,3]])
        else:
            labelName = selectorValue + '-%i' % self.imageLabelData.labelCounts[selectorValue]
            self.imageLabelData.add2DBoxLabel(selectorValue, labelName, [[0, 0], [1, 1], [2, 2], [3, 3]])

        # Update view
        newItemList = [item.labelName for item in self.imageLabelData.labels]
        self.labelsView.updateLabelListView(newItemList)

    def removeLabelCallback(self, sender, data):
        # Get current list selection
        listBoxValue = dpg.get_value(self.labelsView.labelListBox)
        currLabels = [item.labelName for item in self.imageLabelData.labels]

        if len(currLabels) > 0:
            currInd = currLabels.index(listBoxValue)
            if currInd > 0:
                nextVal = currLabels[currInd-1]
                dpg.configure_item(self.labelsView.labelListBox, default_value=nextVal)

            # Update data
            self.imageLabelData.deleteLabelByName(listBoxValue)

            # Update view
            newItemList = [item.labelName for item in self.imageLabelData.labels]
            self.labelsView.updateLabelListView(newItemList)

    def handleWindowResize(self, newSize):
        self.labelsView.handleWindowResize(newSize)


