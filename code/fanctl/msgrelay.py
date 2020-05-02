#relay messages over socket
import logging
import socket
import time


#module logger
logger = logging.getLogger(__name__)


class MsgRelay:
	max_request = 5
	max_conn = 5
	
	def __init__(self,addr='localhost',port=6776):
			self.socks = list()
			self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.serversocket.bind ((addr,port))
			self.serversocket.listen(self.max_request)
			self.serversocket.settimeout(2) #time out for accepting
			
	def __del__(self):
		#destructor: close sockets if not done yet
		for s in self.socks:
			s.close()
		self.socks.clear()

	def accept_conn(self,timeout=2):
		logger.debug("Accepting connections")
		self.serversocket.settimeout(timeout)
		try:
			(conn, (ip, port)) = self.serversocket.accept()
		except socket.timeout:
			logger.debug("timeout accepting connections")
			return False
		except:
			raise
		else:
			logger.info("connection established with %s : %s",ip, port)
			self.socks.append(conn)
			return True
				
	def relay_msg(self,msg):
		for conn in self.socks:
			try:
				conn.sendall(msg)
			except OSError:
				logger.info("connection error, removing connection")
				self.socks.remove(conn)
			except:
				raise
	
	def close_conn(self):
		for conn in self.socks:
			try:
				conn.close()
			except OSError:
				logger.info("error closing connection")
			except:
				raise
			self.socks.remove(conn)
	
	
	
	
