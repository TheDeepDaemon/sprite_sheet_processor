from PIL import Image
import numpy as np
import os

def average_images(images):
    for i in range(len(images) - 1):
        if images[i].shape != images[i + 1].shape:
            print("Image dimensions must match.")
            return

    return np.average(np.array(images, dtype=float), axis=0)

def average_images_in_dir(dir_path, file_type):
    images = []

    for fname in os.listdir(dir_path):
        if fname.endswith(f'.{file_type}'):
            images.append(np.array(Image.open(os.path.join(dir_path, fname))))

    avg_img = average_images(images)

    Image.fromarray(np.uint8(avg_img)).convert('RGBA').save("output.png")
