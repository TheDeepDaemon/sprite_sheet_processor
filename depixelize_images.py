import os
import subprocess

EXE_PATH = "bin/depixelize-svg.exe"

def depixelize_image(input_fpath, output_fpath):
    try:
        command = [EXE_PATH, input_fpath, output_fpath]
        subprocess.run(command, check=True)
    except Exception as e:
        print("An error occurred: ", e)

def depixelize_images_in_directory(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith('.bmp'):
            input_fname = os.path.splitext(filename)[0]
            output_fname = "{}.svg".format(input_fname)
            depixelize_image(os.path.join(input_directory, filename), os.path.join(output_directory, output_fname))

def main():
    depixelize_images_in_directory("bmp_files", "svg_files")

if __name__ == "__main__":
    main()
