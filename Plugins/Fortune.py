##Version 5.0.0##以类方式重写##

import os
import re
import sys
import random
import sqlite3
import datetime
from requests_html import HTMLSession as html

class Fortune():
    def __init__(self,user):
        self.Path = './Data/Fortune_Data/'
        self.File = 'Fortune_Data.db'
        self.user = user
        Now = datetime.datetime.now()
        self.time = Now.strftime('%H:%M:%S')
        self.date = Now.strftime('%Y.%m.%d')
        self.main_num = 0
        self.extra_num = 0
        self.DB = None
        self.cur = None
        self.result = ''
        self.main_text = ['大凶','凶','末吉','吉','中吉','大吉']
        self.main_remark = ['换言之……也是一种幸运……喵……？（不确定的语气）', '今天请小心一点喵……', 
            '一切如常喵~', '运气还不错喵~', '今天也是幸运的一天喵~', '好幸运喵（★ω★）']

    def Main(self):
        self.Premise()
        self.Table_Exist()
        self.User_Data_Read()
        print(self.user,self.time,self.date,self.main_num, self.extra_num, self.DB,self.cur,'\n',self.result)
        return f'[CQ:at,qq={self.user}]\n{self.result}'

    def Premise(self):#数据库路径状态判断模块
        if not os.path.exists(self.Path) :
            os.makedirs(self.Path)
        if not os.path.isfile(f'{self.Path}{self.File}') :
            New_Database = sqlite3.connect(f'{self.Path}{self.File}')
            cursor = New_Database.cursor()
            cursor.execute(f'''
                Create table 
                \'{self.date}\' (
                User integer Primary Key,
                Time text,
                Main integer,
                Extra integer)''')
            cursor.execute(f'insert into \'{self.date}\' values(?,?,?,?)', (000000,0000,0,0))
            New_Database.commit()
            New_Database.close()
        self.DB = sqlite3.connect(f'{self.Path}{self.File}')
        self.cur = self.DB.cursor()

    def Table_Exist(self):#检查当天的表是否存在
        exist = self.cur.execute(f'select * from sqlite_master where type=\'table\' and name=\'{self.date}\'')
        exist = exist.fetchone()
        if exist == None :
            self.New_Table()

    def New_Table(self):
        self.cur.execute(f'''
            Create table 
            \'{self.date}\' (
            User integer Primary Key,
            Time text,
            Main integer,
            Extra integer)''')

    def User_Data_Read(self):
        data = self.cur.execute(f'select * from \'{self.date}\' where User={self.user}')
        Read_Data = data.fetchone()
        if Read_Data == None :
            self.Random(statu=True)
        else :
            self.user,self.time,self.main_num,self.extra_num = Read_Data
            self.Random(statu=False)
            self.Output(Statu=True)

    def Random(self, statu):
        if statu == True :
            self.main_num = random.randint(1,100)
            self.extra_num = random.randint(1,100)
        if self.main_num <= 5 :#1-5
            if self.main_num == 1 :
                self.Special()
            else :
                self.result += f'{self.main_text[0]}{self.Extra(5,True)}\n{self.main_remark[0]}'
        elif self.main_num <= 20 :#6-20
            self.result += f'{self.main_text[1]}{self.Extra(15,True)}\n{self.main_remark[1]}'
        elif self.main_num <= 50 :#21-50
            self.result += f'{self.main_text[2]}{self.Extra(30,False)}\n{self.main_remark[2]}'
        elif self.main_num <= 80 :#51-80
            self.result += f'{self.main_text[3]}{self.Extra(30,False)}\n{self.main_remark[3]}'
        elif self.main_num <= 95 :#81-95
            self.result += f'{self.main_text[4]}{self.Extra(15,False)}\n{self.main_remark[4]}'
        else :#96-100
            if self.main_num == 100 :
                self.Special()
            else :
                self.result += f'{self.main_text[5]}{self.Extra(5,False)}\n{self.main_remark[5]}'
        if statu == True :
            self.User_Data_Write()
        else:
            return f'[CQ:at,qq={self.user}]\n{self.result}'

    def Special(self):##额外判定逻辑模块
        review = ['\n这……请吃好喝好……注意天空，注意地面……（默哀脸）',
        '\n喵↑？你真的没有作弊吗？（怀疑的目光）','\n换言之……也是一种幸运呢……','\n好幸运喵（★ω★）']
        x = 1
        y = 3
        if self.main_num == 1 :
            result = '大凶'
            x = 0
            y = 2
        else :
            result = '大吉' 
        if self.extra_num == self.main_num :
            self.result += f' Ex\n{review[x]}'
        else :
            self.result += f' +\n{review[y]}'

    def Extra(self, main_Extra, judg):##二阶判定模块
        second = ['Ex','+','','-']
        if self.extra_num <= main_Extra :
            re = 3
        elif self.extra_num >= 100-main_Extra :
            re = 1
        else :
            re = 2
        if judg == True :
            re = 0-re
        return second[re]

    def User_Data_Write(self):
        self.cur.execute(f'insert into \'{self.date}\' values(?,?,?,?)', (self.user,self.time,self.main_num,self.extra_num))
        self.DB.commit()
        self.Output(Statu=False)

    def Output(self, Statu):##输出##
        ST=self.Solar_Terms()
        self.DB.close()
        if Statu == True:
            self.result += f'\n\n你今天{self.time}已经抽过了的说……（轻轻戳手指……）'
        else:
            self.result += f'\n\n{ST}'

    def Solar_Terms(self):
        date = datetime.date.today()
        year,month,day = date.year,date.month,date.day
        if self.cur.execute(f'select * from sqlite_master where type=\'table\' and name = \'Solar_Terms\'').fetchone() == None:
            self.cur.execute(f'''
            Create table 
            Solar_Terms (
            ID integer Primary Key,
            Date text,
            ST text)''')
            self.DB.commit()
            try:
                for year in range(2021,2025):
                    url = f"https://jieqi.supfree.net/cntv.asp?n={year}"
                    web = html().get(url)
                    elem = web.html.find('table',first=True)
                    #print(elem.text)
                    if elem == None:
                        break
                    req = re.findall(r'(.{2})\n([0-9]{0,2})月([0-9]{0,2})日',elem.text)
                    ST = 0
                    for ST in range(0,24):
                        Solar_Terms = req[ST][0]
                        date = f'{year}-{req[ST][1]}-{req[ST][2]}'
                        self.cur.execute(f'insert into Solar_Terms values(NULL,?,?)', (date,Solar_Terms))
                    self.DB.commit()
            except:
                print('Web Error.')
        data = self.cur.execute(f'select ST from Solar_Terms where date=\'{year}-{month}-{day}\'')
        Read_Data = data.fetchone()
        if Read_Data == None:
            return ''
        else:
            return f'今天是{Read_Data[0][0:3]}哦……'

if __name__ == '__main__':
    s = Fortune(123456)
    s.Main()