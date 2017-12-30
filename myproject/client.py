#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import wx
import telnetlib
import sys
import _thread as thread
from time import sleep
from random import randint, random

class Data:
    def __init__(self, name, sleep_time=3):
        self.name = name
        self.sleep_time = sleep_time
        self.login()
        self.receive()
        print("asd")
        # self.send()
    
    def login(self):
        print("login")
        con.open("127.0.0.1", port=6666, timeout=10)
        con.write(('login '+ str(self.name) + '\r\n').encode("utf-8"))
    
    def send(self):
        # while(1):
        print("senddata")
        heartbeat_freq = randint(50,110)
        blood_pressure = randint(50, 180)
        temper = 36 + random()*6
        con.write(('senddata ' + str(self.name) + ' ' 
                + str(blood_pressure) + ' '
                + str(heartbeat_freq) + ' ' 
                + str(temper) + '\r\n').encode("utf-8"))
        # sleep(self.sleep_time)
    
    def receive(self):
        # 接受服务器的消息
        thread.start_new_thread(self.send, ())
        while True:
            sleep(0.1)
            result = con.read_very_eager()
            if result != '':
                result = result.decode().split(' ')
                # print(result)
                if result[0] == "frecuency":
                    try:
                        self.sleep_time = int(result[1])
                    except:
                        pass
                elif result[0] == "get":
                    self.send()
            

if __name__ == "__main__":
    # app = wx.App()
    con = telnetlib.Telnet()
    print(sys.argv[1])
    temp = Data(sys.argv[1])
    # app.MainLoop()