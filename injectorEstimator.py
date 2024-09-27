import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#Cd = 0.95
#Pint = 40 #bar
A = 0.000001
rho = 850 #kg/m3

# Function to calculate Vinj cum based on given Cd and Pint for a DataFrame
def calculate_Vinj_cum(Cd, Pint, df):
    Pdif = df['Prail'] - Pint
    Vinj = Cd * A * np.sqrt(2 * Pdif*100000 / rho) * df['Tinj']/1000000
    df['Vinj cum'] = Vinj.cumsum()
    return df['Vinj cum'].iloc[-1]

# Objective function to minimize the difference for all datasets
def objective(params, df, target_vols):
    Cd, Pint = params
    total_error = 0
    
    # Loop over all dataframes to calculate total error
    for i in range(len(target_vols)):
        Vinj_cum_pred = calculate_Vinj_cum(Cd, Pint, df)
        total_error += (Vinj_cum_pred - target_vols[i]) ** 2  # Sum of squared errors
    
    return total_error

# Callback function to print partial results during optimization
def callback(params):
    Cd, Pint = params
    print(f"Partial results - Cd: {Cd:.4f}, Pint: {Pint:.2f}")

# Load all datasets
dfs = [pd.read_csv(f'carData_{i}.csv') for i in range(1, 6)]
df_concat = pd.concat(dfs, axis=0)

# Get target volumes (the last value of 'Vinj cum' from each file)
target_volumes = [df['Vinj_cum'].iloc[-1] for df in dfs]

# Accumulating volume as one big trip
target_volumes_cum = []
target_volumes_cum.append(target_volumes[0])
for i in range(1,5):
    target_volumes_cum.append(target_volumes_cum[i-1] + target_volumes[i])

print(target_volumes)
print(target_volumes_cum)

# Initial guesses for Cd and Pint
initial_guess = [0.7, 500]

# Bounds for Cd and Pint
bounds = [(0.3, 10), (10, 500)]

# Print the initial objective value
initial_objective_value = objective(initial_guess, df_concat, target_volumes_cum)
print(f"Initial objective value: {initial_objective_value}")

# Perform optimization with tighter tolerances and callback for partial results
result = minimize(
    objective, 
    initial_guess, 
    args=(df_concat, target_volumes), 
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





def carDataGen_estimated(Cd,Pint,df):

    #Estimated
    Pdif = df['Prail'] - Pint
    Vinj = Cd * A * np.sqrt(2*Pdif*100000 /rho) * df['Tinj']/1000000
    df['Vinj_cum'] = Vinj.cumsum()
    #df['Tot Vol'] =None
    #df.at[0,'Tot Vol'] = df['Vinj_cum'].iloc[-1]

    #experimental
    df2 = pd.read_csv("carData_1.csv") 

    #plot comparison
    fig, axs = plt.subplots(2,1,figsize=(10,6))   
    axs[0].set_title("Experimental data (.csv)")
    axs[0].plot(df2['RPM'],label="RPM")
    axs[0].plot(df2['Tinj'],label="Tinj")
    axs[0].plot(df2['Prail'],label="Prail")
    #axs[0].plot(df2['Vinj_cum'],label="Vinj_cum")
    axs[0].legend()    
    axs[0].grid(True)

    axs[1].set_title(f"Estimated - Cd:{Cd:.5f} - Pint{Pint:.5f}")
    axs[1].plot(df['Vinj_cum'],label="Vinj_cum estimated")
    axs[1].plot(df2['Vinj_cum'],label="Vinj_cum experimental")
    axs[1].legend()
    axs[1].grid(True)



    plt.tight_layout()
    plt.show()



carDataGen_estimated(Cd_opt,Pint_opt,dfs[0])
carDataGen_estimated(Cd_opt,40,dfs[0])
carDataGen_estimated(Cd_opt,400,dfs[0])
carDataGen_estimated(Cd_opt,30,dfs[0])
carDataGen_estimated(Cd_opt,0,dfs[0])
# carDataGen_optimized(Cd_opt,Pint_opt,dfs[1])
# carDataGen_optimized(Cd_opt,Pint_opt,dfs[2])
# carDataGen_optimized(Cd_opt,Pint_opt,dfs[3])
#carDataGen_optimized(0.47,60,dfs[0])


