import threading
import socket



host = 'localhost'
port = 59000
#python PycharmProjects\Arayüz\istemci.py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

clients = []
persons = []
messages=[]


class Sunucu():
    counter=0
    def broadcast(self,message):  # yayınlamak
        if self.counter==2:
            for client in clients:
                client.send(message)


    def getquestions(self,index):
        with open("dosya", "r", encoding="utf-8") as file:
            question_list = file.readlines()

            question=question_list[index]

            a = question_list[index+1]
            b = question_list[index+2]
            c = question_list[index+3]
            d = question_list[index+4]

            questions= question+'\n'+'A)'+a+'\n'+'B)'+b+'\n'+'C)'+c+'\n'+'D)'+d+'\n'

            if self.counter==2:
                take = f'{questions}'
                for client in clients:
                    client.send(take.encode(('utf-8')))


    def lineNumber(self):
        with open("dosya", "r", encoding="utf-8") as file:
            question_list = file.readlines()
            count = 0
            for x in question_list:
                count += 1
            return count // 5

    def handle_client(self,client):
        count = 0
        skip=0
        number=self.lineNumber()

        try:
            if count == 0:
                self.getquestions(skip)

            while True: # n soru içi 2n tane cevap alıyor


                skip+=5

                message = client.recv(1024)  # alınan mesajı dönüştürüyor ve yayınlıyor.
                messages.append(message)

                message_counter = len(messages)



                if message_counter == 2:

                    for i in messages:
                        self.broadcast(i)
                    messages.clear()
                    count+=1

                    if count !=0 and count<number:
                        self.getquestions(skip)


        except  :
            index = clients.index(client)
            clients.remove(clients)
            client.close()
            person = persons[index]
            self.broadcast(f'{person} has left the chat room!'.encode('utf-8'))
            persons.remove(person)


    def receive(self):


        while self.counter <=2:

            print("sunucu çalışıyor...")

            client, address = server.accept()
            self.counter+= 1
            print('kullanıcı sayısı:',self.counter)

            print(f'Bağlantı kurulan adres {str(address)}')
            client.send('person?'.encode('utf-8'))

            person = client.recv(1024)
            persons.append(person)
            clients.append(client)

            print(f'Kullanici adi: {person}'.encode('utf-8'))

            self.broadcast(f'{person} quiz odasına bağlandı '.encode('utf-8'))
            client.send('Bağlantı kuruldu.!'.encode('utf-8'))


            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

            if self.counter > 2:
                client.send('sınıf doldu.!'.encode('utf-8'))
                print('Sınıf dolu')



obj=Sunucu()
obj.receive()