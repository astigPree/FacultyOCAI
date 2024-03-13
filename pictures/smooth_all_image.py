from PIL import Image
import os

def compress(image_file , new_file):

    filepath = image_file

    image = Image.open(filepath)

    image.save(new_file,
                 "JPEG",
                 optimize = True,
                 quality = 30)
    return


for file in os.listdir(os.getcwd()):
    if file.endswith(".jpg"):
        compress(file , file)