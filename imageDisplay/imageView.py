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

		self.loadedImage = LoadedImage(None, 800, 800, parentTag="Right", beforeTag="imgFilenameText")

	def setLoadedImage(self, imagePath):
		self.loadedImage.loadImage(imagePath)
		fileStr = "File: %s" % self.loadedImage.filename
		dpg.set_value(self.fileText, value=fileStr)

	def handleWindowResize(self, maxWidth, maxHeight):
		self.loadedImage.setMaxSize(maxWidth, maxHeight)



class LoadedImage:
	def __init__(self, filename, maxWidth, maxHeight, parentTag, beforeTag):
		self.filename = filename
		self.parentTag = parentTag
		self.beforeTag = beforeTag
		self.image = None
		self.width, self.height = None, None
		self.newWidth, self.newHeight = None, None
		self.maxWidth = maxWidth
		self.maxHeight = maxHeight
		self.data = None
		self.flatImg = None
		self.resizedImg = None

		self.textureLoaded = False


	def loadImage(self, filename):
		self.filename = filename
		self.image = Image.open(self.filename)
		self.width = self.image.size[0]
		self.height = self.image.size[1]
		self.resizedImg = self.resizeToLimits(self.image)
		data = np.ascontiguousarray(self.resizedImg)
		# Add alpha column if needed
		if data.shape[2] != 4:
			ones = np.ones((data.shape[0], data.shape[1], 1)) * 255.0
			self.data = np.c_[data, ones]
		else:
			self.data = data
		self.flatImg = self.flatternImg(self.data)

		if not self.textureLoaded:
			self.createTexture()
			self.textureLoaded = True
		else:
			self.updateTexture()

	def createTexture(self):
		with dpg.texture_registry(show=False):
			dpg.add_static_texture(self.newWidth, self.newHeight, self.flatImg, tag='textureTag')

		dpg.add_group(tag='imgGroup', horizontal=True, parent=self.parentTag, before=self.beforeTag)
		dpg.add_image("textureTag", parent="imgGroup")

	def updateTexture(self):
		dpg.delete_item("imgGroup")
		dpg.delete_item("textureTag")
		self.createTexture()

	def flatternImg(self, img):
		return np.true_divide(np.asfarray(np.ravel(img), dtype='f'), 255.0)

	def setMaxSize(self, maxWidth, maxHeight):
		self.maxWidth = maxWidth
		self.maxHeight = maxHeight

		self.loadImage(self.filename)

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
