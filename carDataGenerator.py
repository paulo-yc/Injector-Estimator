
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

Cd = 0.6
Pint = 160 #bar

A = 0.000001
rho = 850 #kg/m3

def stable_rpm(rpm_value, duration):
    return np.full(duration, rpm_value)

def changing_rpm(start_rpm, end_rpm, duration):
    return np.linspace(start_rpm, end_rpm, duration)

# RPM values and intervals
time_scale = 10
intervals = np.array([60, 120, 90, 150, 80, 100, 50])
intervals = intervals*time_scale
rpm_values = [1000, 2000, 1500, 2500, 1800, 1300,1000] 
total_time = sum(intervals) # Total seconds

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

    Pdif = df['Prail'] - Pint

    Vinj = Cd * A * np.sqrt(2*Pdif*100000 /rho) * df['Tinj']/1000000
    #Vinj = Cd * A  + (2*Pdif*100000 /rho) * df['Tinj']/1000000 #simple one
    df['Vinj_cum'] = Vinj.cumsum()

    #df['Tot Vol'] =None
    #df.at[0,'Tot Vol'] = df['Vinj_cum'].iloc[-1]

    # Save to csv
    df.to_csv(filename,float_format='%.10f', index=False)



carDataGen(total_time,"carData_1.csv")
carDataGen(total_time,"carData_2.csv")
carDataGen(total_time,"carData_3.csv")
carDataGen(total_time,"carData_4.csv")
carDataGen(total_time,"carData_5.csv")





