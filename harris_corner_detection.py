"""
Harris Corner Detection Implementation
On Grayscale Images
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from CV_utils import *

# Load Image
filepath = '/content/drive/MyDrive/Colab Notebooks/Computer Vision Algorithms/'
img = load_image(filepath+'lab.gif')

pil_img = convert_to_PIL(img)
pil_img

# using standard Sobel filter 
sobel_5x5 = np.array([[-1, -2, 0, 2, 1],
                      [-2, -3, 0, 3, 2],
                      [-3, -5, 0, 5, 3],
                      [-2, -3, 0, 3, 2],
                      [-1, -2, 0, 2, 1]])

sobel_3x3 = np.array([[-1, 0, 1],
                      [-2, 0, 3],
                      [-1, 0, 1]])

Ix = Conv2D(img, sobel_5x5)
Iy = Conv2D(img, sobel_5x5.T)

# show gradient images
pil_Ix = convert_to_PIL(255*abs(Ix)/np.max(abs(Ix)))
pil_Ix

pil_Iy = convert_to_PIL(255*abs(Iy)/np.max(abs(Iy)))
pil_Iy

# Compute corner locations
R = CornerDetection(Ix, Iy, w=7, k=0.06)
R = (R - np.min(R)) / (np.max(R) - np.min(R))
R = np.where(R>np.quantile(R, 0.95), R, 0)

# show corner image ("blurred")
pil_R = convert_to_PIL(255*R)
pil_R

# reduce corners using non-max suppression
R_NMS = NonMaxSuppression(R, w=5)

pil_R_NMS = convert_to_PIL(255*R_NMS)
pil_R_NMS

# extract locations
corners = np.argwhere(R_NMS>0)

# plot image with computed corners
img2 = plt.imread(filepath+'lab.gif')

fig,ax = plt.subplots(1)
ax.set_aspect('equal')

ax.imshow(img2)

for x, y in corners:
  circ = Circle((y, x), radius=5, fill=False, linestyle='solid')
  ax.add_patch(circ)

plt.show()

