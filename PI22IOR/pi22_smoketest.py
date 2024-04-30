import time
import hid
from pi22_driver import *
from pi22_lib import *

pBdg = hid.device()  # create hid device
pBdg.open(0x1A86, 0xFE07)
pAddr = 0x80

def pi22_vdac_DIS():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x03, 0x0001)  # power down state in response to DIS pin.

def pi22_vdac_APD():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x07, 0x0001)  # APD event, Enable bits for ALARM_STATUS1
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x04, 0x0001)  # power down state in response to APD event.

def pi22_vdac_CLRVAL():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x0A, 0x0800)  # TODO: 清除值
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x08, 0x0001)  # clear state in response to DIS pin.
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x0B, 0x0001)  # CFG_DAC_CLR_BIT
    # pi22_i2c_write(pBdg, pAddr, 0x01, 0x0C, 0x0001)  # DIS pin used preset CLR

def pi22_idac_DIS():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x03, 0x0002)  # power down state in response to DIS pin.

def pi22_idac_APD():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x07, 0x0001)  # APD event, Enable bits for ALARM_STATUS1  # TODO: 此前B05A00 相应位置1
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x04, 0x0001)  # power down state in response to APD event.

def pi22_idac_CLRVAL():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x09, 0x0800)  # TODO: 清除值
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x08, 0x0002)  # clear state in response to DIS pin.
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x0B, 0x0002)  # CFG_DAC_CLR_BIT
    # pi22_i2c_write(pBdg, pAddr, 0x01, 0x0C, 0x0001)  # DIS pin used preset CLR


def buck_test():
    # """ Buck test """
    pi22_buck_en(ENABLE)
    pi22_buck_set(0x0A00)

    print("Buck reg")
    pi22_i2c_read(pBdg, pAddr, 0x07, 0x00)
    pi22_i2c_read(pBdg, pAddr, 0x07, 0x01)

def nrail_test():
    # """ Nrail test """
    pi22_nrail_en(ENABLE)
    pi22_nrail_set(0x0000)
    print("Nrail reg")
    pi22_i2c_read(pBdg, pAddr, 0x06, 0x00)
    pi22_i2c_read(pBdg, pAddr, 0x06, 0x01)

def tec_test():
    #Tec
    pi22_tec_cfg()
    pi22_tec_manual_PN_set(0XF000)





if __name__ == '__main__':
    pi22_reset()
    pi22_chipid()

    """BUCK NRAIL TEC TEST"""
    buck_test()
    nrail_test()
    tec_test()

    # pi22_i2c_read(pBdg, pAddr, 0x07, 0x00)





    # """ PWD bit  /DIS pin """
    # pi22_i2c_write(responsepBdg, pAddr, 0x01, 0x03, 0x0001)         # 放VDAC配置后面重启

    # """ Nrail test """
    # pi22_nrail_en(ENABLE)
    # pi22_nrail_set(0x000e)
    # print("Nrail reg")
    # pi22_i2c_read(pBdg, pAddr, 0x06, 0x00)
    # pi22_i2c_read(pBdg, pAddr, 0x06, 0x01)

    # """ VDAC test """
    # pi22_vdac_en()
    # pi22_vdac_gain_range(1, -1)
    # pi22_vdac_en()
    # pi22_vdac_set(0x0800)
    # print("VDAC reg")
    # pi22_i2c_read(pBdg, pAddr, 0x01, 0x05)
    # pi22_i2c_read(pBdg, pAddr, 0x01, 0x02)
    # pi22_i2c_read(pBdg, pAddr, 0x02, 0x00)
    #
    # pi22_vdac_DIS()
    # pi2'
    # 0_vdac_APD()
    # pi22_vdac_CLRVAL()
    # pi22_vdac_Isence()


    # # """ Buck test """
    # pi22_buck_en(ENABLE)
    # pi22_buck_set(0x0A00)
    #
    # print("Buck reg")
    # pi22_i2c_read(pBdg, pAddr, 0x07, 0x00)
    # pi22_i2c_read(pBdg, pAddr, 0x07, 0x01)

    # """ IDAC test @ only PI21"""
    # pi22_idac_en()
    # pi22_idac_set(0x0800)
    # print("\nIDAC reg")
    # pi22_i2c_read(pBdg, pAddr, 0x01, 0x02)
    # pi22_i2c_read(pBdg, pAddr, 0x02, 0x01)

    # pi22_idac_DIS()
    # pi22_idac_APD()
    # pi22_idac_CLRVAL()
    # pi22_idac_Vsence()

    # pi22_adc_cfg_seq(0, 15)
    # pi22_adc_cfg_ctrl(pMode=1, pAlar=0, pPreC=0, pClock=1, pStatus=1)
    # pi22_INTb_log(5, 0x0000, 0x0fff)
    # pi22_adc_readbuf(5)

    #Tec
    # pi22_tec_cfg()
    # pi22_tec_manual_PN_set(0XF000)
