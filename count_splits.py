import numpy as np
from PIL import Image

def alpha_sum(image, n_divisions, axis):
    dim_size = image.shape[axis]
    total = 0
    for i in range(n_divisions - 1):
        index = int(dim_size * (i + 1) / n_divisions)
        if axis == 0:
            total += np.sum(image[index, :, 3])
        else:
            total += np.sum(image[:, index, 3])
    return total

def find_num_splits(image, min_divisions, max_divisions, axis):
    n = max_divisions - min_divisions
    
    lowest_alpha = float('inf')
    best_n_div = None
    
    for i in range(n):
        num_divisions = min_divisions + i
        alpha = alpha_sum(image, num_divisions, axis)
        if alpha <= lowest_alpha:
            lowest_alpha = alpha
            best_n_div = num_divisions
    
    return best_n_div
