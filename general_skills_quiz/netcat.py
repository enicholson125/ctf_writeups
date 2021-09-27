import socket
import urllib
import base64
import string

# Due to me not paying attention during setup, this script is in Python 2

hostname = "pwn-2021.duc.tf"
port = 31905


# Rot13 is symmetrical, so only need one of these for encryption and decryption
def rot13(ciphertext):
    rot13Table = string.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

    text = ""
    for ch in ciphertext:
        text += string.translate(ch, rot13Table)
    return text


def submit_answer(answer, sock):
    sock.send("%s\n" % answer)
    data = sock.recv(1024)
    print(data)
    pieces = data.split(":")
    return pieces[1].strip()


def answer_quiz(hn, p, content):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hn, p))

    sock.send(content)

    data = sock.recv(1024)
    print(data)

    sock.send("\n")

    data = sock.recv(1024)
    print(data)

    # 1+1
    question_text = submit_answer(2, sock)

    # Convert hex to decimal
    question_text = submit_answer(int(question_text, 0), sock)

    # Convert hex to ASCII
    question_text = submit_answer(question_text.decode("hex"), sock)

    # Convert URL format to ASCII
    question_text = submit_answer(urllib.unquote(question_text), sock)

    # Base64 decode
    question_text = submit_answer(base64.b64decode(question_text), sock)

    # Base64 encode
    question_text = submit_answer(base64.b64encode(question_text), sock)

    # Rot13 decode
    question_text = submit_answer(rot13(question_text), sock)

    # Rot13 encode
    question_text = submit_answer(rot13(question_text), sock)

    # Convert binary to int
    question_text = submit_answer(int(question_text, 0), sock)

    # Convert int to binary
    sock.send("%s\n" % bin(int(question_text)))
    data = sock.recv(1024)
    print(data)

    # What is the greatest CTF?
    sock.send("DUCTF\n")
    flag = sock.recv(1024)
    print(flag)

    sock.shutdown(socket.SHUT_WR)

    print("Connection closed.")
    sock.close()


answer_quiz(hostname, port, "")
