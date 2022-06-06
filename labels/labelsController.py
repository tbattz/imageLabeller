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


    def handleWindowResize(self, newSize):
        self.labelsView.handleWindowResize(newSize)


