import hid
from pi22_driver import *
from excel.xls_file import *
from instruments.dmm_gwinstek_9061 import *
from instruments.smu_keithley_2450 import *
import numpy as np

pBdg = hid.device()  # create hid device
pBdg.open(0x1A86, 0xFE07)
pAddr = 0x80

smuid = smu_2450_id
dmmid = dmm_9060_num14_id

"""Pyvisa"""
def print_resource():
    # 创建资源管理器
    rm = pyvisa.ResourceManager()
    #
    # # 打印可用的资源（仪器）列表
    print(rm.list_resources())

""" IOR Test Functions """
def pi20_unlock():
    pi22_i2c_write(pBdg, pAddr, 0x40, 0x00, 0xC0DE)
    pi22_i2c_write(pBdg, pAddr, 0x40, 0x01, 0xF00D)
def pi22_chipid():
    return pi22_i2c_read(pBdg, pAddr, 0x00, 0x01)

def pi22_chip_status():
    return pi22_i2c_read(pBdg, pAddr, 0x00, 0x00)

def external_reset():
    """Test External reset button"""

    """Enable Buck"""
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x00,0x0001)
    print("Pres the button to reset the chip")
    input()
    if (pi22_i2c_read(pBdg, pAddr, 0x07, 0x00) == 0X00):
        print("Reset Button Success to reset")
    else :
        print("Reset Button Fail to reset")

def soft_reset_test():
    """Enable Buck"""
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x00,0x0001)

    """Buck Vset"""
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x01,0x0FFF)

    """soft reset"""
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x01, 0x0001)

    # pi22_i2c_read(pBdg, pAddr, 0x07, 0x00)
    # pi22_i2c_read(pBdg, pAddr, 0x07, 0x01)

def soft_reset():
    """soft reset"""
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x01, 0x0001)



def i2c_com():
    """
    Test IIC Communication
    Buck should be enabled and Voltage should be 0X0FFF

    """
    """Enable Buck"""
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x00,0x0001)
    pi22_i2c_read(pBdg, pAddr, 0x07, 0x00)

    """Buck Vset"""
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x01,0x0FFF)
    pi22_i2c_read(pBdg, pAddr, 0x07, 0x01)

def buck_set():
    """
    Buck output full scale
    :return:
    """
    buck_cfg(1)
    buck_vest(0XFFF)

def vref_powerdown(pdRef):
    """

    :param pdRef:  0 :  enable 1 : disable
    :return:
    """
    """power down the vref"""
    cfg_misc_pwdn(pdRef = pdRef)

def adc_single_seq_test(adcChanelSel,gain = 0):
    """

    :param adcChanelSel:  select which channel to read
    :param gain:  set the adc channel gain
    :return:
    """
    """Read ADC data from channel 6 [PVDD]"""

    print("ADC single Sequence")

    adc_cfg_ctrl(adcModeSel=0,adcEn=1)

    adc_cfg_seq(firReg=0,lastReg=0x0F)

    adc_cfg_config(addr=adcChanelSel, adcChanellSel=adcChanelSel,adcGain=gain)

    temp = adc_data(adcChanelSel)

    for i in range(0,8):
        if( temp != adc_data(adcChanelSel) ) :
            print("Wrong")
            return 0
    print("singale sequence pass")

def adc_continious_seq(adcChanSel = 0,gain = 0):
    """
    Configure the ADC to continious mode and read the value
    :param adcChanSel:
    :param gain:
    :return:
    """
    adc_cfg_ctrl(adcModeSel=1,adcEn=1)

    adc_cfg_seq(firReg=0,lastReg=0x0F)

    adc_cfg_config(addr=adcChanSel, adcChanellSel=adcChanSel,adcGain=gain)

    temp = adc_data(adcChanSel)

    return temp


def adc_continious_seq_test(adcChanSel = 0,gain = 0):
    """

    :param adcChanSel:
    :param gain:
    :return:
    """
    """Read ADC data from channel 5 [VBUCK]"""
    print("Continous Mode Read value from the VBUCK")
    adc_cfg_ctrl(adcModeSel=1,adcEn=1)

    adc_cfg_seq(firReg=0,lastReg=0x0F)

    adc_cfg_config(addr=adcChanSel, adcChanellSel=adcChanSel,adcGain=gain)

    buck_cfg(1)
    buck_vest(0XFFF)
    temp = adc_data(adcChanSel)

    """Buck 可以设定为0值但是不要关"""
    buck_cfg(0)
    buck_vest(0X000)
    time.sleep(3) # 释放电容的值
    temp2 = adc_data(adcChanSel)

    if temp2 != temp:
        print("Continous Seq Pass")

