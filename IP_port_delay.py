__author__ = 'limeng12'
#coding=utf-8
import sys
import os
import read_data
import datetime
import time
import threading

eth="eth0"
class Delay(object):
    def __init__(self , file , delaytime ,runtime):
        self.file=file
        #self.delaytime=delaytime
        self.runtime=runtime
        self.delay_before="tc qdisc del dev "+eth+" root"
        self.delay_command="tc qdisc add dev "+eth+" root handle 1: prio bands 4 \n " \
                            "tc qdisc add dev "+eth+" parent 1:4 handle 40: netem delay "+str(delaytime)+"s \n " \
                            "tc filter add dev "+eth+" protocol ip parent 1:0 prio 4 u32 match ip dport "
        self.delay_after="tc qdisc del dev "+eth+" root"
        self.drop_before="iptables -D INPUT 1"
        self.drop_command="iptables -I INPUT -p TCP -s "
        self.drop_after="iptables -D INPUT 1"


    def delay(self):
        datas=read_data.ReadData(self.file).read()
        for line in datas:
            thread_list=list()
            for port in line:
                print "::  "+port
                thread_list.append(CommonThread(self.delay_before,self.delay_command+port+" 0xffff flowid 1:4",self.delay_after,self.runtime))
            Delay.printOut("---DELAY_START-----")
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
            self.printOut("----DELAY_END-------")

    def drop(self):
        datas=read_data.ReadData(self.file).read()
        for line in datas:
            thread_list=list()
            for ip in line:
                thread_list.append(CommonThread(self.drop_before,self.drop_command+ip+" -j DROP",self.drop_after,self.runtime))
            Delay.printOut("---DROP_START-----")
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
            self.printOut("----DROP_END-------")

    def switch(self):
            pass

    @staticmethod
    def printOut(sth):
        log_file=open("logfile.log","a")
        log_file.write(datetime.datetime.now().strftime('%c') +" : "+ sth +" \n")

class CommonThread(threading.Thread):

    def __init__(self , command_before ,command_run,command_after, runtime):
        threading.Thread.__init__(self)
        self.command_before=command_before
        self.command_run=command_run
        self.command_after=command_after
        self.runtime=runtime

    def run(self):
        Delay.printOut(self.command_before)
        os.system(self.command_before)
        time.sleep(self.runtime)

        Delay.printOut(self.command_run)
        os.system(self.command_run)
        time.sleep(self.runtime)

        Delay.printOut(self.command_after)
        os.system(self.command_after)

if __name__ =='__main__':
    drop = Delay("./drop_config",5,300)
    delay = Delay("./delay_config",5,8)
    if sys.argv[1] == "drop" :
        drop.drop()
    elif sys.argv[1] == "delay" :
        delay.delay()
    else:
        print(" choose a parameter in drop and delay ")