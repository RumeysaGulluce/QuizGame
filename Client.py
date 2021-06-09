import threading
import socket


person = input('İsminiz? >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 59000))


class Istemci():


  def client_receive(self):  # teslim almak
      while True:
          try:
              message = client.recv(1024).decode('utf-8')
              if message == "person?":
                client.send(person.encode('utf-8'))
              else:
                print(message)
          except:
             print('Quiz Bitti')
             client.close()
             break


  def client_send(self):  # göndermek
      answer=['C','D','A','A','C']
      count=int(0)

      while count <=4:
          message = input('').upper()
          a = f'{person}:{message}'

          if answer[count] == message:
              client.send(a.encode(('utf-8')))
              print('doğru cevap')
          else:
            client.send(a.encode(('utf-8')))
            print('yanlış cevap')
          count += 1


obj=Istemci()
receive_thread = threading.Thread(target=obj.client_receive)
receive_thread.start()

send_thread = threading.Thread(target=obj.client_send)
send_thread.start()

