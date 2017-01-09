__author__ = 'limeng12'
#coding=utf-8

class ReadData(object):

    def __init__(self , source):
        self.source=source

    def read(self):
        result=[]
        file=open(self.source)
        for line in file :
            datas=line.replace("\n","").replace(" ","").split(",")
            result.append(datas)
        return result