def adc_average_test(adcChanSel = 5,gain = 0,acerSel : int = 0b11,avrTime = 16):
    """

    :param adcChanSel:
    :param gain:
    :param acerSel: average of how many times 0b00 0b01 0b10 0b11
    :param avrTime: How many average time, acerSel represent to 4 8 16;
    :return:
    """
    print("ADC Average Test")

    buck_cfg(1)

    buck_vest(0XFFF)

    adc_cfg_ctrl(adcModeSel=1, adcEn=1)

    adc_cfg_seq(firReg=0, lastReg=0x0F)

    adc_cfg_config(addr=adcChanSel, adcChanellSel=adcChanSel, adcGain=gain,avrSel = 0b00)

    temp = 0
    for i in range(0,avrTime) :
        temp = temp + adc_data(adcChanSel,0)
    temp = temp/avrTime

    # 将浮点数转换为整数（舍去小数部分）
    int_value = int(temp)
    # 将整数转换为16进制字符串，并格式化为0xABCD形式
    print("The manually average value is : ")
    hex_value = f"0X{int_value:04X}"

    print(hex_value)



    adc_cfg_ctrl(adcModeSel=1, adcEn=1)

    adc_cfg_seq(firReg=0, lastReg=0x0F)

    adc_cfg_config(addr=adcChanSel, adcChanellSel=adcChanSel, adcGain=gain,avrSel = acerSel)

    print(f"The sys average value is : ")
    dataContinous = adc_data(adcChanSel)

    buck_cfg(0)

    buck_vest(0X000)

    if (int(hex_value,16) - dataContinous) < 3:
        print("Average Test Pass")

    print("_______________________________________________________________________")


def acquision_time(adcChanSel = 6, gain = 1,acq_sel : int = 0b11):
        """

        :param adcChanSel:
        :param gain:
        :param acq_sel: acquisition time select default/2/3.5/5us
        :return:
        """
        """Read ADC data from channel 5 [PVDD]"""
        print("acquision test read from PVDD")
        adc_cfg_ctrl(adcModeSel=1, adcEn=1)

        adc_cfg_seq(firReg=0, lastReg=0x0F)

        adc_cfg_config(addr=adcChanSel, adcChanellSel=adcChanSel, adcGain=gain,acqSel=acq_sel)

        adc_data(adcChanSel)

