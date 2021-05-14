import cv2
import ctypes
import time
import random
from math import sin, cos, radians
import cv2
import time
import random
from math import sin, cos, radians
camera =  cv2.VideoCapture(0)
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
random.seed()
questions = []
answers = []
answers_var= []
intfacts = []
answers_stat=[]
spec_tasks = []
gameOver = True
with open('questions.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    questions = [i for i in data]
with open('answers_var.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    answers_var = [i for i in data]
with open('intfacts.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    intfacts = [i for i in data]
with open('answers_stat.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    for i in range(0, len(data) - 1):
        answers_stat.append(int(data[i]))
with open('spec_tasks.txt', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    spec_tasks = [i for i in data]
with open('answers_stat.txt', 'w', encoding='utf-8') as file:
    file.write('')

settings_face = {
    'scaleFactor': 1.3, 
    'minNeighbors': 3, 
    'minSize': (50, 50), 
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

def sptas():
    timeout = time.time() + 5
    while True:
        ret_flip, img_flip = camera.read()
        ret = cv2.flip(ret_flip,1)
        img = cv2.flip(img_flip,1)
        
        cv2.rectangle(img, (0, 0), (640, 480), (103,207,254), -1)
        cv2.putText(img, spec_tasks[b], (55,190), cv2.FONT_HERSHEY_COMPLEX, 0.8, (59,32,13), 2)
        cv2.putText(img, "Нажмите клавишу 'J' для продолжения", (106,460), cv2.FONT_HERSHEY_COMPLEX, 0.6, (59,32,13), 2)
        cv2.putText(img, "Интересный факт:", (25,310), cv2.FONT_HERSHEY_COMPLEX, 0.6, (59,32,13), 2)
        cv2.putText(img, intfacts[c], (25,350), cv2.FONT_HERSHEY_COMPLEX, 0.6, (59,32,13), 2)
        cv2.imshow('facedetect', img)

        if cv2.waitKey(1) & 0xff == ord('j'):
            break

while True:
    ret_flip, img_flip = camera.read()
    ret = cv2.flip(ret_flip,1)
    img = cv2.flip(img_flip,1)
    cv2.rectangle(img, (0, 0), (640, 480), (103,207,254), -1)
    cv2.putText(img, "Инструкция:", (25, 55), cv2.FONT_HERSHEY_COMPLEX , 0.65, (59,32,13), 2)
    cv2.putText(img, "1.Займите удобное положение", (25, 90), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    cv2.putText(img, "2.Убедитесь в наличие свободного пространства", (25, 120), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    cv2.putText(img, "3.Для начала нажмите на 'f'", (25, 150), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    cv2.putText(img, "4.Убедитесь в наличии достаточного количества", (25, 180), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    cv2.putText(img, "света", (45, 210), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    # cv2.putText(img, "Предупреждение:", (25, 380), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    # cv2.putText(img, "Правила игры:", (25, 185), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
    cv2.imshow('facedetect', img)
    if cv2.waitKey(1) & 0xff == ord('f'):
        break
while True:
    ret_flip, img_flip = camera.read()
    ret = cv2.flip(ret_flip,1)
    img = cv2.flip(img_flip,1)

    cv2.rectangle(img, (0, 430), (640,480), (103,207,254),-1)
    cv2.putText(img, "Нажмите клавишу 'o', если заняли удобную позицию", (30,460), cv2.FONT_HERSHEY_COMPLEX, 0.6, (59,32,13), 2)
    cv2.rectangle(img, (0, 0), (640,50), (103,207,254),-1)
    cv2.putText(img, "Расположите лицо в центре экрана", (70, 30), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)

    for angle in [0, -55, 55]:
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings_face)
        if len(detected):
            detected = [rotate_point(detected[-1], img, -angle)]
            break

    for x, y, w, h in detected[-1:]:
        img_facepro = rimg[y:y+h, x:x+w]
    cv2.imshow('facedetect', img)

    if cv2.waitKey(1) & 0xff == ord('o'):
        stx = x
        sty = y
        break
print("x = ", x, "y = ", y,"width= ", w,"height= ", h )    
temp = 0
temp2 = 0
temp3 = 0
schet = 0
while gameOver == True:
    b = random.randint(0, len(spec_tasks)-1)
    while spec_tasks[b] == '#':
        b += 1
        if b == len(spec_tasks):
            b = 0
            temp2 += 1
        if temp2 >= 50:
            break
    if schet == 3:
        sptas()
        schet = schet - 3
        spec_tasks[b] = '#'
        continue
    schet += 1

    c = random.randint(0, len(intfacts)-1)
    while intfacts[c] == '#':
        c += 1
        if c == len(spec_tasks):
            c = 0
            temp3 += 1
        if temp3 >= 50:
            break

    a = random.randint(0, len(questions)-1)
    while questions[a] == '#':
        a += 1
        if a == len(questions):
            a = 0
            temp += 1
        if temp >= 50:
            gameOver = False
            break
    if gameOver == False:
        continue
    while True:
        ret_flip, img_flip = camera.read()
        ret = cv2.flip(ret_flip,1)
        img = cv2.flip(img_flip,1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0))
        cv2.rectangle(img, (0, 0), (640, 50), (103,207,254), -1)
        cv2.putText(img, questions[a], (70,30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (59,32,13), 2)
        cv2.circle(img, (100, 110), 50, (103, 207, 254), -1)
        cv2.circle(img, (540, 110), 50, (103, 207, 254), -1)
        cv2.putText(img, answers_var[a*2+1], (60,110), cv2.FONT_HERSHEY_COMPLEX, 0.5, (59,32,13), 2)
        cv2.putText(img, answers_var[a*2], (500,110), cv2.FONT_HERSHEY_COMPLEX, 0.5, (59,32,13), 2)   

        for angle in [0, -55, 55]:
            rimg = rotate_image(img, angle)
            detected = face.detectMultiScale(rimg, **settings_face)
            if len(detected):
                detected = [rotate_point(detected[-1], img, -angle)]
                break
        for x, y, w, h in detected[-1:]:
            img_facepro = rimg[y:y+h, x:x+w]
        if x < stx-35 and y > sty+20:
            print("left")  
            questions[a] = "#"
            answers_stat[a*2 + 1] += 1
            with open('answers_stat.txt', 'a', encoding='utf-8') as file:
                file.write(str(answers_stat[a*2]))
                file.write("\n")
                file.write(str(answers_stat[a*2+1]))
                file.write("\n")
            while cv2.waitKey(1) & 0xff != ord('u'):
                ret_flip, img_flip = camera.read()
                ret = cv2.flip(ret_flip,1)
                img = cv2.flip(img_flip,1)
                procentp = int(answers_stat[a*2]/(answers_stat[a*2]+answers_stat[a*2+1])*100)
                procentl = 100 - procentp
                cv2.rectangle(img, (0, 0), (640, 50), (103,207,254), -1)
                cv2.putText(img,str(procentl)+"%"+"("+str(answers_stat[a*2+1])+")", (100, 30), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
                cv2.putText(img,str(procentp)+"%"+"("+str(answers_stat[a*2])+")", (430, 30), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
                cv2.rectangle(img, (0, 430), (640,480), (103,207,254),-1)
                cv2.putText(img, "Нажмите клавишу 'u'", (140,460), cv2.FONT_HERSHEY_COMPLEX, 0.8, (59,32,13), 2)
                cv2.line(img, (330, 8), (310, 42), (59,32,13), 3)  
                for angle in [0, -50, 50]:
                    rimg = rotate_image(img, angle)
                    detected = face.detectMultiScale(rimg, **settings_face)
                    if len(detected):
                        detected = [rotate_point(detected[-1], img, -angle)]
                        break

                for x, y, w, h in detected[-1:]:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0))
                    img_facepro = rimg[y:y+h, x:x+w]
                cv2.imshow('facedetect', img)
            break
        if x + w > stx + w + 35 and y > sty + 35:
            print("right")    
            questions[a] = "#"
            answers_stat[a*2] += 1
            with open('answers_stat.txt', 'a', encoding='utf-8') as file:
                file.write(str(answers_stat[a*2]))
                file.write("\n")
                file.write(str(answers_stat[a*2+1]))
                file.write("\n")
            while cv2.waitKey(1) & 0xff != ord('u'):
                ret_flip, img_flip = camera.read()
                ret = cv2.flip(ret_flip,1)
                img = cv2.flip(img_flip,1)
                procentp = int(answers_stat[a*2]/(answers_stat[a*2]+answers_stat[a*2+1])*100)
                procentl = 100 - procentp
                cv2.rectangle(img, (0, 0), (640, 50), (103,207,254), -1)
                cv2.putText(img,str(procentl)+"%"+"("+str(answers_stat[a*2+1])+")", (100, 30), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
                cv2.putText(img,str(procentp)+"%"+"("+str(answers_stat[a*2])+")", (430, 30), cv2.FONT_HERSHEY_COMPLEX, 0.65, (59,32,13), 2)
                cv2.rectangle(img, (0, 430), (640,480), (103,207,254),-1)
                cv2.putText(img, "Нажмите клавишу 'u'", (140,460), cv2.FONT_HERSHEY_COMPLEX, 0.8, (59,32,13), 2)
                cv2.line(img, (330, 8), (310, 42), (59,32,13), 3)
                for angle in [0, -50, 50]:
                    rimg = rotate_image(img, angle)
                    detected = face.detectMultiScale(rimg, **settings_face)
                    if len(detected):
                        detected = [rotate_point(detected[-1], img, -angle)]
                        break

                for x, y, w, h in detected[-1:]:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0))
                    img_facepro = rimg[y:y+h, x:x+w]
                cv2.imshow('facedetect', img)
            break
        cv2.imshow('facedetect', img)
         
        if cv2.waitKey(1) & 0xff == ord('f'):
            questions[a] = "#"
            break

cv2.destroyWindow("facedetect")