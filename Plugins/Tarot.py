# -*- coding: utf-8 -*-
##Version 1.0.1##等待释义##更新随机数系统##

import os
import sys
import time as pause
import random
import sqlite3
import datetime
#import Paraphrase

'''[
Big_Akana[#解释命运的大致运势。],
Small_Akana_Leangle[#【权杖】（The Leangle）代表元素火，象征激情、能量和创造。],
Small_Akana_Garren[#【星币】（The Garren）代表元素土，象征金钱、物质和享受。],
Small_Akana_Chalice[#【圣杯】（The Chalice）代表元素水，象征情感、关系、爱和灵感。],
Small_Akana_Blade[#【宝剑】（The Blade）代表元素风，象征思想、智慧、交流和冲突。]
]'''
#小阿卡那牌是用来补足大阿卡那牌不足之处。
#若是我们想要更进一步知道命运的真相或是对方的事情。
#其中由侍从、骑士、皇后、国王组成的人物牌，也称为宫廷牌（Court cards）。
##全局变量##
Path = f'{os.getcwd()}\\Tarot_Data\\'
File = 'Tarot_Data.db'
Table = 'Tarot_Data'
Akana = [['0 愚人（The Fool）','Ⅰ 魔术师（The Magician）','Ⅱ 女教皇（The High Priestess）','Ⅲ 女皇（The Empress）','Ⅳ 皇帝（The Emperor）','Ⅴ 教皇（The Hierophant）','Ⅵ 恋人（The lovers）','Ⅶ 战车（The Chariot）','Ⅷ 力量（Strength）','Ⅸ 隐士（The Hermit）','Ⅹ 命运之轮（The Wheel of Fortune）','ⅩⅠ 正义（Justice）','ⅩⅡ 悬吊者（The Hanged Man）','ⅩⅢ 死神（Death）','ⅩⅣ 节制（Temperance）','ⅩⅤ 魔鬼（The Devil）','ⅩⅥ 高塔（The Tower）','ⅩⅦ 星星（The Star）','ⅩⅧ 月亮（The Moon）','ⅩⅨ 太阳（The Sun）','ⅩⅩ审判（Judgment）','ⅩⅩⅠ 世界（The World）'],['权杖王牌','权杖二','权杖三','权杖四','权杖五','权杖六','权杖七','权杖八','权杖九','权杖十','权杖侍卫','权杖骑士','权杖皇后','权杖国王',],['星币王牌','星币二','星币三','星币四','星币五','星币六','星币七','星币八','星币九','星币十','星币侍卫','星币骑士','星币皇后','星币国王',],['圣杯王牌','圣杯二','圣杯三','圣杯四','圣杯五','圣杯六','圣杯七','圣杯八','圣杯九','圣杯十','圣杯侍卫','圣杯骑士','圣杯皇后','圣杯国王'],['宝剑王牌','宝剑二','宝剑三','宝剑四','宝剑五','宝剑六','宝剑七','宝剑八','宝剑九','宝剑十','宝剑侍卫','宝剑骑士','宝剑皇后','宝剑国王']]
Bit = ['逆位','正位']
Version = 'Version_1.0.1'

def Premise():##数据库文件、路径状态判断模块##已完成##未测试##
    if not os.path.isfile(Path+File) :
        if not os.path.exists(Path) :
            return False
    else :
        return True

def New_Table(Pre):##占卜数据库新建模块##已完成##未测试##
    global Path,File,Table
    if Pre == False :
        os.makedirs(Path)
    New_Database = sqlite3.connect(Path+File)
    cur = New_Database.cursor()
    new_time = datetime.datetime.now()
    cur.execute(f'''
        Create table 
        {Table} (
        Datetime text Primary Key,
        User integer,
        First_Card text,
        Second_Card text,
        Third_Card text)''')
    cur.execute(f'insert into {Table} values(?,?,?,?,?)', (new_time,2602961063,'First Run','First Run','First Run'))
    New_Database.commit()
    New_Database.close()

def main():
    global user
    times = 1
    first,second,third = None,None,None
    x,y,z = Random()
    first = f'{Akana[x][y]} {Bit[z]}'
    ft = Akana[x][y]
    fx,fy,fz = x,y,z
    x,y,z = Random()
    second = f'{Akana[x][y]} {Bit[z]}'
    st = Akana[x][y]
    sx,sy,sz = x,y,z
    x,y,z = Random()
    third = f'{Akana[x][y]} {Bit[z]}'
    tt = Akana[x][y]
    tx,ty,tz = x,y,z
    while st == ft :
        x,y,z = Random()
        second = f'{Akana[x][y]} {Bit[z]}'
        sx,sy,sz = x,y,z
    while tt == ft :
        x,y,z = Random()
        third = f'{Akana[x][y]} {Bit[z]}'
        tx,ty,tz = x,y,z
    while tt == st :
        x,y,z = Random()
        third = f'{Akana[x][y]} {Bit[z]}'
        tx,ty,tz = x,y,z
    Output(first,fx,fy,fz,second,sx,sy,sz,third,tx,ty,tz)
    #print(f'{first},{fx},{fy},{fz}\n{second},{sx},{sy},{sz}\n{third},{tx},{ty},{tz}')

def Random():##随机取牌##
    x = random.randint(0,(len(Akana)-1)*random.randint(1,10))%len(Akana)
    y = random.randint(0,(len(Akana[x])-1)*random.randint(1,10))%len(Akana[x])
    z = random.randint(1,100)%2
    print(x,y,z)
    #pause.sleep(random.random())
    #print(time)
    return x,y,z

def Output(first,fx,fy,fz,second,sx,sy,sz,third,tx,ty,tz):
    User_Data_Write(first,second,third)
    print(f'[CQ:at,qq={user}]\n{first}\n{second}\n{third}\n{Version}')
    #Paraphrase

def User_Data_Write(first,second,third):##占卜数据写入模块##
    global user,Path,File,Table
    Database = sqlite3.connect(Path+File)
    cur = Database.cursor()
    time = datetime.datetime.now()
    cur.execute(f'insert into {Table} values(?,?,?,?,?)', (time,user,first,second,third))
    Database.commit()
    Database.close()

if __name__ == '__main__':
    global user
    user = sys.argv[-1]
    date = datetime.date.today()
    seed = f'{user}{date.year}{date.month}{date.day}'
    random.seed(seed)
    Pre = Premise()
    if not Pre == True :
        New_Table(Pre)
    main()
