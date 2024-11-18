import numpy as np
import cv2 as cv


def rotate(image, point: tuple, angle: float) -> np.ndarray:
    """
    Повернуть изображение по часовой стрелке на угол от 0 до 360 градусов и преобразовать размер изображения.

    :param image: исходное изображение
    :param point: значение точки (x, y), вокруг которой повернуть изображение
    :param angle: угол поворота
    :return: повернутное изображение
    """
    all_points = np.array([[image.shape[1] - 1, image.shape[0] - 1],
                          [0, 0], [image.shape[1] - 1, 0],
                          [0, image.shape[0] - 1]])

    matrix = cv.getRotationMatrix2D(point, angle, scale=1.0)
    result = apply_transformation(all_points, matrix)

    return cv.warpAffine(image, matrix, result)


def apply_warpAffine(image, points1, points2) -> np.ndarray:
    """
    Применить афинное преобразование согласно переходу точек points1 -> points2 и
    преобразовать размер изображения.

    :param image:
    :param points1:
    :param points2:
    :return: преобразованное изображение
    """

    all_points = np.array([[image.shape[1] - 1, image.shape[0] - 1],
                          [0, 0], [image.shape[1] - 1, 0],
                          [0, image.shape[0] - 1]])

    matrix = cv.getAffineTransform(points1, points2)
    result = apply_transformation(all_points, matrix)

    return cv.warpAffine(image, matrix, result)


def apply_transformation(all_points, matrix):
    rotation = np.hstack((all_points, np.ones((all_points.shape[0], 1))))

    transformed = matrix @ rotation.T

    matrix[:, 2] -= transformed.min(axis=1)
    result = transformed.max(axis=1) - transformed.min(axis=1)
    result = np.int64(np.ceil(result))
    return result