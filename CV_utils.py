# Computer Vision Utility Functions
# PIL functions: load_image, save_image, show_image, convert_to_PIL
# Conv2D, EdgeThresholding, CornerDetection, NonMaxSuppression

from PIL import Image
import numpy as np

def load_image(filename):
  img = Image.open(filename)
  img.load()
  data = np.asarray( img, dtype="int32" )
  return data

def save_image(npdata, filename):
  img = Image.fromarray(np.asarray(np.clip(npdata,0,255), dtype="uint8"), "L")
  img.save(filename)

def show_image(npdata):
  img = Image.fromarray(np.asarray(np.clip(npdata,0,255), dtype="uint8"), "L")
  
def convert_to_PIL(npdata):
  return Image.fromarray(np.asarray(np.clip(npdata,0,255), dtype="uint8"), "L")
  
 
def Conv2D(in_image, kernel):
  # assume kernel is a square matrix with un-even size
  N, M = in_image.shape
  k, _ = kernel.shape
  p = (k-1) // 2

  image = in_image
  out_image = np.zeros(in_image.shape)
  if p>0:
    image = np.zeros((N+2*p, M+2*p))

    # center
    image[p:-p, p:-p] = in_image
    # top and bottom
    image[:p,p:-p] = in_image[0,:]
    image[-p:, p:-p] = in_image[-1,:]
    # left and right
    image[p:-p,:p] = in_image[:,0].reshape(N,1)
    image[p:-p,-p:] = in_image[:,-1].reshape(N,1)
    # corners
    image[:p,:p] = in_image[0,0]
    image[:p,-p:] = in_image[0,-1]
    image[-p:,:p] = in_image[-1, 0]
    image[-p:,-p:] = in_image[-1,-1]
    
  for i in range(N):
    for j in range(M):
      im_slice = image[i:i+k, j:j+k]
      out_image[i,j] = np.sum(kernel * im_slice)

  return out_image
  
def EdgeThresholding(img, Tmin, Tmax):
  """
  Edge Thresholding with Histeresis
  """
  
  img = np.where(img >= Tmax, 1, img)
  img = np.where(img <= Tmin, 0, img)

  for i in range(img.shape[0]):
    for j in range(img.shape[1]):
      if img[i,j] > Tmin and img[i,j] < Tmax:
        i_min = max(0, i-1)
        i_max = min(img.shape[0], i+2)
        j_min = max(0, j-1)
        j_max = min(img.shape[1], j+2)
        if np.max(img[i_min:i_max, j_min:j_max]) == 1:
          img[i,j] = 1
        else: img[i,j] = 0
  return img

def CornerDetection(Ix, Iy, w, k):
  # Ix, Iy - first spatial derivatives in x and y axes, same size
  # w - int, square window size on which to look for corners, assumed odd, and >=3
  # k - harry corner detection coefficient 0.04<=k<=0.06
  N, M = Ix.shape
  
  # padding
  p = (w - 1) // 2
  Ixp = np.zeros((N+2*p, M+2*p))
  Ixp[p:-p, p:-p] = Ix
  Iyp = np.zeros((N+2*p, M+2*p))
  Iyp[p:-p, p:-p] = Iy
      
  R = np.zeros((N,M))
  for i in range(N):
    for j in range(M):
      Ix_slice = Ixp[i:i+w, j:j+w]
      Iy_slice = Iyp[i:i+w, j:j+w]
      # computing coefficients
      a = np.sum(Ix_slice**2)
      c = np.sum(Iy_slice**2)
      b = 2*np.sum(Ix_slice*Iy_slice)

      l1 = .5 * (a + c + np.sqrt(b**2 + (a-c)**2))
      l2 = .5 * (a + c - np.sqrt(b**2 + (a-c)**2))

      R[i,j] = l1 * l2 - k * (l1 + l2)**2
  return R
  
def NonMaxSuppression(img, w):
  # img - image, with minimum element value 0
  # w - window size, assumed to be odd

  N, M = img.shape
  # padding
  p = (w - 1) // 2
  img_p = np.zeros((N+2*p, M+2*p))
  img_p[p:-p, p:-p] = img
  
  # initializing output
  out_img = np.zeros((N,M))

  for i in range(N):
    for j in range(M):
     img_slice = img_p[i:i+w, j:j+w]
     if img[i,j] == np.max(img_slice): out_img[i,j] = img[i,j]
  
  return out_img