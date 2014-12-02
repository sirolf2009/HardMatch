__author__ = 'Rene'

from Crawler.components import Component


class Motherboard(Component):
    socket = None

    chipset = None
    formFactor = None
    amountOfSockets = None
    memoryType = None
    maxMemorySize = None
    storageBus = None
    cardInterface = None
    amountOfPCI = None
    linkInterface = None
    ethernet = None
    networkChip = None
    bluetooth = None
    USBConnetion = None
    videoOutput = None
    audioChannels = None
    analogOutput = None
    digitaloutput = None
    audioChip = None