
import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Lock
import datetime
import pandas as pd
import xmlrpc


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

log_server = xmlrpc.client.ServerProxy("http://localhost:8018/RPC2")
server = xmlrpc.client.ServerProxy("http://localhost:8008/RPC2")

proxy = SimpleXMLRPCServer(("localhost", 8000), 
                            requestHandler=RequestHandler)


def ping():
    t = time.time()
    res = server.ping()
    t = time.time() - t
    try:
        log_server.add_log('ping', t)
    except:
        pass
    return res
proxy.register_function(ping, 'ping')


# Время сервера
def now():
    t = time.time()
    res = server.now()
    t = time.time() - t
    try:
        log_server.add_log('now', t)
    except:
        pass
    return res
proxy.register_function(now, 'now')

# Отображение строкового вида, типа и значений
def show_type(arg):
    t = time.time()
    res = server.type(arg)
    t = time.time() - t
    try:
        log_server.add_log('type', t)
    except:
        pass
    return res
proxy.register_function(show_type, 'type')

# Сумма
def test_sum(a, b):
    t = time.time()
    res = server.sum(a, b)
    t = time.time() - t
    try:
        log_server.add_log('sum', t)
    except:
        pass
    return res
proxy.register_function(test_sum, 'sum')

# Степень
def test_pow(a, b):
    t = time.time()
    res = server.pow(a, b)
    t = time.time() - t
    try:
        log_server.add_log('pow', t)
    except:
        pass
    return res
proxy.register_function(test_pow, 'pow')

# Проверка нахождения клиента в черном списке c использованием Pandas Data Frame
def black_list_check(sname, name, patronym, date_of_birth: str):
    t = time.time()
    res = server.black_list_check(sname, name, patronym, date_of_birth)
    t = time.time() - t
    try:
        log_server.add_log('black_list_check', t)
    except:
        pass
    return res
proxy.register_function(black_list_check, 'black_list_check')

# Бинарная передача данных
def send_back_binary(bin_data):
    t = time.time()
    res = server.send_back_binary(bin_data)
    t = time.time() - t
    try:
        log_server.add_log('send_back_binary', t)
    except:
        pass
    return res
proxy.register_function(send_back_binary, 'send_back_binary')

# Инверсия цвета
# На вход изображение RGB размерности (M, N, 3) со значениями 0-255
def send_back_inversion(bin_data):
    t = time.time()
    res = server.color_inversion(bin_data)
    t = time.time() - t
    try:
        log_server.add_log('color_inversion', t)
    except:
        pass
    return res
proxy.register_function(send_back_inversion, 'color_inversion')

def binarization(bin_data, threshold:int):
    t = time.time()
    res = server.binarization(bin_data, threshold)
    t = time.time() - t
    try:
        log_server.add_log('binarization', t)
    except:
        pass
    return res
proxy.register_function(binarization, 'binarization')

def rotate(bin_data):
    t = time.time()
    res = server.rotate(bin_data)
    t = time.time() - t
    try:
        log_server.add_log('rotate', t)
    except:
        pass
    return res
proxy.register_function(rotate, 'rotate')

def get_log(operation, date_from, date_to, duration):
    res = log_server.get_log(operation, date_from, date_to, duration)
    return res
proxy.register_function(get_log, "get_log")

print("Listening on port 8000...")
proxy.serve_forever()