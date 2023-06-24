# Imports
import os
import shutil
import glob
from PIL import Image

# Variables
zip = '.zip'
epub = '.epub'
folder_path = r"B:\Github\EPUB-Compressor\Compress"

# Functions
def find_file(folder_path, target_extension):
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Iterate over the files to find the target file
    for filename in files:
        file_path = os.path.join(folder_path, filename)

        # Check if the file matches the target extension
        if os.path.isfile(file_path) and filename.lower().endswith(target_extension.lower()):
            return file_path
        else:
            return 0


def change_file_type(file_path, new_extension):
    # Get the directory and base filename without extension
    directory, filename = os.path.split(file_path)
    filename_base, _ = os.path.splitext(filename)

    # Create the new file path with the desired extension
    new_file_path = os.path.join(directory, filename_base + new_extension)

    # Rename the file to the new file path
    shutil.move(file_path, new_file_path)


def unpack_archive(archive_path):
    # Get the folder name from the archive path
    folder_name = os.path.splitext(os.path.basename(archive_path))[0]
    
    # Create the target folder with the same name as the archive
    extract_path = os.path.join(os.path.dirname(archive_path), folder_name)
    os.makedirs(extract_path, exist_ok=True)
    
    # Extract the contents of the archive to the target folder
    shutil.unpack_archive(archive_path, extract_path)

    return extract_path


def find_subfolder_path(folder_path, subfolder_name):
    # Find a given folder path by folder name
    subfolder_path = None
    for path in glob.glob(os.path.join(folder_path, '**', subfolder_name), recursive=True):
        if os.path.isdir(path):
            subfolder_path = path
            break

    return subfolder_path


def compress_images(folder_path, quality=50):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is an image
        if os.path.isfile(file_path) and any(file_path.endswith(extension) for extension in ['.jpg', '.jpeg', '.png']):
            # Open the image
            img = Image.open(file_path)

            # Compress and overwrite the original image
            img.save(file_path, optimize=True, quality=quality)

            # Close the image
            img.close()


def compress_folder_to_zip(folder_path):
    # Get the parent directory of the folder
    parent_dir = os.path.dirname(folder_path)
    
    # Get the base name of the folder
    folder_name = os.path.basename(folder_path)
    
    # Generate the output ZIP file path
    zip_file_path = os.path.join(parent_dir, folder_name)

    # Compress the folder to a ZIP file
    shutil.make_archive(zip_file_path, 'zip', folder_path)
    return zip_file_path


def main(fpath,zip,epub):
    # Find file and change type to Zip
    main_path = find_file(fpath,epub)
    change_file_type(main_path,zip)
    change_path = find_file(fpath,zip)

    # Handle archive and find image folder
    arch_path = unpack_archive(change_path)
    img_path = find_subfolder_path(arch_path,"Images")

    # Compress images
    compress_images(img_path, quality=50)

    # Conversion back to Epub
    zip_path = compress_folder_to_zip(arch_path)
    shutil.rmtree(zip_path)
    change_file_type(zip_path+".zip",epub)


# Main Code
try:
    main(folder_path,zip,epub)
except Exception as e:
    print("File Error")
else:
    print("File Compressed")