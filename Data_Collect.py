import cv2
import uuid
import os
import time

#image labels and count
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
img_count = 5

#directory setup
dir_path = 'C:/Users/luigi/sign_lang_ai'
data_path = os.path.join(dir_path, 'img_dataset')

if not os.path.exists(data_path):
    os.makedirs(data_path)


for label in labels:
    path = os.path.join(data_path, label)
    if not os.path.exists(path):
        os.makedirs(path)

#collect images from webcam
for label in labels:
    cap = cv2.VideoCapture(0)
    print('Getting images for {}'.format(label))
    time.sleep(5)
    for image in range(img_count):
        print('Capturing image {}'.format(image))
        ret, frame = cap.read()
        imgname = os.path.join(data_path,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()