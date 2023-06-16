from PIL import Image
import numpy as np
import os

def swap_colors_of_pixel(img, i, j, color_indices):
    color = np.array(img[i, j])
    img[i, j, 0] = color[color_indices[0]]
    img[i, j, 1] = color[color_indices[1]]
    img[i, j, 2] = color[color_indices[2]]

def swap_colors(image, indices):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            swap_colors_of_pixel(image, i, j, indices)

    return Image.fromarray(np.uint8(image)).convert('RGBA')

def main():
    image = np.array(Image.open("sprite_sheets/shell.png"))
    swap_colors(image, (1, 2, 0)).save("output.png")

if __name__ == "__main__":
    main()
