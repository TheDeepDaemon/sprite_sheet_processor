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

def calc_factor(index, top_index, original_dimension_value):
    return (top_index - index) / original_dimension_value

# estimate the factor to multiply the dimensions by
# in order to shrink a low-res image to its original size
def estimate_downsizing_factor(img, stop_at=5):
    ceiling_dimension = min(img.shape[0], img.shape[1])
    
    top_index = int(ceiling_dimension / 2)
    
    n_results = top_index - stop_at
    
    results = np.zeros(n_results, dtype=float)
    
    factor = None

    for i in range(n_results):
        # calculate the size from the index
        factor = calc_factor(i, top_index, ceiling_dimension)
        result = calc_information_loss_at_size(img, factor)
        results[i] = result
    
    # use the second difference to
    # find out where the biggest change is
    deltas = get_deltas(results)
    second_deltas = get_deltas(deltas)
    highest_d2 = np.argmax(second_deltas) + 1
    
    # calculate the size from the index
    return calc_factor(highest_d2, top_index, ceiling_dimension)

def main():
    image = cv2.imread("image.png")
    estimated_factor = estimate_downsizing_factor(image)
    print(estimated_factor)

if __name__ == "__main__":
    main()
