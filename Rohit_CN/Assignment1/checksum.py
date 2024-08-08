#!/usr/bin/env python3
class Checksum:

    @classmethod
    def generate_checksum(cls, chunks):
        res = ""
        size = len(chunks[0])
        for chunk in chunks:
            res = bin(int(res, 2)+int(chunk, 2)) if res != "" else chunk
        if(len(res)>size) :
            ex = len(res)-size
            res = bin(int(res[0:ex],2)+int(res[ex:],2))[2:]
        if(len(res)<size):
            res='0'*(size-len(res))+res
        checksum=''
        for i in res :
            if i=='1':
                checksum+='0'
            else: 
                checksum+='1'
        return checksum

    @classmethod
    def check_checksum(cls, chunks, checksum):
        res = ""
        size = len(chunks[0])
        for chunk in chunks:
            if chunk == '':
                continue
            res = bin(int(res, 2)+int(chunk, 2)) if res != "" else chunk
        if(len(res)>size) :
            ex = len(res)-size
            res = bin(int(res[0:ex],2)+int(res[ex:],2))[2:]
        if(len(res)<size):
            res='0'*(size-len(res))+res
        res = bin(int(res, 2)+int(checksum, 2))
        if res.count("1") == size:
            return True
        else:
            return False