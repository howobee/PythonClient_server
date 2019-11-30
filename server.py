import socket
import time

#Получаем порт и ip нашего сервера
host = socket.gethostbyname(socket.gethostname())


port = 5050

# Создаем пустой список для адресов будущих клиентов
clients = []

#Создаем сокет используя Ip4 и протокол UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

quit = False

print("<Server Started>")

#============================ЦИКЛ СЕРВЕРА===================================#

while not quit:
	try:
		data, addr = s.recvfrom(1024)
		
		# Проверка содержиться ли клиент в списке Clients если нет тогда добавляем
		if addr not in clients:
			clients.append(addr)
		
		#Получения текущего времени и сохранения его в переменной itsatime	
		itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
		
		# Отправления отформатированного сообщения всем клиентам кроме отправителя
		print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")
		print(data.decode("utf-8"))
		
		#Проверка перед отправкой сообщения
		for client in clients:
			if addr != client:
				s.sendto(data, client)
		
	except:
		print("\n<Server Stopped>")
		quit = True
		
# Закрываем соке
s.close()