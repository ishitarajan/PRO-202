import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.2'
port = 8001

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []
print("Server has started")

questions = [
    "Who is the leader of Stray Kids??\n a.Bhang Chahn\n b.Jungkook\n c.Hyunjin\n d.Taecyon",
    "How many memebers are there in Stray Kids??\n a.4\n b.5\n c.3\n d.8",
    "Who is not the OG avenger??\n a.Scott Lang\n b.Natasha Romanoff\n c.Bruce Banner\n d.Steve Rogers",
    "Who is Steve Roger's best-friend??\n a.Clint Barton\n b.Thor\n c. Bucky Barnes\n d.Bruce Banner",
    "Who wrote the Maxe Runner Series??\n a.Rick Riordan\n b.James Dashner\n c.J.K.Rowling\n d.C.S.Lewis"
]
answers = ['a', 'd','a','c','b']
def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will recieve a question. The answer to that question should be one of a, b,c or d ".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, questions, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            print(message)
            message= message.split(": ")[-1]
            print(message)
            if message:
                if message. lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your scores is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time\n\n".encode('utf-8'))
                remove_question(index)
                index, questions, answer = get_random_question_answer(conn)
            else:
                
                remove_nickname(nickname)
        except:
            continue

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer 

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()