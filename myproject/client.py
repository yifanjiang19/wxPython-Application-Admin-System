#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import wx
import telnetlib
from time import sleep

class Data():
    def __init__(self):
        pass
    def send(self):
        con.open("127.0.0.1", port=8000, timeout=10)
        con.write("test")

if __name__ = "__main__":
    app = wx.App()
    con = telnetlib.telnet()
    app.MainLoop()