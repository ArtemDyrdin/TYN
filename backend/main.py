import asyncio
import websockets
import numpy as np
import urllib.request as ur
import cv2
import random
from rotate import rotate_image, rotate_point

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

with open('database\\answers_stat.txt', 'r') as file:
    data = file.read()
    answer_stat = eval(data)

with open('database\\spec_tasks.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    spec_tasks = [i for i in data]


face = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
settings_face = {
    'scaleFactor': 1.3,
    'minNeighbors': 3,
    'minSize': (50, 50),
}


def procent(index, side):
    procentp = int(
        answer_stat[index*2]/(answer_stat[index*2]+answer_stat[index*2+1])*100)
    if side == 'left':
        return procentp
    elif side == 'right':
        return 100 - procentp


async def server(websocket, path):
    stx = 0
    sty = 0
    stw = 0
    sth = 0
    temp = 0
    temp2 = 0
    # index of questions, variants and stats
    index = None
    # Register.
    connected.add(websocket)
    print('websocket opened \n')
    try:
        async for message in websocket:
            # extract the contents of the URL:
            try:
                if message == 'start':
                    a = random.randint(0, len(questions)-1)
                    while questions[a] == '#':
                        a += 1
                        if a == len(questions):
                            a = 0
                            temp += 1
                        if temp >= len(questions):
                            for conn in connected:
                                if conn == websocket:
                                    await conn.send(f'Break')
                    index = a
                    for conn in connected:
                        if conn == websocket:
                            # sending a questions and variants
                            await conn.send(f'Q{questions[a]}')
                            await conn.send(f'V{answers_var[a*2+1]}  {answers_var[a*2]}')
                else:
                    url_response = ur.urlopen(message)
                    # convert it into a numpy array
                    img_array = np.array(
                        bytearray(url_response.read()), dtype=np.uint8)
                    # decode the image (готово для использования в библиотеке cv2)
                    image = cv2.imdecode(img_array, -1)  # это готовый кадр
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
                            try:
                                if (x < stx-35 and y > sty+20) or (x + w > stx + w + 35 and y > sty + 20):
                                    b = random.randint(0, len(intfacts)-1)
                                    while intfacts[b] == '#':
                                        b += 1
                                        if b == len(spec_tasks):
                                            b = 0
                                            temp2 += 1
                                    if x < stx-35 and y > sty+20:
                                        print("left")
                                        answer_stat[index*2] += 1
                                        questions[a] = "#"
                                        intfacts[b] == '#'
                                        print(f"{procent(index, 'left')} %")
                                        await conn.send('ALeft')
                                        await conn.send(f"P{procent(index, 'left')} %")
                                        await conn.send(f'F{intfacts[b]}')

                                    elif x + w > stx + w + 35 and y > sty + 20:
                                        print("right")
                                        answer_stat[index*2+1] += 1
                                        questions[a] = "#"
                                        intfacts[b] == '#'
                                        print(f"{procent(index, 'right')} %")
                                        await conn.send('ARight')
                                        await conn.send(f"P{procent(index, 'right')} %")
                                        await conn.send(f'F{intfacts[b]}')

                                    with open('database\\answers_stat.txt', 'w') as file:
                                        file.write(f'{answer_stat}')
                                        print(answer_stat)

                            except Exception as expt:
                                print(f'Exception of writing to file: {expt}')

            except Exception as expt:
                print(expt)
                for conn in connected:
                    if conn == websocket:
                        await conn.send('EЛицо не обнаружено')

    except Exception as expt:
        print(f'ERROR!!!! \n{expt}\n')
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
