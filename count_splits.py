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

def find_num_splits(image, max_divisions, axis):
    min_divisions = 1
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

def mark_division_lines(image, n_divisions, axis):
    dim_size = image.shape[axis]
    for i in range(n_divisions - 1):
        index = int(dim_size * (i + 1) / n_divisions)
        if axis == 0:
            image[index, :, 0] = 255
            image[index, :, 1] = 255
            image[index, :, 2] = 255
            image[index, :, 3] = 255
        else:
            image[:, index, 0] = 255
            image[:, index, 1] = 255
            image[:, index, 2] = 255
            image[:, index, 3] = 255
    Image.fromarray(np.uint8(image)).convert('RGBA').save("marked.png")

def main():
    fpath = "sprite_sheet.png"
    image = Image.open(fpath)
    
    image_arr = np.array(image)
    
    rows = find_num_splits(image_arr, 16, 0)
    cols = find_num_splits(image_arr, 16, 1)
    
    print(f"{rows} rows, {cols} cols")

if __name__ == "__main__":
    main()
