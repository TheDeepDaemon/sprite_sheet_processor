import cv2
import numpy as np
from scipy.spatial import KDTree
from PIL import Image

def crystallize_voronoi(img, num_cells):
    img_np = np.array(img)

    # Generate the centers of Voronoi cells
    centers = np.array([(np.random.randint(0, img_np.shape[1]), np.random.randint(0, img_np.shape[0])) for _ in range(num_cells)])

    # Generate Voronoi tessellation
    tree = KDTree(centers)

    # Create a result image
    result_img = np.zeros_like(img_np)

    # Get the nearest Voronoi cell for each pixel and color the pixel as the average color of the cell
    for x in range(img_np.shape[1]):
        for y in range(img_np.shape[0]):
            # Find the nearest center
            _, idx = tree.query([x, y])
            center = centers[idx]
            result_img[y, x] = img_np[center[1], center[0]]

    # Save the result
    result_img_pil = Image.fromarray(result_img)
    result_img_pil.save("output.png")

image = cv2.imread("split_sprites/sprite.bmp")

image = cv2.resize(image, (256, 256), interpolation = cv2.INTER_CUBIC)

crystallize_voronoi(image, 1000)
