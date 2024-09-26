import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import glob

# Path to multiples .csv
filePaths = glob.glob('carData_*.csv')

# Read multiples .csv and store it as a DataFrame list
df_list = [pd.read_csv(file) for file in filePaths]

# Define the real total volume (last row of Vinj cum)
real_total_volume = df_list[0]['Vinj cum'].iloc[-1]  # Example value in liters (adjust as needed)
print(f"real_total_volume: {real_total_volume}")

# Vinj function
def calc_vinj(params, df):
    Cd, Pint = params
    return Cd * df['A'] * np.sqrt(2 * (df['Prail'] - Pint) / df['rho']) * df['Tinj']

# Objective function to minimize the difference between cumulative Vinj and the real total volume
def objective(params, df, real_total_volume):
    Cd, Pint = params
    df['Vinj'] = calc_vinj(params, df)
    calculated_total_volume = df['Vinj'].cumsum().iloc[-1]  # Last row of cumulative Vinj
    return abs(calculated_total_volume - real_total_volume)

# Initial guess for Cd and Pint
initial_params = [0.1, 80]  # Example initial guesses (adjust as needed)

optimization_options = {
    'maxiter': 10000,  # Maximum number of iterations
    'xatol': 1e-6,    # Tolerance for changes in parameters
    'fatol': 1e-6,    # Tolerance in the value of the objective function
}

# Run the optimization
result = minimize(objective, initial_params, args=(df_list[0], real_total_volume), 
                  method='Nelder-Mead', options=optimization_options)

# Optimal values of Cd and Pint
optimal_Cd, optimal_Pint = result.x

# Display results
print(f"Optimal value of Cd: {optimal_Cd:.5f}")
print(f"Optimal value of Pint: {optimal_Pint:.5f}")

# Optional: Plot data
# plt.figure(figsize=(10, 6))  # figure size
# plt.plot(df.index, df['Vinj'], marker='o', label='Vinj')  
# plt.plot(df.index, df['Vinj cum'], marker='o', label='Vinj cum')  

# plt.title('Vinj and Vinj cum')
# plt.xlabel('Index')
# plt.ylabel('Values')
# plt.grid(True)  # Add a grid
# plt.show()
