import asyncio
import websockets
import numpy as np
import urllib.request as ur
import cv2
import random
from PIL import Image
from math import sin, cos, radians

random.seed()

connected = set()

print('server started \n')

with open('.\database\\questions.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    questions = [i for i in data]

with open('.\database\\answers_var.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    answers_var = [i for i in data]

with open('database\\intfacts.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    intfacts = [i for i in data]

with open('database\\answers_stat.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    answers_stat = [int(data[i]) for i in range(0, len(data) - 1)]

with open('database\\spec_tasks.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    spec_tasks = [i for i in data]

with open('database\\answers_stat.txt', 'w', encoding='utf-8') as file:
    file.write('')


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


face = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
settings_face = {
    'scaleFactor': 1.3,
    'minNeighbors': 3,
    'minSize': (50, 50),
}


async def server(websocket, path):
    stx = 0
    sty = 0
    stw = 0
    sth = 0
    # Register.
    connected.add(websocket)
    print('websocket opened \n')
    try:
        async for message in websocket:
            # extract the contents of the URL:
            try:
                if message == 'start':
                    a = random.randint(0, len(questions)-1)
                    for conn in connected:
                        if conn == websocket:
                            # sending a questions and variants
                            await conn.send(f'Q{questions[a] + answers_var[a*2+1] + answers_var[a*2]}')
                else:
                    url_response = ur.urlopen(message)
                    # convert it into a numpy array
                    img_array = np.array(
                        bytearray(url_response.read()), dtype=np.uint8)
                    # decode the image (готово для использования в библиотеке cv2)
                    image = cv2.imdecode(img_array, -1)  # это готовый кадр
                    # print(type(image))
                    ret_flip = image
                    img_flip = image
                    ret = cv2.flip(ret_flip, 1)
                    img = cv2.flip(img_flip, 1)

                    for angle in [0, -55, 55]:
                        rimg = rotate_image(img, angle)
                        detected = face.detectMultiScale(
                            rimg, **settings_face)
                        if len(detected):
                            detected = [rotate_point(
                                detected[-1], img, -angle)]
                            break
                    for x, y, w, h in detected[-1:]:
                        img_facepro = rimg[y:y+h, x:x+w]

                    if not stx and x and y and w and h:
                        stx = x
                        sty = y
                        stw = w
                        sth = h
                        print("stx =", stx, "sty =", sty,
                              "stw =", stw, "sth =", sth)

                    for conn in connected:
                        if conn == websocket:
                            if x < stx-35 and y > sty+20:
                                print("left")
                                await conn.send('ALeft')
                            elif x + w > stx + w + 35 and y > sty + 20:
                                print("right")
                                await conn.send('ARight')

            except Exception as expt:
                print(expt)
                if expt == "local variable 'x' referenced before assignment":
                    for conn in connected:
                        if conn == websocket:
                            await conn.send('EЛицо не обнаружено')

    except Exception as expt:
        print(f'ERROR!!!! \n{expt}\n')
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
