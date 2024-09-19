
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Random car signals
num_rows = 10
data = {
    'RPM': np.random.randint(1000, 2000,size=num_rows),
}

# Create DataFrame
df = pd.DataFrame(data)

# Experience data
df['Tinj'] = np.random.randint(8, 15,size=num_rows)/10000
df['Prail'] = np.random.randint(1000, 2000, size=num_rows)
df['Pint'] = 100 #vamos considerar constante por enquanto
df['Pdif'] = df['Prail'] - df['Pint']
df['Cd'] = 0.7
df['A'] = 0.000001
df['rho'] = 850 #kg/m3
df['Vinj'] = df['Cd'] * df['A'] * np.sqrt(2*df['Pdif'] / df['rho']) * df['Tinj']
df['Vinj cum'] = df['Vinj'].cumsum()

# Save to csv
df.to_csv('carData.csv', index=False)


