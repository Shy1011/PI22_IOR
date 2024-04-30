from IfDriver import *

def pi22_i2c_write(pHid, pSlaveAddr, pBlockAddr, pRegAddr, pData):
    i2c_write(pHid, pSlaveAddr, 0x00, [0x80, 0x00, pBlockAddr])
    i2c_write(pHid, pSlaveAddr, 0x00, [pRegAddr, (pData>>8) & 0xFF, (pData & 0xFF)])

def pi22_i2c_read(pHid, pSlaveAddr, pBlockAddr, pRegAddr,ifPrint = 1):
    i2c_write(pHid, pSlaveAddr, 0x00, [0x80, pBlockAddr, 0x00])
    rdData = i2c_read(pHid, pSlaveAddr, 0x00, 2, pRegAddr)
    data = rdData[1] << 8 | rdData[2]
    if ifPrint == 1:
        print(f"0x{data:04x}")

    return data