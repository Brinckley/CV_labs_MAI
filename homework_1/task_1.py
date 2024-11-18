import cv2
import numpy as np
from queue import Queue

def findFirstAndLast(arr, x):
    print(type(arr))

    n = len(arr)
    first = -1
    last = -1
    for i in range(0, n):
        if (x != arr[i]):
            continue
        if (first == -1):
            first = i
        last = i
 
    if (first != -1):
        return (first, last)
    else:
        return None, None


def bfs(maze, start, end):
    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    #queue = deque([start])  # Queue for BFS
    
    queue = Queue()
    queue.put((start, []))    # Queue for BFS
    visited = set([start])    # Keep track of visited cells
    while not queue.empty():
        (current, path) = queue.get()

        for direction in directions:
            # Calculate the next cell's position
            next_cell = (current[0] + direction[0], current[1] + direction[1])

            if next_cell == end:
                print("The goal achieved!")
                return path + [next_cell] # Path found to exit

            # Check if the next cell is within the maze and not a wall
            if (0 <= next_cell[0] < len(maze) and
                    0 <= next_cell[1] < len(maze[0]) and
                    maze[next_cell[0]][next_cell[1]] != 0 and
                    next_cell not in visited):
                queue.put((next_cell, path + [next_cell]))
                visited.add(next_cell)

    return None


def find_way_from_maze(image: np.ndarray) -> tuple:
    """
    Найти путь через лабиринт.

    :param image: изображение лабиринта
    :return: координаты пути через лабиринт в виде (x, y)
    """
    bgr_base = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, fmatrix = cv2.threshold(bgr_base, 128, 255, cv2.THRESH_BINARY) # matrix where 0 - black point, 255 - white point
    height, width = fmatrix.shape

    # strart point - middle of white space on the highest line
    l, r = findFirstAndLast(fmatrix[0], 255)
    start = (0, (l + r) // 2)

    # finish point - middle of white space
    l, r = findFirstAndLast(fmatrix[-1], 255)
    finish = (height - 1, (l + r) // 2)

    height, width = fmatrix.shape
    #start = (0, np.where(fmatrix[0] == 255)[0][0])  
    #end = (height - 1, np.where(fmatrix[-1] == 255)[0][0])  
    solpath = bfs(fmatrix, start, finish)

    print(type(solpath))
    fy = []
    fx = []
    for (i, j) in solpath:
        fx.append(i)
        fy.append(j)
    return np.array(fx), np.array(fy)
