import asyncio
import websockets
import numpy as np
import urllib.request as ur
import cv2
import random
import os
from helpers import *

random.seed()

connected = set()

print('server started \n')

BASE = os.path.join(os.path.dirname(__file__), 'database')

questions = load_lines(os.path.join(BASE, 'questions.txt'))
answers_var = load_lines(os.path.join(BASE, 'answers_var.txt'))
intfacts = load_lines(os.path.join(BASE, 'intfacts.txt'))

ans_stat_path = os.path.join(BASE, 'answers_stat.txt')
if os.path.exists(ans_stat_path):
    with open(ans_stat_path, 'r', encoding='utf-8') as f:
        try:
            answer_stat = eval(f.read())
        except Exception:
            answer_stat = []
else:
    answer_stat = []

spec_tasks = load_lines(os.path.join(BASE, 'spec_tasks.txt'))

# face detector
face = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
settings_face = {
    'scaleFactor': 1.3,
    'minNeighbors': 3,
    'minSize': (50, 50),
}

async def server(websocket):
    # Use None for uninitialized anchor
    stx = sty = stw = sth = None
    temp = 0
    temp2 = 0
    index = None
    a = None

    # Register.
    connected.add(websocket)
    print('websocket opened \n')
    try:
        async for message in websocket:
            try:
                if message == 'start':
                    if not questions:
                        await websocket.send('EНет вопросов')
                        continue

                    a = random.randint(0, len(questions) - 1)

                    # Find next non-# question (protect infinite loop)
                    tries = 0
                    while questions[a] == '#':
                        a += 1
                        if a >= len(questions):
                            a = 0
                        tries += 1
                        if tries >= len(questions):
                            # all are '#'
                            await websocket.send('Break')
                            a = None
                            break

                    if a is None:
                        continue

                    index = a
                    # Send question and variants (guard indexes)
                    q_text = questions[a] if a < len(questions) else ''
                    # answers_var expected to store two lines per question?? original used a*2+1 and a*2
                    var_right = answers_var[a * 2 + 1] if a * 2 + 1 < len(answers_var) else ''
                    var_left = answers_var[a * 2] if a * 2 < len(answers_var) else ''
                    await websocket.send(f'Q{q_text}')
                    await websocket.send(f'V{var_right}  {var_left}')

                else:
                    # treat message as image URL
                    try:
                        url_response = ur.urlopen(message)
                    except Exception as e:
                        await websocket.send('EНе удалось загрузить изображение')
                        print('URL open error:', e)
                        continue

                    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                    image = cv2.imdecode(img_array, -1)
                    if image is None:
                        await websocket.send('EНевалидное изображение')
                        continue

                    # flip horizontally (mirror)
                    img = cv2.flip(image, 1)

                    detected = []
                    # try a few rotations
                    for angle in [0, -55, 55]:
                        rimg = rotate_image(img, angle)
                        det = face.detectMultiScale(rimg, **settings_face)
                        if len(det):
                            # take the last detected (like in original)
                            detected = [rotate_point(det[-1], img, -angle)]
                            break

                    if not detected:
                        # no face detected
                        await websocket.send('EЛицо не обнаружено')
                        continue

                    # get x,y,w,h from detection
                    x, y, w, h = detected[-1]

                    # crop face area if needed (not used currently)
                    # img_facepro = rimg[y:y + h, x:x + w]

                    # initialize anchor if not set
                    if stx is None and x is not None:
                        stx, sty, stw, sth = x, y, w, h
                        print("anchor set: stx =", stx, "sty =", sty, "stw =", stw, "sth =", sth)

                    # now check for left/right nod (with bounds checking)
                    try:
                        # choose a fact index b
                        if (x < stx - 35 and y > sty + 20) or (x + w > stx + stw + 35 and y > sty + 20):
                            # find a non-# fact
                            if not intfacts:
                                b = None
                            else:
                                b = random.randint(0, len(intfacts) - 1)
                                tries = 0
                                while intfacts[b] == '#':
                                    b += 1
                                    if b >= len(intfacts):
                                        b = 0
                                    tries += 1
                                    if tries >= len(intfacts):
                                        b = None
                                        break

                            # LEFT
                            if x < stx - 35 and y > sty + 20:
                                print("left")
                                if index is not None and index * 2 < len(answer_stat):
                                    answer_stat[index * 2] += 1
                                if a is not None:
                                    questions[a] = "#"
                                if b is not None:
                                    intfacts[b] = '#'
                                p = procent(index, 'left', answer_stat) if index is not None else 50
                                await websocket.send('ALeft')
                                await websocket.send(f'P{p} %')
                                if b is not None:
                                    await websocket.send(f'F{intfacts[b]}')
                                else:
                                    await websocket.send('FНет фактов')

                            # RIGHT
                            elif x + w > stx + stw + 35 and y > sty + 20:
                                print("right")
                                if index is not None and index * 2 + 1 < len(answer_stat):
                                    answer_stat[index * 2 + 1] += 1
                                if a is not None:
                                    questions[a] = "#"
                                if b is not None:
                                    intfacts[b] = '#'
                                p = procent(index, 'right', answer_stat) if index is not None else 50
                                await websocket.send('ARight')
                                await websocket.send(f'P{p} %')
                                if b is not None:
                                    await websocket.send(f'F{intfacts[b]}')
                                else:
                                    await websocket.send('FНет фактов')

                            # persist stats to file
                            try:
                                with open(ans_stat_path, 'w', encoding='utf-8') as file:
                                    file.write(f'{answer_stat}')
                                    print('Saved answer_stat:', answer_stat)
                            except Exception as e:
                                print('Exception writing answer_stat:', e)

                    except Exception as expt:
                        # handle any processing exceptions per-frame
                        print('Frame processing exception:', expt)
                        await websocket.send('EОшибка обработки кадра')

            except Exception as expt:
                # this captures per-message exceptions
                print('Message handling exception:', expt)
                try:
                    await websocket.send('EОшибка сервера при обработке сообщения')
                except Exception:
                    pass

    except websockets.exceptions.ConnectionClosedOK:
        print('Connection closed normally')
    except Exception as expt:
        print(f'ERROR in connection handler: {expt}')
    finally:
        # Ensure socket is removed from connected
        if websocket in connected:
            connected.remove(websocket)
        print('websocket closed \n')


async def main():
    # bind server
    async with websockets.serve(server, "localhost", 5000):
        print('websocket serve running on ws://localhost:5000')
        # keep server alive forever
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Server stopped by user')
