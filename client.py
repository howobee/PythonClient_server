import socket
import threading
import time

# Ключ для шифрования сообщений
key = 8194

# Переменные
shutdown = False
join = False

# Функция создания клиента
def receving(name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				print(data.decode("utf-8"))
				
				# Шифрование сообщений перед отправкой на сервер
				#BEGIN
				decrypt = ""; k = False
				for i in data.decode("utf-8"):
					if i == ":" :
						k = True
						decrypt += i
					elif k == False	or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^key)
				print(decrypt)
				#END
					
				time.sleep(0.2)
		except:
			pass
			
# Создания сокета клиента
host = socket.gethostbyname(socket.gethostname())
port = 0

# Ищем аддрес сервера
server = (' ', 5050 )			

#Создаем сокет используя Ip4 и протокол UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

# Принимаем и Сохраняем имя нового клиента
alias = input("Name: ")

#Создаем поток
rT = threading.Thread(target = receving, args = ("RecvThread", s))
rT.start()

#========================Основной цикл=====================================#
while shutdown == False:
	if join == False:
		s.sendto(("["+alias + "] >>> join chat ").encode("utf-8"), server)
		join = True
	else:
		try:
			message = input()
			
			#BEGIN
			crypt = ""
			for i in message:
				crypt += chr(ord(i)^key)
			message = crypt
			#END
			
			if message != " ":
				s.sendto(("["+alias + "] :: "+message).encode("utf-8"), server)
			time.sleep(0.2)
		except:
			s.sendto(("["+alias + "] <<< left chat ").encode("utf-8"), server)
			shutdown = True
			
			
rT.join()
s.close()			