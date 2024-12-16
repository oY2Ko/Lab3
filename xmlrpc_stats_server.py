
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Lock
import datetime
import pandas
import sqlite3

connection = sqlite3.connect('log.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
operation TEXT NOT NULL,
datetime TEXT NOT NULL,
time TEXT NOT NULL
)
''')
cursor.close()
connection.commit()
connection.close()

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8018), 
                            requestHandler=RequestHandler)

# filename = "log.csv"
# max_length = 50
lock = Lock()

# def set_logs_max_length(length):
#     global lock
#     with lock:
#         global max_length
#         max_length = length
#         return True
# server.register_function(set_logs_max_length, 'set_logs_max_length')

# Добавление строки в лог
def add_log(sname, t:datetime):
    global lock

    with lock:
        connection = sqlite3.connect('log.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Logs (operation, datetime, time) VALUES (?, ?, ?)',
                       (sname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), t))
        cursor.close()
        connection.commit()
        connection.close()
        return True
server.register_function(add_log, 'add_log')
        
def get_log(operation, date_from, date_to, duration:float):
    connection = sqlite3.connect('log.db')
    cursor = connection.cursor()
    logs = cursor.execute("SELECT * FROM Logs")
    should_add = True
    logs_to_send = []
    for log in logs:
        if operation is not None:
            if operation != log[1]:
                should_add = False
        if date_to is not None and date_from is not None:
            if datetime.datetime.strptime(log[2], "%Y-%m-%d %H:%M:%S") < date_from or datetime.datetime.strptime(log[2], "%Y-%m-%d %H:%M:%S") > date_to:
                should_add = False
        if duration is not None:
            if float(log[3]) > duration:
                should_add = False
        if should_add:
            logs_to_send.append(log[1:])
        should_add = True
    print(logs_to_send)
    return logs_to_send
server.register_function(get_log, "get_log")


print ("Listening on port 8018...")
server.serve_forever()
