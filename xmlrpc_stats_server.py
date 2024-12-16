
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Lock
import datetime
import pandas


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8018), 
                            requestHandler=RequestHandler)

filename = 'log_20220916_150531.csv'
max_length = 50
lock = Lock()

def set_logs_max_length(length):
    global lock
    with lock:
        global max_length
        max_length = length
        return True
server.register_function(set_logs_max_length, 'set_logs_max_length')

# Добавление строки в лог
def add_log(sname):
    global lock
    with lock:
        global max_length
        global filename
        csv = pandas.read_csv(filename, sep=',', header=None)
        print(csv)
        length = len(csv)
        dt = datetime.datetime.now()
        if length >= max_length:    
            filename = f'log_{dt.strftime("%Y%m%d_%H%M%S")}.csv'
        csv = pandas.DataFrame({'operation': [sname], 'datetime': [dt.strftime("%Y-%m-%d %H:%M:%S")]})
        csv.to_csv(filename, index=False, mode='a', sep=",",encoding='utf-8', header=False)
        return True
        
        
server.register_function(add_log, 'add_log')


print ("Listening on port 8018...")
server.serve_forever()
