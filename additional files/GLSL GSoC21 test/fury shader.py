import numpy as np
from fury import window, actor

dirs = np.random.rand(4, 3)
colors = np.random.rand(4, 3) * 255
centers = np.array([[1, 0, 0], [0, 0, 0], [-1, 0, 0], [0, 1, 0]])
scales = np.random.rand(4, 1)
