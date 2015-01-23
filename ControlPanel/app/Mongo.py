__author__ = 'gokhankacan'
from pymongo import MongoClient, Connection

# Mongo Client Connection
client = MongoClient('localhost', 27017)
mongodb = client.coolblue


def main():

    getCPU()



def useDatabase(use):
    if use == 'coolblue':
        mongodb = client.coolblue
    elif use == 'alternate':
        mongodb = client.alternate
    elif use == 'informatique':
        mongodb = client.informatique
    return mongodb




def getCollection(coll):

    if coll == 'CPU':
        print('dsfsdf')
    """
    # Check Datetime at every loop
    now = datetime.now()

    if PD.get('Merk') is None: brand = "NULL"
    else: brand = PD['Merk']

    post = {'ModelID': PD['Fabrikantcode'], 'Name': title, 'Price': price, 'Brand': brand, 'Type': productType[componentTitle], 'Timestamp': int(time.mktime(now.timetuple()))}


    if productType[componentTitle] == 'CPU': mongodb.CPU.insert(post)
    elif productType[componentTitle] == 'Motherboard': mongodb.Motherboard.insert(post)
    elif productType[componentTitle] == 'CPUFan': mongodb.CPUFan.insert(post)
    elif productType[componentTitle] == 'GraphicsCard': mongodb.GraphicsCard.insert(post)
    elif productType[componentTitle] == 'RAM': mongodb.RAM.insert(post)
    elif productType[componentTitle] == 'Case': mongodb.Case.insert(post)
    elif productType[componentTitle] == 'PSU': mongodb.PSU.insert(post)
    elif productType[componentTitle] == 'Barebones': mongodb.Barebones.insert(post)
    elif productType[componentTitle] == 'Storage-HDD': mongodb.HDD.insert(post)
    elif productType[componentTitle] == 'Storage-SSD': mongodb.SSD.insert(post)
    else: mongodb.MISC.insert(post)
    """

def getCPU():


    cpuAll = mongodb.CPU.find()
    count = cpuAll.count()
    print(count)

    intel = mongodb.CPU.find({'Brand': 'Intel'})
    countIntel = intel.count()
    print(countIntel)

    amd = count - countIntel
    print(amd)


    """
    amdCPU = mongodb.CPU.find({'Brand': 'AMD'})
    amdCount = amdCPU.count()
    print(amdCount)
    """


if __name__ == '__main__':
    main()