import cv2
import numpy as np
from PIL import Image

def resize_dimensions(size, factor):
    return (int(size[0] * factor), int(size[1] * factor))

def get_deltas(arr):
    n = len(arr) - 1
    deltas = np.zeros(n, dtype=arr.dtype)
    for i in range(n):
        deltas[i] = arr[i + 1] - arr[i]
    return deltas

def compare_images(image1, image2):
    diff = image1 - image2
    return np.sum(np.square(diff))

def calc_information_loss_at_size(image, factor):
    # get original shape
    full_size = (image.shape[0], image.shape[1])
    
    # downsize
    small_size = resize_dimensions(full_size, factor)
    downsized_image = cv2.resize(image, (small_size[1], small_size[0]), interpolation = cv2.INTER_AREA)
    
    # upscale
    resized_image = cv2.resize(downsized_image, (full_size[1], full_size[0]), interpolation = cv2.INTER_CUBIC)
    
    return compare_images(resized_image, image)

def calc_factor(index, max_value):
    return (max_value - index - 1) / max_value

def find_original_size(img, stop_at=5):
    img_shape_0 = img.shape[0]
    img_shape_1 = img.shape[1]
    
    using_dim_1 = (img_shape_1 < img_shape_0)
    
    ceiling_dimension = min(img_shape_1, img_shape_0)
    
    n_results = ceiling_dimension - stop_at
    
    results = np.zeros(n_results, dtype=float)
    
    factor = None

    for i in range(n_results):
        # calculate the size from the index
        if using_dim_1:
            factor = calc_factor(i, img_shape_1)
        else:
            factor = calc_factor(i, img_shape_0)
        
        result = calc_information_loss_at_size(img, factor)
        results[i] = result
    
    # use the second difference to
    # find out where the biggest change is
    deltas = get_deltas(results)
    second_deltas = get_deltas(deltas)
    highest_d2 = np.argmax(second_deltas) + 1
    
    # calculate the size from the index
    if using_dim_1:
        factor = calc_factor(highest_d2, img_shape_1)
    else:
        factor = calc_factor(highest_d2, img_shape_0)
    
    return resize_dimensions(img.shape, factor)

def main():
    image = cv2.imread("image.png")
    original_size = find_original_size(image)
    print(original_size)

if __name__ == "__main__":
    main()