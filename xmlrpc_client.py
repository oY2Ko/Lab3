import datetime
import time
import xmlrpc.client
from PIL import Image # Работа с изображением
import PIL
import PIL.Image
import matplotlib # Отображение
import matplotlib.pyplot as plt
import xmlrpc

import matplotlib.pyplot


img = Image.open('Jellyfish.jpg')

img_arr = img

# Исходное изображение
plt.imshow(img_arr)
time.sleep(0.5)
plt.show()

# xmlrpc_client.ipynb

import xmlrpc
import pickle
import pandas as pd


server = xmlrpc.client.ServerProxy("http://localhost:8008/RPC2")
print('Ping:', server.ping())

print ('Server datetime:', server.now())

print ('View, type, value:', server.type(2))
print ('View, type, value:', server.type(2.))
print ('View, type, value:', server.type('My string'))
print ('View, type, value:', server.type("My string"))
print ('View, type, value:', server.type([1,2,3]))
print ('View, type, value:', server.type(["one", "two", "three"]))
print ('View, type, value:', server.type((1,2,"3")))

print ('Sum 2 + 3 :', server.sum(2, 3))
print ('Pow 2^3: ', server.pow(2, 3))

# Тест бинарной передачи данных
#pimg = img_arr.dumps()
pimg = pickle.dumps(img_arr) # универсально

img_bin = xmlrpc.client.Binary(pimg)

img_bin2 = server.send_back_binary(img_bin)

#img_arr2 = np.loads(img_bin2.data)
img_arr2 = pickle.loads(img_bin2.data) # универсально

# Изображение после возрата с сервера
plt.imshow(img_arr)
time.sleep(0.5)
plt.show()

# Инверсия цвета изображения через сервер
def inv_color(img_arr_in):
    pimg = pickle.dumps(img_arr_in)
    img_bin = xmlrpc.client.Binary(pimg)
    
    img_bin2 = server.color_inversion(img_bin)
    
    img_arr_out = pickle.loads(img_bin2.data)
    return img_arr_out

img_arr_inv = inv_color(img_arr)

# Изображение с инверсией цвета
plt.imshow(img_arr_inv)
time.sleep(0.5)
plt.show()

grayscale = Image.open('11.bmp')
img_arr_inv = inv_color(grayscale)

# Изображение с инверсией цвета
plt.imshow(img_arr_inv)
time.sleep(0.5)
plt.show()

print(server.black_list_check(u'Петров', "Иван", "Петрович", "07.08.1985"))
print(server.black_list_check(u'Примеров',"Михаил", "Викторович", "13.02.1992"))

# бинаризация
def binarization(img_arr_in):
    pimg = pickle.dumps(img_arr_in)
    img_bin = xmlrpc.client.Binary(pimg)
    
    img_bin2 = server.binarization(img_bin, 128)
    
    img_arr_out = pickle.loads(img_bin2.data)
    return img_arr_out

binarized = binarization(img_arr)
plt.imshow(binarized)
time.sleep(0.5)
plt.show()

#Поворот изображения
def rotate(img_arr_in):
    pimg = pickle.dumps(img_arr_in)
    img_bin = xmlrpc.client.Binary(pimg)
    
    img_bin2 = server.rotate(img_bin)
    
    img_arr_out = pickle.loads(img_bin2.data)
    image = PIL.Image.fromarray(img_arr_out, "RGB")
    return img_arr_out

rotated_img = rotate(img_arr)

# cv2.imshow('rotated_img', rotated_img)
# cv2.waitKey(0)

plt.imshow(rotated_img)
time.sleep(0.5)
plt.show()
