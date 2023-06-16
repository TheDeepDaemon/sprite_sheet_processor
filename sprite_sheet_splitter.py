from PIL import Image, ImageOps
import os
import cv2
import numpy as np
from image_downsizing import estimate_downsizing_factor, resize_dimensions

def remove_transparent_edges(img):
    """Remove transparent edges from the image."""

    # Only process if image has transparency 
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        
        # Need to convert to RGBA if LA format due to a bug in PIL
        alpha = img.convert('RGBA').split()[-1]
        
        # Find image bounding box
        bbox = alpha.getbbox()

        # If bbox, return an image cropped to this bounding box
        # else, the image was empty, return the original image
        return img.crop(bbox) if bbox else img
    else:
        return img

def remove_low_alpha(img, cutoff=128):
    img_arr = np.array(img)
    for i in range(img_arr.shape[0]):
        for j in range(img_arr.shape[1]):
            pix = img_arr[i, j]
            if pix[3] < cutoff:
                img_arr[i, j, :] = 0
    return Image.fromarray(np.uint8(img_arr)).convert('RGBA')

def no_alpha_ff(file_format):
    if file_format == 'bmp' or file_format == 'jpg' or file_format == 'jpeg':
        return True
    else:
        return False

def split_sprite_sheet(fpath, output_dir, sprites_x, sprites_y, shrink_to_original=False, file_format="png"):
    
    # file stuff
    split_path = os.path.split(fpath)
    input_fname = os.path.splitext(split_path[1])[0]
    
    # Open the sprite sheet
    sprite_sheet = Image.open(fpath)
    
    sprite_sheet_size = sprite_sheet.size
    sprite_sheet_width = sprite_sheet_size[0]
    sprite_sheet_height = sprite_sheet_size[1]
    
    # calculate sprite size
    sprite_width = int(sprite_sheet_width / sprites_x)
    sprite_height = int(sprite_sheet_height / sprites_y)
    
    no_alpha = no_alpha_ff(file_format)
    
    sprite_list = []
    factors = []
    
    for i in range(sprites_y):
        for j in range(sprites_x):
            # Calculate the position of the current sprite
            left = j * sprite_width
            top = i * sprite_height
            right = (j + 1) * sprite_width
            bottom = (i + 1) * sprite_height

            # Extract the sprite
            sprite = sprite_sheet.crop((left, top, right, bottom))
            
            # remove transparency
            sprite = remove_transparent_edges(sprite)
            
            sprite_list.append((sprite, i, j))
            
            if shrink_to_original:
                estimated_factor = estimate_downsizing_factor(np.array(sprite) / 255.0)
                factors.append(estimated_factor)
    
    if len(factors) > 0:
        factors = np.array(factors, dtype=float)
        factor = np.median(factors)
    
    for sprite, i, j in sprite_list:
        
        if shrink_to_original:
            sprite_arr = np.array(sprite)
            original_size = resize_dimensions(sprite_arr.shape, factor)
            sprite_arr = cv2.resize(sprite_arr, (original_size[1], original_size[0]), interpolation = cv2.INTER_AREA)
            sprite = Image.fromarray(np.uint8(sprite_arr)).convert('RGBA')
        
        # add border
        expanded_image = ImageOps.expand(sprite, border=(1, 1, 1, 1), fill=(255, 255, 255, 0))
        
        # reduce the color palette
        quantized_image = remove_low_alpha(expanded_image).quantize(16, kmeans=16)
        quantized_image = quantized_image.convert('RGBA')
        
        # set the output
        output_image = quantized_image
        
        if no_alpha:
            # handle formats with no alpha with white background
            background = Image.new('RGB', output_image.size, (255, 255, 255))
            background.paste(output_image, mask=output_image.split()[3])
            output_image = background

        # Save the sprite to a file
        output_fname = '{}_{}_{}.{}'.format(input_fname, i, j, file_format)
        output_fpath = os.path.join(output_dir, output_fname)
        output_image.save(output_fpath)

def main():
    split_sprite_sheet("sprite_sheets/underwater_sprite_sheet7.png", "split_sprites", 3, 2, True, 'bmp')

if __name__ == "__main__":
    main()
