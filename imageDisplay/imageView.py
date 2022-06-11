import dearpygui.dearpygui as dpg
from PIL import Image
import numpy as np


class ImageDisplayView:
	def __init__(self, parent):
		self.parent = parent

		# Create right group for images
		self.groupRight = dpg.add_group(label="Right", parent=self.parent)
		self.fileText = dpg.add_text("File: " , tag="imgFilenameText", parent=self.groupRight)
		self.imgButtonGroup = dpg.add_group(label="Image Button", horizontal=True, parent=self.groupRight)
		self.prevBtn = dpg.add_button(label="Prev (<-)", parent=self.imgButtonGroup)
		self.saveBtn = dpg.add_button(label="Save Data(S)", parent=self.imgButtonGroup)
		self.nextBtn = dpg.add_button(label="Next (->)", parent=self.imgButtonGroup)

		self.plot = dpg.add_plot(tag="plot", label="Image Plot", height=400, width=-1, equal_aspects=True, before=self.fileText, parent=self.groupRight)
		self.xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="x axis", parent=self.plot)
		self.yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="y axis", parent=self.plot)

		self.loadedImage = LoadedImage(None, 800, 800, parentTag=self.groupRight, yaxis=self.yaxis)


	def reinitPlot(self, plotHeight):
		# Remove previous
		dpg.delete_item("plot")
		# Create new
		self.plot = dpg.add_plot(tag="plot", label="Image Plot", height=plotHeight, width=-1, equal_aspects=True, before=self.fileText, parent=self.groupRight)
		self.xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="x axis", parent=self.plot)
		self.yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="y axis", parent=self.plot)
		self.loadedImage.setYaxis(self.yaxis)

		# Load new texture
		self.loadedImage.updateTexture()


	def setLoadedImage(self, imagePath, currInd, imgCount):
		self.loadedImage.loadImage(imagePath)
		fileStr = "File: %s (%i/%i)" % (self.loadedImage.filename, currInd, imgCount)
		dpg.set_value(self.fileText, value=fileStr)


	def handleWindowResize(self, maxWidth, maxHeight):
		self.loadedImage.setMaxSize(maxWidth, maxHeight)
		dpg.set_item_height(self.plot, maxHeight)


class LoadedImage:
	def __init__(self, filename, maxWidth, maxHeight, parentTag, yaxis):
		self.filename = filename
		self.parentTag = parentTag
		self.imgLayer = None
		self.yaxis = yaxis
		self.image = None
		self.width, self.height = None, None
		self.newWidth, self.newHeight = None, None
		self.maxWidth = maxWidth
		self.maxHeight = maxHeight
		self.data = None
		self.flatImg = None
		self.resizedImg = None

		self.textureLoaded = False

	def setYaxis(self, newYaxis):
		self.yaxis = newYaxis

	def flatternImg(self, img):
		return np.true_divide(np.asfarray(np.ravel(img), dtype='f'), 255.0)

	def setMaxSize(self, maxWidth, maxHeight):
		self.maxWidth = maxWidth
		self.maxHeight = maxHeight

		self.resizeImage()

	def resizeToLimits(self, image):
		# Resize the image to the maximum given
		widthRatio = self.width / self.maxWidth
		heightRatio = self.height / self.maxHeight
		if heightRatio > widthRatio:
			# Height limits scaling
			scale = 1/heightRatio
		else:
			# Width limits scaling
			scale = 1/widthRatio

		self.newWidth = int(self.width*scale)
		self.newHeight = int(self.height*scale)
		resizedImage = image.resize((self.newWidth, self.newHeight), Image.LANCZOS)

		return resizedImage

	def resizeImage(self):
		self.resizedImg = self.resizeToLimits(self.image)
		data = np.ascontiguousarray(self.resizedImg)
		# Add alpha column if needed
		if data.shape[2] != 4:
			ones = np.ones((data.shape[0], data.shape[1], 1)) * 255.0
			self.data = np.c_[data, ones]
		else:
			self.data = data
		self.flatImg = self.flatternImg(self.data)


	def loadImage(self, filename):
		self.filename = filename
		self.image = Image.open(self.filename)
		self.width = self.image.size[0]
		self.height = self.image.size[1]

		self.resizeImage()

	def createTexture(self):
		with dpg.texture_registry(show=False):
			dpg.add_static_texture(self.newWidth, self.newHeight, self.flatImg, tag='textureTag')

		self.textureLoaded = True

		dpg.add_image_series("textureTag", [0, 0], [self.width, self.height], parent=self.yaxis)
		#dpg.draw_line((10, 10), (800, 800), color=(255, 0, 0, 255), thickness=1, parent=self.drawList)

	def updateTexture(self):
		if self.textureLoaded:
			dpg.delete_item("textureTag")

		self.createTexture()


