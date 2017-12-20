#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import asynchat
import asyncore
import wx

class AdminFrame(wx.Frame):
    """
    admin window
    """
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        
        panel = wx.Panel(self, -1)
        panel.Bind(wx.EVT_MOTION, self.OnMove) 
        wx.StaticText(panel, -1, "Pos:", pos=(10, 12))
        self.posCtrl = wx.TextCtrl(panel, -1, "", pos=(40, 10))
        self.Show()
    def OnMove(self, event):
        pos = event.GetPosition() 
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))
            
class CentralServer(asyncore.dispatcher):
    """
    Server
    """
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        # 创建socket
        self.create_socket()
        # 设置 socket 为可重用
        self.set_reuse_addr()
        # 监听端口
        self.bind(('', port))
        self.listen(5)
        self.users = {}
        self.system = AdminSystem(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ReceiveSession(self, conn) # "self" is server

class ReceiveSession(asynchat.async_chat):
    def __init__(self, server, sock):
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator(b'\r\n')
        self.data = []
        self.name = None
        self.system = None
        self.add_to_system(server.system)
        # self.enter(LoginRoom(server))

    def add_to_system(self, system):
        self.system = system
        system.add(self)
    
    def collect_incoming_data(self, data):
        # 接收客户端的数据
        self.data.append(data.decode("utf-8"))

    def found_terminator(self):
        # 当客户端的一条数据结束时的处理
        line = ''.join(self.data)
        self.data = []
        try:
            self.system.handle(self, line.encode("utf-8"))
        # 退出聊天室的处理
        except EndSession:
            self.handle_close()

class CommandHandler:
    """
    命令处理类
    """

    def unknown(self, session, cmd):
        # 响应未知命令
        # 通过 aynchat.async_chat.push 方法发送消息
        session.push(('Unknown command {} \n'.format(cmd)).encode("utf-8"))

    def handle(self, session, line):
        line = line.decode()
        # 命令处理
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        # 通过协议代码执行相应的方法
        method = getattr(self, 'do_' + cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)

class SessionList(CommandHandler):
    """
    processing all sessions
    """
    def __init__(self, server):
        self.server = server
        self.sessions = []
    
    def add(self, session):
        self.sessions.append(session)

    def do_login(self, session, line):
        name = line.strip()
        # 获取用户名称
        if not name:
            session.push(b'UserName Empty')
        # 检查是否有同名用户
        elif name in self.server.users:
            session.push(b'UserName Exist')
        # 用户名检查成功后，进入主聊天室
        else:
            session.name = name
            session.push(b'Login Success')
            self.server.users[session.name] = session
            if session not in self.sessions:
                self.add(session) 
            for session in self.sessions:
                print(session.name)
            print(session.server.users)
            # print(session.system.server.users)
    def do_process_data(self, session, data):
        print(session)
        

    def remove(self, session):
        self.sessions.remove(session)

    def do_broadcast(self, session, cmd):
        # use asynchat.async_chat.push() to send data
        try:
            for session in self.sessions:
                for sess in self.sessions:
                    session.push(bytes(sess.name, encoding="utf-8"))
        except:
            print("error")
    def send(self, session, cmd):
        session.push(cmd)


class AdminSystem(SessionList):
    """
    main admin system
    """
    def add(self, session):
        self.sessions.append(session)
    def change_frequency(self):
        # broadcast to every users
        pass
    def alarm(self):
        # send data to one user
        pass

if __name__ == "__main__":
    # app = wx.App()
    # AdminFrame(None, -1, title="Login", size=(320, 250))
    # app.MainLoop()
    port = 6666
    sess = CentralServer(port)
    try:
        print("chat serve run at '0.0.0.0:{0}'".format(port))
        asyncore.loop()
    except KeyboardInterrupt:
        print("chat server exit")