def read_all_channels():
    """Read ADC data from channel 5 [VBUCK]"""
    acquision_time(0,0,0b00)
    acquision_time(0, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(1, 0, 0b00)
    acquision_time(1, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(2, 0, 0b00)
    acquision_time(2, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(3, 0, 0b00)
    acquision_time(3, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(5,0,0b00)
    acquision_time(5, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(6, 0, 0b00)
    acquision_time(6, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(7, 0, 0b00)
    acquision_time(7, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(11, 0, 0b00)
    acquision_time(11, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(14, 0, 0b00)
    acquision_time(14, 1, 0b00)
    print("---------------------------------------------------------")
    acquision_time(15, 0, 0b00)
    acquision_time(15, 1, 0b00)
    print("---------------------------------------------------------")

def intb_test(adcChannel : int = 6,lo = 0x0000,hi = 0x0FFF):
    """
    :param addr: The register addr
    :param intbSel: Which status maps to INTB
    :param lo: low threshold
    :param hi: high threshold
    :return:
    """
    cfg_intb_src1(0XFFFF) # channel 6 open
    """channel 6 theshold set"""
    adc_cfg_lo_th(0x10|adcChannel,lo)
    adc_cfg_hi_th(0x20|adcChannel, hi)
    temp = pi22_i2c_read(pBdg, pAddr, 0x05, 0x00, 1)
    binary_representation = f"{temp:016b}"
    print(binary_representation)



###############################################################
""" Register Configure Operation"""
def cfg_intb_src1(intbEn : int = 0X0000):
    """
    :param intbEn: Max : OXFFFF  Enable bits to select ALARM_STATUS1 bits to trigger the INTb pin.
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x06, intbEn)

def buck_cfg(enable : int = 0b0):
    # pi22_i2c_write(pBdg, pAddr, 0x07, 0x07, 0x0fff)  # TODO: buck pid设定
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x00, enable)
    pi22_i2c_read(pBdg, pAddr, 0x07, 0x00)

def buck_vest(setpoint : int = 0x000):
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x01 , setpoint)
    pi22_i2c_read(pBdg, pAddr, 0x07, 0x01)


def cfg_misc_pwdn(pdAdc : int = 0b0,pdRef : int = 0b0,pdTemper : int = 0b0):
    """

    :param pdAdc:
    :param pdRef:
    :param pdRemper:
    :return:
    """
    pdata = pdAdc | (pdRef << 1) | (pdTemper << 3)
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x0F, pdata)
    # pi22_i2c_read(pBdg, pAddr, 0x01, 0x0F)


def adc_cfg_config(addr = 0X00,adcChanellSel : int = 0b0000,adcGain : int = 0,hizSel : int = 0,avrSel : int = 0b00,acqSel : int = 00):
    """

    :param addr:
    :param adcChanellSel:
    :param adcGain:
    :param hizSel:
    :param avrSel:
    :param acqSel:
    :return:
    """
    pdata = adcChanellSel | (adcGain << 4) | (hizSel << 5) | (avrSel << 6) | (acqSel << 8)

    pi22_i2c_write(pBdg, pAddr, 0x03, addr, pdata)
    # pi22_i2c_read(pBdg, pAddr, 0x03, addr)

    # for i in  range(0,16):
    #     adc_cfg_config(addr=i,adcChanellSel=i)


def adc_cfg_seq(firReg : int = 0b0000,lastReg : int = 0b0000):
    """

    :param firReg:
    :param lastReg:
    :return:
    """
    pdata = ( firReg << 8) | lastReg
    pi22_i2c_write(pBdg, pAddr, 0x03, 0x32, pdata)
    # pi22_i2c_read(pBdg, pAddr, 0x03, 0x32)

def adc_cfg_ctrl(adcModeSel :int = 0b0, alarmMode : int = 0b0, adcPre : int = 0b0,adcClo : int = 0b0,adcEn : int = 0b0):

    pdata = adcModeSel | (alarmMode << 2) | (adcPre << 3) | (adcClo << 6) | (adcEn << 7)

    pi22_i2c_write(pBdg, pAddr, 0x03, 0x33, pdata)
    # pi22_i2c_read(pBdg, pAddr, 0x03, 0x33)

def adc_data(addr,ifPrint = 1):
    return pi22_i2c_read(pBdg, pAddr, 0x04, addr,ifPrint)


def adc_cfg_lo_th(addr = 0x10,valueSet : int = 0X0000):
    pi22_i2c_write(pBdg, pAddr, 0x03, addr, valueSet)
    pi22_i2c_read(pBdg, pAddr, 0x03, addr,0)

def adc_cfg_hi_th(addr = 0x20,valueSet : int = 0X0FFF):
    pi22_i2c_write(pBdg, pAddr, 0x03, addr, valueSet)
    pi22_i2c_read(pBdg, pAddr, 0x03, addr,0)


"""Buck"""
def output_voltage_range():
    buck_cfg(1)
    dmm = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid)
    for i in range(40):
        buck_vest(i*100)
        vol = dmm.read_voltage()
        print(vol)
        if(vol > 1.2):
            print("Success")

def load_current():
    """Load Current test"""
    """
    在Buck输出1.8V的情况下能否输出 0 - 1.5A的电流
    """
    buck_cfg(1)
    buck_vest(0x0A80)
    # for i in range(0,0X0A80,0X0010):
    #     buck_vest(i)


def buck_voltage_range_test():
    """Detect the voltage change of Vref when the output voltage of the buck changes."""
    dmm = DmmGwinstek9061(pyvisa.ResourceManager(), dmm_9060_num14_id)
    smu = SmuKeithley2450(pyvisa.ResourceManager(), smu_2450_id)

    buck_cfg(1)
    buck_vest(0)

    ins_xls_ = Xls_File("BuckOutputRange.xlsx")
    ins_xls_.xls_open()

    ins_xls_.xls_write(1, 2, 'Code')
    ins_xls_.xls_write(1, 3, 'Vref(V)')
    ins_xls_.xls_write(1, 4, 'Vout_Buck(V)')

    for i in range(0,41):

        buck_cfg(1)
        code = i*100
        buck_vest(code)
        vout_buck = smu.smu_meas_v()
        vref = dmm.read_voltage()

        print(f"The Buck voltage is {vout_buck}")
        print(f"The Vref Voltage is {vref}")
        print("---------------------------------------------------------")
        row = ins_xls_.xls_append_row()
        ins_xls_.xls_write(row, 2, code)
        ins_xls_.xls_write(row, 3, vref)
        ins_xls_.xls_write(row, 4, vout_buck)

        ins_xls_.xls_close()

def load_regulation():
    """Buck设置为1.8V"""
    buck_cfg(1)
    buck_vest(0X0A80)

    dmm = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid)
    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)
    smu.sum2450_force_cur_sens_volt_init(-0.1, 5,1, 5, 0.1) # 强制电流测电压初始化

    step = 0.02  # 步长可以根据需要进行调整

    ins_xls_ = Xls_File("Load Regulation.xlsx")
    ins_xls_.xls_open()

    ins_xls_.xls_write(1, 2, 'Code')
    ins_xls_.xls_write(1, 3, 'Vref(V)')
    ins_xls_.xls_write(1, 4, 'Vout_Buck(V)')

    for value in np.arange(0.02, 1 + step, step):
        vref = dmm.read_voltage()
        print(vref)
        smu.smu_sour_ii(-value, 1)  # 提供电流 1是能提供的最大电流
        v_buck = smu.smu_2450_meas_v(1)  # 测量电压四线
        print(v_buck)







# def load_current():
#     smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)
#     for i in np.arange(0, 1.51, 0.1):
#         smu.smu_sour_ii(-i, 4)  # range cur
#         time.sleep(0.5)

def output_setpoint_resolution():
    buck_cfg(1)

    dmm = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid)
    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)
    smu.smu_meas_v()

    ins_xls_ = Xls_File("output_setpoint_resolution.xlsx")
    ins_xls_.xls_open()

    row = ins_xls_.xls_append_row()
    column = ins_xls_.xls_append_column()

    ins_xls_.xls_write(row + 1, column, 'Vref(V)')
    ins_xls_.xls_write(row + 2, column, 'Vout_Buck(V)')

    for i in range(0xFFF):
        print(i)
        buck_vest(i)
        time.sleep(0.1)
        v_buck = smu.instrument.query('MEAS:VOLT?')
        v_ref = dmm.read_voltage()
        column = ins_xls_.xls_append_column()
        ins_xls_.xls_write(row+1, column, v_ref)
        ins_xls_.xls_write(row+2, column, v_buck)

        ins_xls_.xls_close()

"""Nrail"""
def pi22_nrail_en():
    pi22_i2c_write(pBdg, pAddr, 0x20, 0x03, 0b1000 << 7) # 调整频率
    pi22_i2c_write(pBdg, pAddr, 0x06, 0x00, 0x0061)

def pi22_nrail_set(pCode):
    """
    :param pCode: 0x00----0x1f
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x06, 0x01, pCode)


"""Below are Developped by Bin Yang"""
###############################################################

def pi22_unlock():
    pi22_i2c_write(pBdg, pAddr, 0x40, 0x00, 0xC0DE)
    pi22_i2c_write(pBdg, pAddr, 0x40, 0x01, 0xF00D)

def pi22_reset():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x01, 0x0001)

def pi22_vdac_en():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x02, 0x0001)

def pi22_idac_en():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x02, 0x0002)

def pi22_vdac_gain_range(pGain = 1, pDir = 1):
    """
    :param pGain: 1 stand for 2.5V gain, other is 5V gain
    :param pDir: 1 stand for positive range, other is negative range
    :return:
    """
    mask = 0x0000
    if pGain == 1:
        mask = mask | 0x0001
    if pDir == 1:
        mask = mask | 0x0002
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x05, mask)
    return mask

def pi22_vdac_set(pCode):
    """
    :param pCode: 0x0000----0x0fff
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x02, 0x00, pCode)

def pi22_idac_set(pCode):
    """
    :param pCode: 0x0000----0x0fff
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x02, 0x01, pCode)


# def pi22_nrail_en(enable):
#     pi22_i2c_write(pBdg, pAddr, 0x06, 0x00, 0x0000 | enable)
#     pi22_i2c_write(pBdg, pAddr, 0x06, 0x00, 0x0060 | enable)
#
# def pi22_nrail_set(pCode):
#     """
#     :param pCode: 0x00----0x1f
#     :return:
#     """
#     pi22_i2c_write(pBdg, pAddr, 0x06, 0x01, pCode)


def pi22_buck_en(enable):
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x00, enable)

def pi22_buck_set(pCode):
    """
    :param pCode: 0x0000----0x0fff
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x07, 0x01, pCode)

def pi21_tian_pre():
    pi22_i2c_write(pBdg, pAddr, 0x01, 0x0f, 0x0000)

def pi21_tian(pGain = 0x07, pVbaisCtr = 1, pVbais = 0, pMirr = 0, pDis = 0):
    """
    :param pGain:       bit[2:0], 0x00~0x07
    :param pVbaisCtr:   bit[3]
    :param pVbais:      bit[9:4], 0x00~0x3f
    :param pMirr:       bit[10], 1: enable mirror output
    :param pDis:        bit[12], 1: disable TIA
    :return:
    """
    mask = pGain | (pVbaisCtr << 3) | (pVbais << 4) | (pMirr << 10) | (pDis << 12)
    pi22_i2c_write(pBdg, pAddr, 0x11, 0x00, mask)


"""ADC function"""
def pi22_adc_cfg_one(pADC_SHSEL, pAdcGain = 0, pHiz = 1, pAvr = 0b11, pAcqT = 0b11, pCh =0):
    """
    :param pADC_SHSEL:         bit[3:0], 0x00----0x0f, 16 channel,
    :param pAdcGain:    bit[4], 0----Vref, 1----2*Vref,
    :param pHiz:        bit[5]
                            0----precharge not applied
                            1----precharge is applied for half acq time if the golbal disable_precharge = 0 (only applicable to some channels)

    :param pAvr:        bit[7:6], 0~3,
                            Average of '4 * pAvr' samples
    :param pAcqT:       bit[9:8], 0~3,
                            00 - Acq Time = As per ADC timing reg
                            01 - Acq Time = 2us
                            10 - Acq Time = 3.5us
                            11 - Acq Time = 5us
    :param pCh:         seleclt ADC switch acq, default use 0 channel
    :return:
    """
    mask = pADC_SHSEL | (pAdcGain<<4) | (pHiz<<5) | (pAvr<<6) | (pAcqT<<8)
    pi22_i2c_write(pBdg, pAddr, 0x03, 0x00+pCh, mask)

def pi22_adc_cfg_seq(pStart, pEnd):
    """
    from pStart to pEnd
    :param pStart: bit[11:8], 0----f
    :param pEnd: bit[3:0], 0----f
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x03, 0x32, (pStart<<8) + pEnd)

