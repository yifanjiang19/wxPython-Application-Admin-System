#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import wx
import telnetlib
import sys
import _thread as thread
import time
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
        try:
            temp = int(name)
        except:
            print("user")
        con.write(('login '+ str(self.name) + '\r\n').encode("utf-8"))
    
    def send(self):
        while(1):
            print("senddata")
            sleep(self.sleep_time)
            blood_pressure = randint(50,110)
            breath = randint(50, 180)
            temper = randint(3500,4200)/100.0
            alarm = self.is_alarmed(blood_pressure, breath, temper)
            localtime = time.asctime( time.localtime(time.time()) )
            con.write(('senddata ' + str(self.index) + ' '
                    + str(self.name) + ' ' 
                    + str(alarm) + ' '
                    + str(blood_pressure) + ' '
                    + str(breath) + ' ' 
                    + str(temper) + ' '
                    + str(localtime) + '\r\n').encode("utf-8"))
    
    def is_alarmed(self, blood_pressure, breath, temper):
        if blood_pressure < self.blood_pressure_down or blood_pressure > self.blood_pressure_up:
            return 1
        elif breath < self.breath_down or breath > self.breath_up:
            return 1
        elif temper < self.temper_down or temper > self.temper_up:
            return 1
        else:
            return 0
        
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
                        self.blood_pressure_up = int(result[3])
                        self.blood_pressure_down = int(result[4])
                        self.breath_up = int(result[5])
                        self.breath_down = int(result[6])
                        self.temper_up = int(result[7])
                        self.temper_down = int(result[8])
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