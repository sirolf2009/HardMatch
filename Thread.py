__author__ = 'gokhankacan'
from subprocess import call
import time
import shlex
import threading as t

def func():


    print('Rebooting')
    # call(shlex.split('reboot'))


    call(["ls", "-l"])
    print("Next go into map")
    time.sleep(3)

    call(shlex.split('ifconfig'))
    print("Printed IFconig")
    time.sleep(5)


    call(shlex.split('cd Analyser'), )
    print('Done')



def main():

    startNeoTemp = t.Thread(target=neoTemp.start('start'), name='Staring Neo4j Temp Database')
    startNeoFinal = t.Thread(target=neoFinal.start('start'), name='Staring Neo4j Final Database')
    startThrift = t.Thread(target=thriftSignal.start('start'), name='Staring THRIFT signal')
    startFlask = t.Thread(target=flaskDash.start('start'), name='Staring Flash Dashboard')

    startNeoTemp.start()
    startNeoTemp.join()
    startNeoFinal.start()
    startNeoTemp.join()
    startThrift.start()
    startThrift.join()
    startFlask.start()

    print("Everything started the right way")



class neoTemp():

    def start(self):
        print('Starting Neo4J Temp Database')
        time.sleep(5)


class neoFinal():

    def start(self):
        print('Starting Neo4J FINAL Database')
        time.sleep(5)


class thriftSignal():

    def start(self):
        print('Starting THRIFT connection')
        time.sleep(5)

class flaskDash():

    def start(self):
        print('Starting the Dahsboard')
        time.sleep(5)



if __name__ == '__main__':
    func()