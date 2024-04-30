import time

from instruments.DP821A import *
from pi22_lib import *
from instruments.instruments_name import *
from excel.excel_api import *
import numpy as np

# pBdg = hid.device()  # create hid device
# pBdg.open(0x1A86, 0xFE07)
# pAddr = 0x80

smuid = smu_2450_id
dmmid = dmm_9060_num14_id
powerid = DP821A_id
dmmid2 = dmm_34461_num1_id


def buck_load(sheet0,load_current):

    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)  # SMU LOAD BUCK_OUTPUT
    dmm = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid) # 9060 Vref
    dmm2 = DmmGwinstek9061(pyvisa.ResourceManager(), dmmid2) # 34461 Power_Current
    power = Power_DP821A(pyvisa.ResourceManager(),powerid)  # Power Power_voltage



    i = load_current # 负载


    # smu.sum2450_force_cur_sens_volt_init(-0.1, 5,1, 5, 0.1) # 初始化 手动初始化比较好
    smu.smu_sour_ii(-i,1) # 提供电流 1是能提供的最大电流
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


    # write(sheet, '张三', '李四', '王五')
    data_insert(sheet0, buck_output, 1) # Buck Output
    data_insert(sheet0, load, 2) # Load
    data_insert(sheet0, power_voltage, 3) # Power Voltage
    data_insert(sheet0, power_current, 4) # Power Current
    data_insert(sheet0, vref, 5) # Vref


#_________________________________________________________________________________________________
    # finalize_excel(app, wb, filepath)

    """
    1. 手动打开电源1 2 通道,及通道2感测
    2. 检查一下是否能在Buck 探测到电压
    3. 能够探测到电压再检测一下是否能手动加到0.8A的电流
    4. 一切确定好之后,关闭电源,再连接电路
    5. 开始写代码
    """

def buck_efficiency_sweep():
    """
    1. 打开电源
    2. SMU设置为 强制电流测电压
    3. 运行代码

    """
    power = Power_DP821A(pyvisa.ResourceManager(), powerid)  # Power Power_voltage
    power.turn_on_off(1,"ON")
    power.turn_on_off(2, "ON")

    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)  # SMU LOAD BUCK_OUTPUT
    smu.sum2450_force_cur_sens_volt_init(-0.1, 5, 1, 5, 0.1)  # 初始化 手动初始化比较好

    pi22_chipid()
    pi22_unlock()  # 只有解锁了才能trim buck frequency

    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x008C)  # Trim fre to 2.2M
    pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x0780)  # Trim fre to 3.9062M

    smu.smu_off()
    time.sleep(1)

    buck_cfg(1)  # 打开Buck
    buck_vest(0x0A80)  # 1.8V

    time.sleep(1)
    smu.smu_on()

    """上面是仪器操作,下面是Excel表格操作"""

    filepath = "results/Buck_4M.xlsx"
    app, wb = initialize_excel(filepath)
    sheet = wb.sheets[0]

    for i in np.arange(0, 0.85, 0.05):
        buck_load(sheet,i)

    finalize_excel(app, wb, filepath)

if __name__ == "__main__":
    """
    1. 打开电源
    2. SMU设置为 强制电流测电压
    3. 打开感测
    3. 运行代码
    """
    smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)  # SMU LOAD BUCK_OUTPUT
    # smu.sum2450_force_cur_sens_volt_init(-0.1, 5, 1, 5, 0.1)  # 初始化 手动初始化比较好

    pi22_chipid()
    pi22_unlock() # 只有解锁了才能trim buck frequency

    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x008C)  # Trim fre to 2.2M
    pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x0780)  # Trim fre to 3.9062M

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

    filepath = "results/Buck_4M7.xlsx"
    app, wb = initialize_excel(filepath)
    sheet = wb.sheets[0]

    for i in np.arange(0,0.9,0.1):
        buck_load(sheet,i)


    finalize_excel(app, wb, filepath)









