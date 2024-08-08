#!/usr/bin/env python3
import socket
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random
import time
import checksum
import helper
import crc

HOST = 'localhost'
PORT = 9999
PKT_SIZE = 8
c = socket.socket()
random.seed(time.time()) #initialize the random number generator


def inject_error(text: str, number: int) -> str:
    if number == 0:
        return text
    for _ in range(number):
        x = random.randint(0, len(text)-1)
        if text[x] == '0':
            text = text[:x]+'1'+text[x+1:]
        else:
            text = text[:x]+'0'+text[x+1:]
    return text


c.connect((HOST, PORT)) #establishes a connection from the client socket c to a server running on the local machine (localhost) at port 9999

text = input("Enter data:").encode('utf-8') # The encode('utf-8') method converts the string entered by the user into bytes using the UTF-8 encoding. This is useful for preparing the string for transmission over a network or for writing to a binary file.
res = input("Do you want to insert errors?(Y/n)")
method = input("Detection Method:(CRC/Checksum)")
enc_text = bin(bytes_to_long(text))[2:]
actual_len = len(enc_text)

if actual_len/8 == 0:
    pass
else:
    extra = '0'*(8-(actual_len % 8))
    enc_text = enc_text + extra

chunks = [enc_text[i:i+PKT_SIZE] for i in range(0, len(enc_text), PKT_SIZE)]

c.send(long_to_bytes(actual_len))
time.sleep(1)
if method == "CRC":

    c.send(b"CRC")
    time.sleep(1)
    crc_method = input("Give the CRC divisor method:")
    divisor = helper.convToBinary(crc_method)
    c.send(divisor.encode('utf-8'))
    chunks = crc.CRC.encodeData(chunks, divisor)
elif method == "Checksum":
    c.send(b"Checksum")
    time.sleep(1)
    c.send(checksum.Checksum.generate_checksum(chunks).encode('utf-8'))
else:
    print("No such method!")
    c.close()
    exit(1)
for i in chunks:
    time.sleep(1)
    if res == 'y' or res == 'Y':
        j = inject_error(i, random.randint(0, 2))
        c.send(j.encode('utf-8'))
    else:
        c.send(i.encode('utf-8'))

c.send(b'EOF')
print("Sending data", enc_text)
print(chunks)
print(c.recv(1024).decode('utf-8'))