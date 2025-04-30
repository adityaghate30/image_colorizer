import os
import cv2
import numpy as np
import urllib.request

class DeepLearningColorizer:
    def __init__(self):
        self.model_dir = "models"
        os.makedirs(self.model_dir, exist_ok=True)

        self.prototxt_url = "https://raw.githubusercontent.com/alexellis/faas-colorization/master/function/models/colorization_deploy_v2.prototxt"
        #  Defines the network architecture in Caffe's text format, specifying layers, connections, and parameters


        self.model_url = "https://data.vision.ee.ethz.ch/cvl/zhang/colorization/models/colorization_release_v2.caffemodel"
        #  Contains the trained weights for the network (approximately 128MB binary file)
        
        self.points_url = "https://raw.githubusercontent.com/richzhang/colorization/master/resources/pts_in_hull.npy"
        #   Defines the centroids of the 313 ab color clusters in the quantized ab space


        self.prototxt = os.path.join(self.model_dir, "colorization_deploy_v2.prototxt")
        self.model = os.path.join(self.model_dir, "colorization_release_v2.caffemodel")
        self.points = os.path.join(self.model_dir, "pts_in_hull.npy")

        self._download_if_missing()

        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        pts = np.load(self.points)

        class8_ab = self.net.getLayerId("class8_ab")
        conv8_313_rh = self.net.getLayerId("conv8_313_rh")

        pts = pts.transpose().reshape(2, 313, 1, 1)

        
        self.net.getLayer(class8_ab).blobs = [pts.astype(np.float32)]


        self.net.getLayer(conv8_313_rh).blobs = [np.full([1, 313], 2.606, dtype=np.float32)]

    def _download_if_missing(self):
        if not os.path.exists(self.prototxt):
            print("Downloading prototxt...")
            urllib.request.urlretrieve(self.prototxt_url, self.prototxt)

        if not os.path.exists(self.model):
            print("Downloading caffemodel...")
            urllib.request.urlretrieve(self.model_url, self.model)

        if not os.path.exists(self.points):
            print("Downloading pts_in_hull.npy...")
            urllib.request.urlretrieve(self.points_url, self.points)

    def colorize(self, image):

    
    
        scaled = image.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2Lab)
        l = lab[:, :, 0]
        l_resized = cv2.resize(l, (224, 224))
        l_resized -= 50

        net_input = cv2.dnn.blobFromImage(l_resized)
        self.net.setInput(net_input)
        ab_output = self.net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab_output = cv2.resize(ab_output, (image.shape[1], image.shape[0]))

        lab_out = np.concatenate((l[:, :, np.newaxis], ab_output), axis=2)
        colorized = cv2.cvtColor(lab_out, cv2.COLOR_Lab2RGB)
        colorized = np.clip(colorized, 0, 1)
        colorized = (255 * colorized).astype("uint8")
        return colorized
