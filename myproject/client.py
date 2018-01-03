#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import wx
import telnetlib
import sys
import _thread as thread
from time import sleep
from random import randint, random

class Data:
    def __init__(self, name, sleep_time=3, index=0):
        self.name = name
        self.sleep_time = sleep_time
        self.index = index
        self.blood_pressure_up = 180
        self.blood_pressure_down = 100
        self.breath_up = 180
        self.breath_down = 100
        self.temper_up = 42
        self.temper_down = 36
        self.login()
        self.receive()
        print("asd")
        # self.send()
    
    def login(self):
        print("login")
        con.open("127.0.0.1", port=6666, timeout=10)
        con.write(('login '+ str(self.name) + '\r\n').encode("utf-8"))
    
    def send(self):
        while(1):
            print("senddata")
            sleep(self.sleep_time)
            heartbeat_freq = randint(50,110)
            blood_pressure = randint(50, 180)
            temper = randint(3500,4200)/100.0
            alarm = 1
            con.write(('senddata ' + str(self.index) + ' '
                    + str(self.name) + ' ' 
                    + str(alarm) + ' '
                    + str(blood_pressure) + ' '
                    + str(heartbeat_freq) + ' ' 
                    + str(temper) + '\r\n').encode("utf-8"))
    
    def receive(self):
        # 接受服务器的消息
        
        while True:
            sleep(0.1)
            result = con.read_very_eager()
            if result != '':
                result = result.decode().split(' ')
                if result[0] == "frecuency":
                    try:
                        self.sleep_time = int(result[2])
                    except:
                        pass
                elif result[0] == "Success":
                    self.index = int(result[1])
                    thread.start_new_thread(self.send, ())
                    
                # elif result[0] == "get":
                #     self.send()
            

if __name__ == "__main__":
    con = telnetlib.Telnet()
    print(sys.argv[1])
    temp = Data(sys.argv[1])