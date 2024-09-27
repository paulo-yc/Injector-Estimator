
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def stable_rpm(rpm_value, duration):
    return np.full(duration, rpm_value)

def changing_rpm(start_rpm, end_rpm, duration):
    return np.linspace(start_rpm, end_rpm, duration)

# RPM values and intervals
total_time = 600  # Total seconds
intervals = [60, 120, 90, 150, 80, 100] 
rpm_values = [1000, 2000, 1500, 2500, 1800, 2200] 

# RPM variation
rpm_data = np.array([])
for i in range(len(intervals) - 1):
    stable_part = stable_rpm(rpm_values[i], int(intervals[i] * 0.5))  # Período estável (metade do intervalo)
    changing_part = changing_rpm(rpm_values[i], rpm_values[i + 1], int(intervals[i] * 0.5))  # Aceleração/desaceleração
    rpm_data = np.concatenate((rpm_data, stable_part, changing_part))

# Last stable phase
rpm_data = np.concatenate((rpm_data, stable_rpm(rpm_values[-1], intervals[-1])))


def carDataGen(num_rows, filename):
    data = {
        'RPM': rpm_data,
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Experience data
    df['TinjA'] = df['RPM']/1000 * np.random.randint(300, 500,size=num_rows)
    df['TinjB'] = df['RPM']/1000 * np.random.randint(500, 900,size=num_rows)
    df['Tinj'] = df['TinjA'] + df['TinjB'] # microsecond
    df['Prail'] = df['RPM'] * np.random.uniform(0.9, 1.1, size=num_rows)

    Pint = 60 #bar
    Pdif = df['Prail'] - Pint
    Cd = 0.8
    A = 1
    rho = 850 #kg/m3
    Vinj = Cd * A * np.sqrt(2*Pdif*100000 /rho) * df['Tinj']/1000000
    df['Vinj_cum'] = Vinj.cumsum()

    df['Tot Vol'] =None
    df.at[0,'Tot Vol'] = df['Vinj_cum'].iloc[-1]

    # Save to csv
    df.to_csv(filename,float_format='%.5f', index=False)



carDataGen(total_time,"carData_1.csv")
carDataGen(total_time,"carData_2.csv")
carDataGen(total_time,"carData_3.csv")
carDataGen(total_time,"carData_4.csv")
carDataGen(total_time,"carData_5.csv")