def pi22_adc_cfg_ctrl(pMode = 1, pAlar = 0, pPreC = 0, pClock = 1, pStatus = 1):
    """
    :param pMode: bit[0], 0----single, 1----continuous
    :param pAlar: bit[2], Alarm Mode select; 0: Non-latch mode; 1: Latch mode
    :param pPreC: bit[3], 0----ADC pre-charge buffer enabled for internal channels
                          1----Pre-charge function is disabled
    :param pClock: bit[6], 0----16MHz, 1----8MHz
    :param pStatus: bit[7], 0----Disable ADC function, 1----Enable ADC function
    :return:
    """
    mask = pMode | (pAlar<<2) | (pPreC<<3) | (pClock<<6) | (pStatus<<7)
    pi22_i2c_write(pBdg, pAddr, 0x03, 0x33, mask)    # Precharge disable, Non-latch, 0 to Vref, 连续采样

def pi22_adc_readbuf(pCh=0):
    """
    :param pCh: 0~F
    :return:
    """
    temp = pi22_i2c_read(pBdg, pAddr, 0x04, 0x00+pCh)
    return temp

def pi2x_adc_avr(pADC_ch, pCount):
    adc_list = []
    for i in range(pCount):
        temp = pi22_adc_readbuf(pADC_ch)  # ADC channel 12
        temp = int(temp, 16)  # adc 十进制
        print("{}\t".format(temp), end='')
        adc_list.append(temp)
        time.sleep(0.005)
    remaining_adc_list = adc_list[4:]  # ? 列表切片，从索引4到末尾
    avr = sum(remaining_adc_list) // len(remaining_adc_list)
    print("----{}\t".format(avr), end='')
    return avr

""" TEC function， B08Axx"""
def pi22_tec_cfg(pTecOn = 1, pManu = 1, pDisOCP = 1):
    """
    :param pTecOn: 0 or 1----Enable TEC operation
    :param pManu:  0 or 1----Manual duty mode
    :param pDisOCP:   0 or 1----disable over current detection
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x08, 0x0A, 0x0000)
    pi22_i2c_write(pBdg, pAddr, 0x08, 0x07, pTecOn | (pManu << 1) | (pDisOCP << 2))

def pi22_tec_manual_PN_set(pCode):
    """
    :param pCode: 0x0000~0x7fff; 0xff00~0x8000
    :return:
    """
    pi22_i2c_write(pBdg, pAddr, 0x08, 0x08, pCode)

def printf(data):
    formatted_data = "0x{:04x}".format(data)
    print(formatted_data)



if __name__ == '__main__':
    " test case "
    pi22_i2c_write(pBdg, pAddr, 0x0b, 0x05, 0x0061)
    time.sleep(1)
    pi22_i2c_write(pBdg, pAddr, 0x0b, 0x06, 0x000e)
