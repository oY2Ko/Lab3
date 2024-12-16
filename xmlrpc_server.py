# xmlrpc_server.ipynb

import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc
import datetime
import PIL
import PIL.Image
from matplotlib import pyplot as plt
import pandas as pd
import pickle
import numpy as np

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8008), 
                            requestHandler=RequestHandler)

# Тест
def ping():
    return True
server.register_function(ping, 'ping')


# Время сервера
def now():
    return datetime.datetime.now()
server.register_function(now, 'now')

# Отображение строкового вида, типа и значений
def show_type(arg):
    return (str(arg), str(type(arg)), arg)
server.register_function(show_type, 'type')

# Сумма
def test_sum(a, b):
    return a + b
server.register_function(test_sum, 'sum')

# Степень
def test_pow(a, b):
    return a**b
server.register_function(test_pow, 'pow')

# Проверка нахождения клиента в черном списке c использованием Pandas Data Frame
def black_list_check(sname, name, patronym, date_of_birth: str):
    frame = pd.read_csv('bad_boys2.csv', header=0, sep=',', encoding='utf8')
    result = frame.loc[(frame['Surname'] == sname) & (frame['Name'] == name) & (frame['Patronym'] == patronym)
                      & (frame['Birth'] == date_of_birth)]
    
    if (not result.empty):
        return sname + ": "+ "bad_boy"
    else:
        return sname + ": "+ "good_boy"

server.register_function(black_list_check, 'black_list_check')

# Бинарная передача данных
def send_back_binary(bin_data):
    data = bin_data.data
    return xmlrpc.client.Binary(data)
server.register_function(send_back_binary, 'send_back_binary')

# Инверсия цвета
# На вход изображение RGB размерности (M, N, 3) со значениями 0-255
def send_back_inversion(bin_data):
    img_arr = pickle.loads(bin_data.data)
    img_arr = np.array(img_arr)
    
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    channels = 3 if len(img_arr.shape) == 3 else 1
    
    if channels == 3:
        for i in range(height):
            for j in range(width):
                img_arr[i][j][0] = 255 - img_arr[i][j][0]
                img_arr[i][j][1] = 255 - img_arr[i][j][1]
                img_arr[i][j][2] = 255 - img_arr[i][j][2]
    if channels == 1:
        for i in range(height):
            for j in range(width):
                img_arr[i][j] = 255 - img_arr[i][j]
    
    pimg = pickle.dumps(img_arr)        
    return xmlrpc.client.Binary(pimg)
server.register_function(send_back_inversion, 'color_inversion')

def binarization(bin_data, threshold:int):
    img_arr = pickle.loads(bin_data.data)
    img_arr = np.array(img_arr)
    
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    channels = 3 if len(img_arr.shape) == 3 else 1
    
    if channels == 3:
        for i in range(height):
            for j in range(width):
                s =np.sum(img_arr[i][j])
                if s/3 < threshold:
                    img_arr[i][j] = np.zeros((3))
                else:
                    img_arr[i][j] = np.ones((3))*255
    if channels == 1:
        for i in range(height):
            for j in range(width):
                if img_arr[i][j] < threshold:
                    img_arr[i][j] = 0
                else:
                    img_arr[i][j] = 255
    pimg = pickle.dumps(img_arr)        
    return xmlrpc.client.Binary(pimg)
server.register_function(binarization, 'binarization')

def rotate(bin_data):
    img_arr = pickle.loads(bin_data.data)
    img_arr = np.array(img_arr)
    
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    channels = 3 if len(img_arr.shape) == 3 else 1
    
    rotated_img = np.zeros((width, height, channels))
    for i in range(width):
        for j in range(height):
            rotated_img[i][j] = img_arr[j][i]
            
    # p= PIL.Image.fromarray(rotated_img)
    # plt.imshow(rotated_img)
    # time.sleep(0.5)
    # plt.show()

    pimg = pickle.dumps(rotated_img/255)        
    return xmlrpc.client.Binary(pimg)
server.register_function(rotate, 'rotate')

print("Listening on port 8008...")
server.serve_forever()
