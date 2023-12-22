import random


shift_RGB_value = [random.randrange(-250, 250, 10)]
color_channels = [random.randint(0, 2)]  # 0: Red, 1: Green, 2: Blue
# Number of cores

while len(shift_RGB_value) < (19):
    rand_color = random.randint(0, 2)
    # Check if the previous number is the same
    if rand_color == color_channels[-1]:
        continue
    valueer = random.randrange(-250, 250, 10)

    shift_RGB_value.append(valueer)
    color_channels.append(rand_color)

print("values" + str(len(shift_RGB_value)))
print("Color" + str(len(color_channels)))
