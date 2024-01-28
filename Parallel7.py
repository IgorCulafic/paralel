from PIL import Image
import numpy as np
from multiprocessing import Pool, current_process
import os
import time
import random


def process_image(image_part, shift_value, color_channel):
    # Convert PIL Image to numpy array
    img_shift = np.array(image_part)

    # Shift the colour channel
    img_shift[..., color_channel] = (img_shift[..., color_channel] + shift_value).clip(
        0, 255
    )

    # Convert numpy array to PIL Image
    processed_img = Image.fromarray(img_shift.astype("uint8"))

    # Get process name
    process_name = current_process().name

    return processed_img, process_name


def main():
    start_time = time.time()  # Start timer

    img = Image.open("C:/Users/pitch/OneDrive/Desktop/paralel/big_pic.jpg")

    # Output file name numbers
    pic_num = str(48)
    process_num = str(34)

    # Number of rows and columns
    matrix_row = 6
    matrix_column = 4

    # Number of cores and variables
    number_of_cores_and_variables = 24

    width, height = img.size
    part_height = height // matrix_row
    part_width = width // matrix_column

    image_parts = []
    for i in range(matrix_row):
        for j in range(matrix_column):
            left = j * part_width
            upper = i * part_height
            right = min((j + 1) * part_width, width)
            lower = min((i + 1) * part_height, height)
            part = img.crop((left, upper, right, lower))
            image_parts.append(part)

    shift_RGB_value = [random.randrange(-250, 250, 10) for _ in range(24)]
    color_channels = [
        random.randint(0, 2) for _ in range(24)
    ]  # 0: Red, 1: Green, 2: Blue

    # Multiprocessing
    with Pool(number_of_cores_and_variables) as p:
        results = p.starmap(
            process_image, zip(image_parts, shift_RGB_value, color_channels)
        )

    processed_parts = [result[0] for result in results]

    final_img = Image.new("RGB", img.size)
    for i in range(matrix_row):
        for j in range(matrix_column):
            final_img.paste(
                processed_parts[i * matrix_column + j],
                (j * part_width, i * part_height),
            )

    directory = "C:/Users/pitch/OneDrive/Desktop/paralel"
    if not os.path.exists(directory):
        os.mkdir(directory)

    image_path = os.path.join(directory, "final" + pic_num + ".jpg")
    final_img.save(image_path)

    end_time = time.time()  # End timer

    # Calculate total time
    total_time = end_time - start_time

    # Core performance TXT file
    
    with open(os.path.join(directory, "process_info" + process_num + ".txt"), "w") as f:
        f.write(f"The program took {total_time} seconds\n")
#print out the message "Complete"
        

if __name__ == "__main__":
    main()
