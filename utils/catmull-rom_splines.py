import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(precision=4)

import splines
from helper import plot_spline_2d, plot_tangent_2d

# points1 = [
#     (-1, -0.5),
#     (0, 2.3),
#     (1, 1),
#     (4, 1.3),
#     (3.8, -0.2),
#     (2.5, 0.1),
# ]

points1 = [
    (-1, -0.5),
    (0, 2.3),
    (1, 1)]

s1 = splines.CatmullRom(points1, endconditions='closed')

fig, ax = plt.subplots()
plot_spline_2d(s1, ax=ax)
plt.show()