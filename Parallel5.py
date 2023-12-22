from PIL import Image
import numpy as np
from multiprocessing import Pool, current_process
import os
import time
import random


def process_image(image_part, shift_value, color_channel):
    # Record start time
    start_time = time.time()

    # Convert PIL Image to numpy array
    img_shift = np.array(image_part)

    # Shift the colour channel
    img_shift[..., color_channel] = (img_shift[..., color_channel] + shift_value).clip(
        0, 255
    )

    # Convert numpy array to PIL Image
    processed_img = Image.fromarray(img_shift.astype("uint8"))

    # Record end time
    end_time = time.time()

    # Calculate process time
    process_time = end_time - start_time

    # Get process name
    process_name = current_process().name

    return processed_img, process_name, process_time


def main():
    img = Image.open("C:/Users/pitch/OneDrive/Desktop/paralel/big_pic.jpg")

    # Output file name numbers
    pic_num = str(32)
    process_num = str(18)

    # Number of rows and columns
    # IMPORTANT!!!
    # matrix_row * matrix_column = number_of_cores_and_variables
    matrix_row = 6
    matrix_column = 4

    # Number of cores and variables
    number_of_cores_and_variables = matrix_row * matrix_column

    width, height = img.size
    part_height = height // matrix_row
    part_width = width // matrix_column
    image_parts = []

    for i in range(matrix_row):
        for j in range(matrix_column):
            left = j * part_width
            upper = i * part_height
            right = (j + 1) * part_width if j + 1 != matrix_row else width
            lower = (i + 1) * part_height if i + 1 != matrix_column else height
            part = img.crop((left, upper, right, lower))
            image_parts.append(part)

    shift_RGB_value = [random.randrange(-250, 250, 10)]
    color_channels = [random.randint(0, 2)]  # 0: Red, 1: Green, 2: Blue

    # Number of variables and generating variables, must be same as core value
    for i in range(number_of_cores_and_variables - 1):
        rand_color = random.randint(0, 2)

        # Check if the previous number is the same
        if rand_color == color_channels[-1]:
            while rand_color == color_channels[-1]:
                rand_color = random.randint(0, 2)

        valueer = random.randrange(-250, 250, 10)

        shift_RGB_value.append(valueer)
        color_channels.append(rand_color)

    # Alternative solution, might be faster but not that important
    # while len(shift_RGB_value) < (number_of_cores_and_variables - 1):
    #     rand_color = random.randint(0, 2)
    #     # Check if the previous number is the same
    #     if rand_color == color_channels[-1]:
    #         continue
    #     valueer = random.randrange(-250, 250, 10)

    #     shift_RGB_value.append(valueer)
    #     color_channels.append(rand_color)

    # Multiprocessing
    # IMPORTANT!!!
    # Must edit column and row numbers for more cores to apply
    # They corespond to segments of the photo, 6 segments 6 core max
    with Pool(number_of_cores_and_variables) as p:
        results = p.starmap(
            process_image, zip(image_parts, shift_RGB_value, color_channels)
        )

    processed_parts = [result[0] for result in results]
    process_info = [(result[1], result[2]) for result in results]

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

    # Core performance TXT file
    with open(os.path.join(directory, "process_info" + process_num + ".txt"), "w") as f:
        for info in process_info:
            f.write(f"Process {info[0]} took {info[1]} seconds\n")


if __name__ == "__main__":
    main()
