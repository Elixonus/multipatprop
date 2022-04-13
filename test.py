import numpy as np
from skimage.draw import line
img = np.zeros((10, 10), dtype=np.uint8)
rr, cc = line(1, 1, 9, 8)
img[rr, cc] = 1
print(img)
