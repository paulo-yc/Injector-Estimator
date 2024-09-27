import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

A = 1
rho = 850

# Function to calculate Vinj cum based on given Cd and Pint for a DataFrame
def calculate_Vinj_cum(Cd, Pint, df):

    Pdif = df['Prail'] - Pint
    Vinj = Cd * A * np.sqrt(2 * Pdif*100 / rho) * df['Tinj']/1000000
    df['Vinj cum'] = Vinj.cumsum()
    return df['Vinj cum'].iloc[-1]

# Objective function to minimize the difference for all datasets
def objective(params, dataframes, target_volumes):
    Cd, Pint = params
    total_error = 0
    
    # Loop over all dataframes to calculate total error
    for i, df in enumerate(dataframes):
        Vinj_cum_pred = calculate_Vinj_cum(Cd, Pint, df)
        total_error += (Vinj_cum_pred - target_volumes[i]) ** 2  # Sum of squared errors
    
    return total_error

# Callback function to print partial results during optimization
def callback(params):
    Cd, Pint = params
    print(f"Partial results - Cd: {Cd:.4f}, Pint: {Pint:.2f}")

# Load all datasets
dfs = [pd.read_csv(f'carData_{i}.csv') for i in range(1, 6)]

# Get target volumes (the last value of 'Vinj cum' from each file)
target_volumes = [df['Tot Vol'].iloc[0] for df in dfs]

# Initial guesses for Cd and Pint
initial_guess = [0.1, 0.1]

# Bounds for Cd and Pint
bounds = [(0.01, 100), (30, 60)]

# Print the initial objective value
initial_objective_value = objective(initial_guess, dfs, target_volumes)
print(f"Initial objective value: {initial_objective_value}")

# Perform optimization with tighter tolerances and callback for partial results
result = minimize(
    objective, 
    initial_guess, 
    args=(dfs, target_volumes), 
    bounds=bounds, 
    method='L-BFGS-B', 
    callback=callback, 
    options={
        'disp': True,           # Display the optimization process
        'maxiter': 1000,        # Maximum number of iterations
        'ftol': 1e-20,          # Function tolerance for stopping
        'gtol': 1e-12,          # Gradient tolerance for stopping
    }
)

# Get the optimized Cd and Pint
Cd_opt, Pint_opt = result.x

# Display final results
print(f"Optimized Cd: {Cd_opt:.4f}, Pint: {Pint_opt:.2f}")





def carDataGen_optimized(Cd,Pint,df):

    Pdif = df['Prail'] - Pint
    A = 1
    rho = 850 #kg/m3
    Vinj = Cd * A * np.sqrt(2*Pdif*100000 /rho) * df['Tinj']/1000000
    df['Vinj_cum'] = Vinj.cumsum()

    df['Tot Vol'] =None
    df.at[0,'Tot Vol'] = df['Vinj_cum'].iloc[-1]

    fig, axs = plt.subplots(2,1,figsize=(10,6))
    axs[0].grid(True)
    axs[1].grid(True)

    axs[1].set_title("Estimated")
    axs[1].plot(df['RPM'])
    axs[1].plot(df['Tinj'])
    axs[1].plot(df['Prail'])
    axs[1].plot(df['Vinj_cum'])

    df2 = pd.read_csv("carData_1.csv")    
    axs[0].set_title("Experimental data (.csv)")
    axs[0].plot(df2['RPM'])
    axs[0].plot(df2['Tinj'])
    axs[0].plot(df2['Prail'])
    axs[0].plot(df2['Vinj_cum'])

    plt.tight_layout()
    plt.show()



#carDataGen_optimized(Cd_opt,Pint_opt,dfs[0])
carDataGen_optimized(0.47,60,dfs[0])


