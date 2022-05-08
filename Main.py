from flask import Flask, request
from Function import Function as Fun
from Function import DebugConsole as DBC
from Function import GoCQHttpLog as GCQH
from threading import Thread
import os
from importlib import reload


app = Flask(__name__)

@app.route('/', methods=["POST"])
def PostData():##接收Json，传递给data
    data = request.get_json()
    if not 'interval' in data:
        Me = Fun.MessageProcess(data)
        statu = Me.MessageBypass()
        if statu == 'reload':
            reload(Fun)
    return 'OK'

def HTTP_Server():
    # 此处的 host和 port对应上面 yml文件的设置
    #保证和我们在配置里填的一致
    app.run(host='127.0.0.1', port=5710) 

def thread_start():##多线程（其实没必要）
    #Go_CQHttp = Thread(target=GCQH.CQhttp)
    HttpServer = Thread(target=HTTP_Server)
    Debug_Console = Thread(target=DBC.DebugConsole)

    #Go_CQHttp.start()
    HttpServer.start()
    Debug_Console.start()

    #Go_CQHttp.join()
    HttpServer.join()
    Debug_Console.join()

if __name__ == '__main__':
    os.system('color 02')
    thread_start()