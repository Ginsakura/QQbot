from flask import Flask, request
from Data import Function as Fun
from threading import Thread
import os


app = Flask(__name__)

@app.route('/', methods=["POST"])
def PostData():##接收Json，传递给data
    data = request.get_json()
    Fun.Data(data)
    return 'OK'

def HTTP_Server():
    # 此处的 host和 port对应上面 yml文件的设置
    #保证和我们在配置里填的一致
    app.run(host='127.0.0.1', port=5710) 

def CQhttp():
    ##外部执行cqhttp
    os.system('cd ./go-cqhttp && start start.bat')
    ##内部执行cqhttp
    #os.system('cd ./go-cqhttp && go-cqhttp.exe faststart')

def DebugConsole():
    pass

def thread_start():##双线程（其实没必要）
    Go_CQHttp = Thread(target=CQhttp)
    HttpServer = Thread(target=HTTP_Server)
    Debug_Console = Thread(target=DebugConsole)

    #Go_CQHttp.start()
    HttpServer.start()
    #Debug_Console.start()

    #Go_CQHttp.join()
    HttpServer.join()
    #Debug_Console.join()

if __name__ == '__main__':
    os.system('color 02')
    thread_start()