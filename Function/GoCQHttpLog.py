import os

def CQhttp():
    ##外部执行cqhttp
    #os.system('cd ./go-cqhttp && start start.bat')
    ##内部执行cqhttp
    print('GCQH')
    os.system('cd ./go-cqhttp && go-cqhttp.exe -faststart')