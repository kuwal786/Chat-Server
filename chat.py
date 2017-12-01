import socket
from _thread import *
import sys

class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	def __init__(self):
		self.sock.bind(('0.0.0.0',10000))
		self.sock.listen(1)

	def handler(self,c,a):
		while True:
			data = c.recv(1024)
			if not data:
				print(str(a[0]) + ':' + str(a[1]),"disconnected")
				self.connections.remove(c)
				c.close()
				break
			else:
				print(data.decode().split('|')[0])
				for connection in self.connections:
					connection.send(data)
				
			
	def run(self):
		while True:
			c, a = self.sock.accept()
			start_new_thread(self.handler,(c,a))
			
			self.connections.append(c)
			print(str(a[0]) + ':' + str(a[1]),"connected")

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	uname = ''
	chat_with = ''
	def sendMsg(self):
		while True:
			message = sys.stdin.readline()
			self.sock.send(str.encode(self.uname+':'+message+'|'+self.chat_with))
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()

	def __init__(self, address):
		print("Enter your name:")
		self.uname=input()
		print("To whom you want to chat with('all' for broadcast):")
		self.chat_with=input()
		self.sock.connect((address, 10000))
		start_new_thread(self.sendMsg,())
		
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			msg = data.decode().split('|')[0]
			sentfor = data.decode().split('|')[1]
			if sentfor == 'all' or sentfor == self.uname :
				print(msg)

if (len(sys.argv) > 1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()
		
		