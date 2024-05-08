import time

from instruments.DP821A import *
from pi22_lib import *
from instruments.instruments_name import *
from excel.excel_api import *
import numpy as np

# pBdg = hid.device()  # create hid device
# pBdg.open(0x1A86, 0xFE07)
# pAddr = 0x80

smuid = smu_2460_id
dmmid = dmm_9060_num14_id
powerid = DP821A_id
dmmid2 = dmm_34461_num1_id


def buck_load(load_current,row,file_path):

    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)  # SMU LOAD BUCK_OUTPUT
    dmm = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid) # 9060 Vref
    dmm2 = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid2) # 34461 Power_Current
    power = Power_DP821A(pyvisa.ResourceManager(),powerid)  # Power Power_voltage



    i = load_current # 负载


    # smu.sum2450_force_cur_sens_volt_init(-0.1, 5,1, 5, 0.1) # 初始化 手动初始化比较好
    smu.smu_sour_ii(-i,2) # 提供电流 1是能提供的最大电流
    time.sleep(0.1) # 延迟等待负载稳定

    buck_output = smu.smu_2450_meas_v(1) # 测量电压 四线
    time.sleep(0.1)  # 延迟等待负载稳定
    load = i
    time.sleep(0.1)  # 延迟等待负载稳定
    power_voltage = power.read_voltage(2)
    time.sleep(0.1)  # 延迟等待负载稳定
    power_current = dmm2.read_current()
    time.sleep(0.1)  # 延迟等待负载稳定
    vref = dmm.read_voltage()
    time.sleep(0.1)  # 延迟等待负载稳定


    ins_xls_ = Xls_File(file_path)
    ins_xls_.xls_open()

    column = ins_xls_.xls_append_column()
    ins_xls_.xls_write(row, column, buck_output)
    ins_xls_.xls_write(row+1, column, load)
    ins_xls_.xls_write(row+2, column, power_voltage)
    ins_xls_.xls_write(row+3, column, power_current)
    ins_xls_.xls_write(row+4, column, vref)

    ins_xls_.xls_close()


#_________________________________________________________________________________________________
    # finalize_excel(app, wb, filepath)

    """
    1. 手动打开电源1 2 通道,及通道2感测
    2. 检查一下是否能在Buck 探测到电压
    3. 能够探测到电压再检测一下是否能手动加到0.8A的电流
    4. 一切确定好之后,关闭电源,再连接电路
    5. 开始写代码
    """

def buck_efficiency_sweep(row,filepath):
    """
    1. 打开感测
    """
    power = Power_DP821A(pyvisa.ResourceManager(), powerid)  # Power Power_voltage
    power.set_volta_current(1,3.3,1)
    power.set_volta_current(2,3.3,2)
    power.turn_on_off(1,"ON")
    power.turn_on_off(2, "ON")

    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)  # SMU LOAD BUCK_OUTPUT
    smu.smu2450_reset()
    smu.sum2450_force_cur_sens_volt_init(0, 5, 2, 5, 0.1)  # 初始化 手动初始化比较好

    pi22_chipid()
    pi22_unlock() # 只有解锁了才能trim buck frequency

    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x08FC)  # Trim fre to  1.7MHZ

    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x00F0)  # Trim fre to ?M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x00FC)  # Trim fre to 2.2M

    pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x008C)  # Trim fre to 2.2M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x0780)  # Trim fre to 3.9062M

    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x000C)  # Trim fre to 2.2M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x0700)  # Trim fre to 3.9062M

    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x00FC)  # Trim fre to 2.2M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x07F0)  # Trim fre to 3.9062M

    smu.smu_off()
    time.sleep(1)

    buck_cfg(1) # 打开Buck
    for i in range(0,0X0AA0,0X0020):
        buck_vest(i) # 1.8V

    time.sleep(1)
    smu.smu_on()


    """上面是仪器操作,下面是Excel表格操作"""


    for i in np.arange(0,1.55,0.05):
        buck_load(i,row,filepath)

    power.turn_on_off(1,"OFF")
    power.turn_on_off(2, "OFF")
    smu.smu2450_reset()
    smu.smu_off()

if __name__ == "__main__":
    buck_efficiency_sweep(40, "../00FC/Buck_2M8.xlsx")









