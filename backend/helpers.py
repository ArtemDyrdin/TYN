from math import sin, cos, radians
import os
import cv2

def load_lines(path, encoding='utf-8'):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding=encoding) as f:
        return [line for line in f.read().splitlines()]
    
def procent(index, side, answer_stat):
    try:
        left = int(answer_stat[index * 2])
        right = int(answer_stat[index * 2 + 1])
        total = left + right
        if total == 0:
            return 50
        procentp = int(left / total * 100)
        return procentp if side == 'left' else 100 - procentp
    except Exception:
        return 50

def rotate_image(image, angle):
    if angle == 0:
        return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(
        image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result


def rotate_point(pos, img, angle):
    if angle == 0:
        return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]