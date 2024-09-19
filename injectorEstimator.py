import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Path to .csv
filePath = 'carData.csv'

# Read .csv and store it as a DataFrame
df = pd.read_csv(filePath)

# Define the real total volume (last row of Vinj cum) 
real_total_volume = df['Vinj cum'].iloc[-1]  # Example value in liters (adjust as needed)
print(f"real_total_volume: {real_total_volume}")

# Vinj function
def calc_vinj(Cd, df):
    return Cd * df['A'] * np.sqrt(2 * df['Pdif'] / df['rho']) * df['Tinj']

# Objective function to minimize the difference between cumulative Vinj and the real total volume
def objective(Cd, df, real_total_volume):
    df['Vinj'] = calc_vinj(Cd, df)
    calculated_total_volume = df['Vinj'].cumsum().iloc[-1]  # Last row of cumulative Vinj
    return abs(calculated_total_volume - real_total_volume)

# Initial guess for Cd
initial_Cd = 0.1

optimization_options = {
    'maxiter': 1000,  # Maximum number of iterations
    'xatol': 1e-6,     # Tolerance for changes in Cd values
    'fatol': 1e-6,     # Tolerance in the value of the objective function
}

# Run the optimization
result = minimize(objective, initial_Cd, args=(df, real_total_volume), 
                  method='Nelder-Mead', options=optimization_options)

# Optimal value of Cd
optimal_Cd = result.x[0]

# Display result
print(f"Optimal value of Cd: {optimal_Cd:.5f}")


# # Plot data
# plt.figure(figsize=(10, 6))  # figure size

# plt.plot(df.index, df['Vinj'], marker='o', label='Vinj')  
# plt.plot(df.index, df['Vinj cum'], marker='o', label='Vinj cum')  

# plt.title('Vinj and Vinj cum')
# plt.xlabel('Index')
# plt.ylabel('Values')
# plt.grid(True)  # Adiciona uma grade
# plt.show()  