import re
import os
import json
import random
#import hashlib
import requests
from Plugins import Fortune,Cloudmusic
import base64
import sqlite3
from urllib import parse



class MessageProcess():
    def __init__(self,Json):
        self.Json = Json
        self.SendMessage = ''
        self.message_source = ''
        #筛选接收到的消息
        self.font = ''
        self.sub_type = Json['sub_type']#消息子类型
        self.post_type = Json['post_type']#消息类型
        self.message_id = ''
        self.message_type = ''
        self.raw_message = ''
        self.sender_age = ''
        self.sender_nickname = ''
        self.sender_sex = ''
        self.sender_id = ''
        self.SubID = ''
        self.target_id = ''
        self.self_id = Json['self_id']#botQQID
        self.time = Json['time']#消息发送时间（Unix）
        #共用数据
        if self.sub_type == 'poke':
        #戳一戳Json的格式化
            if 'group_id' in Json:
                self.message_source = 'group'
                self.group_id = Json['group_id']
            else:
                self.message_source = 'private'
            self.target_id = Json['target_id']
            self.sender_id = Json['sender_id']
            #戳一戳共用数据
        elif self.post_type == 'message':
        #消息Json的格式化
            self.sub_type = self.post_type
            self.font = Json['font']
            self.message_id = Json['message_id']
            self.message_type = Json['message_type']
            self.raw_message = Json['raw_message']
            self.sender_age = Json['sender']['age']
            self.sender_nickname = Json['sender']['nickname']
            self.sender_sex = Json['sender']['sex']
            self.sender_id = Json['sender']['user_id']
            #消息共用数据
            if self.message_type == 'group':
            #群组独占
                self.message_source = 'group'
                self.anonymous = Json['anonymous']
                self.group_id = Json['group_id']
                self.sender_area = Json['sender']['area']
                self.sender_group_nickname = Json['sender']['card']#群昵称
                self.sender_level = Json['sender']['level']
                self.sender_role = Json['sender']['role']#用户权限'admin' 'owner'
                self.sender_title = Json['sender']['title']#称号
            else:
            #私聊独占
                self.target_id = Json['target_id']
                self.message_source = 'private'
        self.SubID = f'{self.message_id}{self.sender_id}'

    def ResourceExtraction(self):
        imagere = '\[CQ:image,file=([a-fA-F0-9]{32}).image'
        audiore = '\[CQ:record,file=([a-fA-F0-9]{32}).amr'
        facere = '\[CQ:face,id=([0-9]{1,3})\]'

    def MessageBypass(self):
        #self.SQL_Write()
        #消息类型判断
        #if self.sub_type == 'poke':
        #    MessageProcess.Poke(self)
        #elif self.message_source == 'group':
        #    MessageProcess.GroupMessage(self)
        #elif self.message_source == 'private':
        #    MessageProcess.PrivateMessage(self)
        if self.raw_message == '今日运势':
            fortuneD = Fortune.Fortune(self.sender_id)
            self.SendMessage = fortuneD.Main()
            self.MessageSend()
        elif '网易云点歌' in self.raw_message:
            CM = Cloudmusic.Cloudmusic(self.sender_id,self.raw_message)
            self.SendMessage = CM.Main()
            self.MessageSend()
        elif self.raw_message == 'image':
            with open('./go-cqhttp/data/images/t.png','rb') as img:
                imgD = img.read()
                b64 = base64.b64encode(imgD)
                b64_str = parse.urlencode({'file':f'base64://{b64.decode()}'})
                self.SendMessage = f'[CQ:image,{b64_str}]'
            self.MessageSend()
        elif self.raw_message == 't':
            self.SendMessage = 'text1231454'
            self.MessageSend()
        elif self.raw_message == 'reload' :
            if not self.sender_id == 2602961063:
                self.SendMessage = 'No Purview.'
                self.MessageSend()
            else:
                self.SendMessage = 'Function Reloading...'
                self.MessageSend()
                return 'reload'

    def SQL_Write(self):
        DB = sqlite3.connect('./Data/Message.db')
        cur = DB.cursor()
        cur.execute('insert into message values(NULL,?,?,?,?,?,?,?,?,?,?,?)', (self.font,self.sub_type,self.message_id,self.message_type,self.raw_message,self.sender_age,self.sender_nickname,self.sender_sex,self.sender_id,self.SubID,self.target_id,self.self_id,self.time))
        if self.message_type == 'group':
            cur.execute('insert into group_message values(?,?,?,?,?,?,?,?)', (self.SubID,self.anonymous,self.group_id,self.sender_area,self.sender_group_nickname,self.sender_level,self.sender_role,self.sender_title))
        DB.commit()
        DB.close()

    def Poke(self):
        #戳一戳
        self.SendMessage = f'It\'s a poke by {self.sender_id}.'
        MessageProcess.MessageSend()

    def GroupMessage(self,):
        #群组消息
        self.SendMessage = f'It\'s a group message by {self.group_id} group and {self.sender_id} user.'
        MessageProcess.MessageSend()

    def PrivateMessage(self):
        #私聊消息
        self.SendMessage = f'It\'s a private message by {self.sender_id}.'
        MessageProcess.MessageSend()

    def MessageSend(self):
        #消息发送
        if self.message_source == 'group':
            result = requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={self.group_id}&message={self.SendMessage}')
        else:
            result = requests.post(url=f'http://127.0.0.1:5700/send_private_msg?user_id={self.sender_id}&message={self.SendMessage}')
        print(result)
