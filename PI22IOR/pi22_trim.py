import hid
from instruments.dmm_gwinstek_9061 import *
from pi22_driver import *


def pi20_chipid():
    """
    :return: chipid
    """
    return pi22_i2c_read(pBdg, pAddr, 0x00, 0x01)

def pi22_unlock():
    """
    unlock the register to write the trimmed register
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x40, 0x00, 0xC0DE)
    pi22_i2c_write(pBdg, pAddr, 0x40, 0x01, 0xF00D)
    pi22_i2c_read(pBdg, pAddr, 0x40, 0x00)
    pi22_i2c_read(pBdg, pAddr, 0x40, 0x01)

def ibias_trim():
    """Connect the SMU and Force 1v voltage"""
    # IBIAS
    pi22_i2c_write(pBdg, pAddr, 0x41, 0x02, 0x0021)   # map ibias on INTB
    # Force 1V on the INTB using SMU and measure current
    pi22_i2c_write(pBdg, pAddr, 0x20, 0x00, 0x0000)  # 5:0  find the value which get 1uA 最高位是符号位
    # disconnect the pull up resistor

    print("Check the current")
    input()
    pi22_i2c_write(pBdg, pAddr, 0x41, 0x02, 0x0000) # ibias on INTB off

    # input()


def osc_trim():
    pi22_i2c_write(pBdg, pAddr, 0x41, 0x01, 0x0001) # map osc on INTB
    pi22_i2c_write(pBdg, pAddr, 0x22, 0x03, 0x2300) # adjust the osc
    print("check the ossc fre")
    input()
    pi22_i2c_write(pBdg, pAddr, 0x41, 0x01, 0x0000)  # INTB funcs on INTB off

def vref_trim():
    diff = 0.002
    dmm = DmmGwinstek9061(pyvisa.ResourceManager(),dmm_9060_num14_id)
    print(dmm.read_voltage())
    pi22_i2c_write(pBdg, pAddr, 0x20, 0x00, 0xD000)
    # pi22_i2c_write(pBdg, pAddr, 0x20, 0x01, 0x0700)

    i = 40 # Normally should scan from 0X00
    pi22_i2c_write(pBdg, pAddr, 0x20, 0x01, 0x0700 | i)  # adjust the vref

    while(abs((2.5 - dmm.read_voltage())) > diff) :
        i = i + 1
        print(i)
        pi22_i2c_write(pBdg, pAddr, 0x20, 0x01, 0x0700 | i) # adjust the vref
        time.sleep(0.2)

        """改一下 改成二分法"""

def tec_current_trim():
    """
    Not tested The default Value should be 0XA300
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0X21, 0X03, 0XA300)  # set the not tested but default value


def efuse_trim():
    """

    :return:
    """
    print("Set power to 5.2V")
    input()
    pi22_i2c_write(pBdg, pAddr, 0x41, 0x03, 0X0001)  # adjust the vref
    print("Set poer to 3.3V")
    print("Power circle to detect the vref which should be 2.5V")




if __name__ == '__main__':
    pBdg = hid.device()  # create hid device
    pBdg.open(0x1A86, 0xFE07)
    pAddr = 0x80

    print("Please Reset the chip")
    """For example turn off the Buck Nrail Tec ..."""

    pi22_unlock()

    ibias_trim()
    #
    # pi22_i2c_read(pBdg,0x80,0x20,0x00,1)
    # pi22_i2c_read(pBdg, 0x80, 0x41, 0x02, 1)

    osc_trim()
    #
    vref_trim()
    # #
    tec_current_trim()
    # #
    efuse_trim()




















