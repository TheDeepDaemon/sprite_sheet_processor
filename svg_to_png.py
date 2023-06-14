import os
from cairosvg import svg2png

def convert_svg_to_png(input_folder, output_folder):
    
    # List all files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith('.svg'):
            # Form the full file path by joining the input folder and the file name
            input_file_path = os.path.join(input_folder, filename)

            # Form the output file path by joining the output folder and the file name
            # Replace the .svg extension with .png
            output_file_path = os.path.join(output_folder, filename.replace('.svg', '.png'))

            # Convert SVG to PNG
            svg2png(url=input_file_path, write_to=output_file_path)

# Replace these with the paths to your folders
input_folder = 'svg_files'
output_folder = 'png_files'

# Call the function
convert_svg_to_png(input_folder, output_folder)
