import re
import json
import random
#import hashlib
import requests


class MessageProcess():
    def __init__(self,Json):
        self.Json = Json
        self.SendMessage = ''
        self.message_source = ''
        if not 'interval' in Json:
        #筛选接收到的消息
            self.post_type = Json['post_type']
            self.self_id = Json['self_id']
            self.sub_type = Json['sub_type']
            self.time = Json['time']
            #共用数据
            if self.sub_type == 'poke':
            #戳一戳Json的格式化
                if 'group_id' in Json:
                #群组独占
                    self.message_source = 'group'
                    self.group_id = Json['group_id']
                else:
                    self.message_source = 'private'
                self.target_id = Json['target_id']
                self.sender_id = Json['sender_id']
                #戳一戳共用数据
            elif self.post_type == 'message':
                print(self.sub_type)
            #消息Json的格式化
                self.font = Json['font']
                self.message_id = Json['message_id']
                self.message = Json['message']
                self.message_type = Json['message_type']
                self.raw_message = Json['raw_message']
                self.sender_age = Json['sender']['age']
                self.sender_nickname = Json['sender']['nickname']
                self.sender_sex = Json['sender']['sex']
                self.sender_id = Json['sender']['user_id']
                #消息共用数据
                if self.message_type == 'group':
                    print(self.message_type)
                #群组独占
                    self.message_source = 'group'
                    self.anonymous = Json['anonymous']
                    self.group_id = Json['group_id']
                    self.sender_area = Json['sender']['area']
                    self.sender_card = Json['sender']['card']
                    self.sender_level = Json['sender']['level']
                    self.sender_role = Json['sender']['role']
                    self.sender_title = Json['sender']['title']
                else:
                #私聊独占
                    self.message_source = 'private'
                    self.target_id = Json['target_id']

    def ResourceExtraction(self):
        imagere = '\[CQ:image,file=([a-fA-F0-9]{32}).image'
        audiore = '\[CQ:record,file=([a-fA-F0-9]{32}).amr'
        facere = '\[CQ:face,id=([0-9]{1,3})\]'
        pass

    def MessageBypass(self):
        if self.sub_type == 'poke':
            MessageProcess.Poke(self)
        elif self.message_source == 'group':
            MessageProcess.GroupMessage(self)
        elif self.message_source == 'private':
            MessageProcess.PrivateMessage(self)

    def Poke(self):
        self.SendMessage = f'It\'s a poke by {self.sender_id}.'
        MessageProcess.MessageSend(self)

    def GroupMessage(self):
        self.SendMessage = f'It\'s a group message by {self.group_id} group and {self.sender_id} user.'
        MessageProcess.MessageSend(self)

    def PrivateMessage(self):
        self.SendMessage = f'It\'s a private message by {self.sender_id}.'
        MessageProcess.MessageSend(self)

    def MessageSend(self):
        if self.message_source == 'group':
            result = requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={self.group_id}&message={self.SendMessage}')
        else:
            result = requests.get(url=f'http://127.0.0.1:5700/send_private_msg?user_id={self.sender_id}&message={self.SendMessage}')
        print(result)

def Data(data):
    if not 'interval' in data:
        print(data)
        me = MessageProcess(data)
        me.MessageBypass()
    if 'message_type' in data:
        if data['message_type'] == 'group':  # 如果是群聊信息
            gid = data['group_id']  # 获取群号
            uid = data['sender']['user_id']  # 获取信息发送者的 QQ号码
            message = data['raw_message']  #获取原始信息
            print(f'Group Msg:\tuid={uid}\tgid={gid}')
            keyword(message, uid, gid)  # 将 Q号和原始信息传到我们的后台
        elif data['message_type'] == 'private':
            uid = data['sender']['user_id']
            msg = data['raw_message']
            print(f'Private Msg:\tuid={uid}')
            keyword(msg,uid,gid=0)
        #print(f'https://gchat.qpic.cn/gchatpic_new/0/0-0-{u}/0?term=2')
    else:
        print("No Data.")
    

#'下面这个函数用来判断信息开头的几个字是否为关键词'
def keyword(message, uid, gid):
    if gid != 0 and message[0:2] == '你好':
        group_send(uid,gid,"你也好啊!@#$%^&*()_+！")
    elif re.match(r'.*？.*',message) != None:
        private_send(uid,message)
 
def group_send(uid, gid, message):
    '''群消息'''
    message = str(message)
    sign = {"&": "%26", "+": "%2B", "#": "%23"}
    print(f'Group Send:\tuid={uid}\tgid={gid}')
    for i in sign:
        message = message.replace(i, sign[i]) #防止在请求中特殊符号出现消息错误
    if uid != 0:
        message = f"[CQ:at,qq={uid}]\n+{message}" #CQ码，这里是at某人的作用
    requests.get(url=f'http://127.0.0.1:5700/send_msg?message_type=group&group_id={gid}&message={message}')
    #发送群消息的api，前面的地址保证和配置中的一直

def private_send(uid,msg):
    msg = str(msg)
    sign = {"&": "%26", "+": "%2B", "#": "%23"}
    print(f'Private Send:\tuid={uid}\tMsg={msg}')
    for i in sign:
        msg = msg.replace(i, sign[i])
    js = requests.get(url=f'http://127.0.0.1:5700/send_msg?message_type=private&user_id={uid}&message={msg}')
    js=js.text.encode()
    requests.get(url=f'http://127.0.0.1:5700/send_msg?message_type=private&user_id={uid}&message=[欢迎]')

