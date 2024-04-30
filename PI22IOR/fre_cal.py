def calculate_frequency(time_str):
    # 解析输入字符串，提取数值和单位
    time_value = float(time_str[:-2])
    time_unit = time_str[-2:]

    # 根据单位转换时间为秒
    if time_unit == "us":
        time_seconds = time_value * 1e-6
    elif time_unit == "ms":
        time_seconds = time_value * 1e-3
    elif time_unit == "ns":
        time_seconds = time_value * 1e-9
    else:
        print("Unsupported time unit. Please use 'us', 'ms', or 'ns'.")
        return

    # 计算频率
    frequency_hz = 1 / time_seconds

    # 根据频率大小选择合适的单位进行输出
    if frequency_hz >= 1e6:
        print(f"Frequency: {frequency_hz / 1e6} MHz")
    elif frequency_hz >= 1e3:
        print(f"Frequency: {frequency_hz / 1e3} kHz")
    else:
        print(f"Frequency: {frequency_hz} Hz")

# 示例输入
time_str = input("Enter the period (e.g., 100us, 20ms, 400ns): ")
calculate_frequency(time_str)
print(1.767*0.6/1.24)