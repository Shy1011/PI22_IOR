"""
Author : RanShuai
Date : 2024/04/15

"""

"""
Question : 
Buck一开,Vref的值会下降
"""
from pi22_lib import *

if __name__ == "__main__":
    # pi22_chipid()

    pi22_unlock()
    pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x0780) # Trim fre to 3.9062M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x0380) # Trim fre to 3M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x018C)  # Trim fre to 2.4M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x008C)  # Trim fre to 2.2M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x00F0)  # Trim fre to 2.9M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x00FC)  # Trim fre to 2.2M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x00F8)  # Trim fre to 2.5                                                                      M
    # pi22_i2c_write(pBdg, pAddr, 0x21, 0x02, 0x08FC)  # Trim fre to  1.7MHZ                                                      M


    # PID
    # pi22_i2c_write(pBdg, pAddr, 0x07, 0x07, 0                                                                                                                                                                                                                                                   x07F0)
    # pi22_i2c_write(pBdg, pAddr, 0x07, 0x07, 0x038C) # 20 2M
    # pi22_i2c_write(pBdg, pAddr, 0x07, 0x07, 0x030C)  # Trim frequency to  2M
    # pi22_i2c_write(pBdg, pAddr, 0x07, 0x07, 0x0380)  # Trim frequency to  2M
    # pi22_i2c_write(pBdg, pAddr, 0x07, 0x07, 0x0700)  #

    # time.sleep(1)

    # pi22_chip_status()

    # external_reset() # input inside

    # i2c_com()

    # soft_reset_test()

    # soft_reset() # 这个只是测试用不用每次都reset
    # pi22_i2c_write(pBdg, 0x80, 0x21, 0x02, 0x0700)  # adjust buck fre to 4Mhz

    # vref_powerdown(0) # enable Vref


    # """Buck Open"""
    # buck_cfg(1)
    # buck_vest(0XFFF)

    # """ADC single Sequence"""
    # adc_single_seq_test(5,0)

    # """ADC Continious Mode"""
    # adc_continious_seq_test(6,0)

    # """ADC Average Mode"""
    # adc_average_test(acerSel=0b00,avrTime=1)
    # adc_average_test(acerSel=0b01, avrTime=4)
    # adc_average_test(acerSel=0b10, avrTime=8)
    # adc_average_test(acerSel=0b11, avrTime=16)


    # """adc acquision time test"""
    # acquision_time()

    # """MUX test"""
    # read_all_channels()

    """Read the adc result data from the ADC Register"""
    # adc_continious_seq(6, 1) # PVDD = 3.3V
    # buck_cfg(1)
    # buck_vest(0xA70)  # buck  = 1.8v
    # adc_continious_seq(5, 0)  # Vbuck = 2.5V Max
    # adc_continious_seq(7, 1)  # DVDD = 3.3V
    #
    """Threshold Test / Alarm Test /Intb Test"""
    # intb_test(adcChannel= 6,lo = 0x0A00, hi = 0x0FFF) # PVDD no alarm
    # intb_test(adcChannel=5,lo=0x0000, hi=0x0FFF)  # BUCK alarm
    # intb_test(adcChannel=7, lo=0x0F00, hi=0x0FFF)  # DVDD alarm

    """Above are the blue parts."""




    """Below are Buck specific characteristics"""

    """output_voltage_range 1.2 - 2.5V"""
    # output_voltage_range()

    """Load Current"""
    pi22_chipid()
    load_current() # set Vbuck to 1.8V
    # pi22_i2c_write(pBdg, pAddr, 0x01, 0x02, 0x0000) # Disable the IDAC
    # pi22_i2c_read(pBdg, pAddr, 0x01, 0x02) # Disable the IDAC


    # """Current Test"""
    # load_regulation()
    # load_regulation()

    # """Test if can output current from 0 - 1.5 A"""
    # load_current()

    # buck_cfg(1)
    # buck_vest(0x0A80)  # buck  = 1.8v
    """ Output setpoint resolution """
    # output_setpoint_resolution()

    """"""

    """Below are Nrail specific characteristics"""
    # pi22_nrail_en()
    # pi22_nrail_set(0x0000)





