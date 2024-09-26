
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def carDataGen(num_rows, filename):
    data = {
        'RPM': np.random.randint(1000, 2000,size=num_rows),
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Experience data
    df['Tinj'] = np.random.randint(8, 15,size=num_rows)/10000
    df['Prail'] = np.random.randint(1000, 2000, size=num_rows)

    Pint = 230 #vamos considerar constante por enquanto
    Pdif = df['Prail'] - Pint
    Cd = 0.65
    A = 1
    rho = 850 #kg/m3
    Vinj = Cd * A * (2*Pdif /rho) * df['Tinj']
    df['Vinj cum'] = Vinj.cumsum()

    # Save to csv
    df.to_csv(filename, index=False)

carDataGen(1000,"carData_1.csv")
carDataGen(1000,"carData_2.csv")
carDataGen(1000,"carData_3.csv")
