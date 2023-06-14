from PIL import Image, ImageOps
import os
import cv2
import numpy as np
from image_downsizing import find_original_size

def remove_transparency(img):
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

def no_alpha_ff(file_format):
    if file_format == 'bmp' or file_format == 'jpg' or file_format == 'jpeg':
        return True
    else:
        return False

def split_sprite_sheet(fpath, sprites_x, sprites_y, shrink_to_original=False, file_format="png"):
    
    # file stuff
    split_path = os.path.split(fpath)
    input_dir = split_path[0]
    input_fname = os.path.splitext(split_path[1])[0]

    output_dir = os.path.join(input_dir, input_fname)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the sprite sheet
    sprite_sheet = Image.open(fpath)
    
    sprite_sheet_size = sprite_sheet.size
    sprite_sheet_width = sprite_sheet_size[0]
    sprite_sheet_height = sprite_sheet_size[1]
    
    # calculate sprite size
    sprite_width = int(sprite_sheet_width / sprites_x)
    sprite_height = int(sprite_sheet_height / sprites_y)
    
    no_alpha = no_alpha_ff(file_format)

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
            sprite_image = remove_transparency(sprite)
            
            if shrink_to_original:
                sprite_image_arr = np.array(sprite_image)
                
                original_size = find_original_size(sprite_image_arr / 255.0)
                
                sprite_image_arr = cv2.resize(sprite_image_arr, (original_size[1], original_size[0]), interpolation = cv2.INTER_AREA)
                sprite_image = Image.fromarray(np.uint8(sprite_image_arr)).convert('RGBA')
            
            # add border
            expanded_image = ImageOps.expand(sprite_image, border=(1, 1, 1, 1), fill=(255, 255, 255, 0))
            
            if no_alpha:
                # handle formats with no alpha with white background
                solid_image = Image.new("RGBA", expanded_image.size, "WHITE")
                solid_image.paste(expanded_image, mask=expanded_image)
                expanded_image = solid_image.convert("RGB")

            # Save the sprite to a file
            output_fname = '{}_{}_{}.{}'.format(input_fname, i, j, file_format)
            output_fpath = os.path.join(output_dir, output_fname)
            expanded_image.save(output_fpath)

def main():
    split_sprite_sheet("sprite_sheet.png", 4, 2, True)

if __name__ == "__main__":
    main()
