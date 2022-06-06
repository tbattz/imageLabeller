


class SingleLabelData:
    def __init__(self, labelType, labelName, xys):
        self.labelType = labelType
        self.labelName = labelName
        self.xys = xys


class AllLabelData:
    def __init__(self, labelTypeList):
        """
        Stores the data for the current image labels.
        """
        self.labels = []
        self.labelTypeList = labelTypeList
        self.labelCounts = {k: 0 for k in self.labelTypeList}

    def addBoxLabel(self, labelType, labelName, xypos4):
        self.labels.append(SingleLabelData(labelType, labelName, xypos4))
        self.labelCounts[labelType] += 1

    def add3DBoxLabel(self, labelType, labelName, xypos8):
        self.labels.append(SingleLabelData(labelType, labelName, xypos8))
        self.labelCounts[labelType] += 1

    def deleteLabelByName(self, labelName):
        data2Delete = [x for x in self.labels if x.labelName == labelName]
        for item in data2Delete:
            self.labels.remove(item)
            labelType = '-'.join(labelName.split('-')[:-1])