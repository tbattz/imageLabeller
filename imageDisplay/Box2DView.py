import dearpygui.dearpygui as dpg

class Box2DView:
    def __init__(self, xys4, parentAxes, boxName):
        self.x = [xy[0] for xy in xys4] + [xys4[0][0]]
        self.y = [xy[1] for xy in xys4] + [xys4[0][1]]
        self.parentAxes = parentAxes
        self.boxName = boxName

        self.line = None

        self.createLine()

    def createLine(self):
        self.line = dpg.add_line_series(self.x, self.y,
                            label=self.boxName+'-line',
                            tag=self.boxName+'-line',
                            parent=self.parentAxes)

    def editPoints(self, xys4):
        self.x = [xy[0] for xy in xys4] + [xys4[0][0]]
        self.y = [xy[1] for xy in xys4] + [xys4[0][1]]
        dpg.set_value(self.boxName+'-line', [self.x, self.y])


    def cleanup(self):
        dpg.delete_item(self.boxName+'-line')