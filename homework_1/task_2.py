import cv2
import numpy as np


def find_road_number(image: np.ndarray) -> int:
    """
    Найти номер дороги, на которой нет препятсвия в конце пути.

    :param image: исходное изображение
    :return: номер дороги, на котором нет препятсвия на дороге
    """
    bgr_base = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)
    full_image = get_obstacle(bgr_base) + get_lines(bgr_base) + get_car(bgr_base) + get_obstacle(bgr_base)
    height, width = full_image.shape

    ls = 0
    rs = 0
    for i in range(width):
        curh = height // 2
        if full_image[curh, i] != 0:
            if rs != 0:
                break
            ls += 1
        
        if full_image[curh, i] == 0 and ls != 0:
            rs += 1

    road_count = round((height - ls) / (ls + rs))
    roads = np.zeros(road_count)

    delta = int(((width - ls) / road_count) // 2)
    for road_num in range(road_count):
        for dh in range(height // 2):
            if(full_image[dh, delta + 2 * delta * road_num] == 255 or full_image[dh, delta + 2 * delta * road_num] == 254):
                roads[road_num] = -1
                break

    cars = np.zeros(road_count)
    for road_num in range(road_count):
        for dh in range(height // 2, height, 1):
            if(full_image[dh, delta + 2 * delta * road_num] == 255 or full_image[dh, delta + 2 * delta * road_num] == 254):
                cars[road_num] = -1
                break

    cur = 0
    cur = list(cars).index(-1)
    free_space = list(roads).index(0)

    if(cur == free_space):
        return -1
    return free_space+1


def get_obstacle(bgr_base):
    return cv2.inRange(bgr_base, (1, 250, 250), (255, 255, 255))


def get_car(bgr_base):
    return cv2.inRange(bgr_base, (109, 0, 0), (112, 255, 255))


def get_lines(bgr_base):
    return cv2.inRange(bgr_base, (25, 0, 0), (32, 255, 255))
