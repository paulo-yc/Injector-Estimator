import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from objectiveFun import calculate_Vinj_cum,objective,callback

#Cd = 0.95
#Pint = 40 #bar
A = 0.000001
rho = 850 #kg/m3
const = A, rho

# Load all datasets
dfs = [pd.read_csv(f'carData_{i}.csv') for i in range(1, 6)]
df_concat = pd.concat(dfs, axis=0,ignore_index=True)

# Get target volumes (the last value of 'Vinj cum' from each file)
target_volumes = [df['Vinj_cum'].iloc[-1] for df in dfs]
target_volumes_pos = [len(df) for df in dfs]
target_volumes_pos = [x-1 for x in target_volumes_pos]
print("======Target Volumes and Positions")
print(f"target_volumes:{target_volumes}")
print(f"target_volumes_pos:{target_volumes_pos}")
print("\n")

# Accumulating volume as one big trip
target_volumes_cum = []
target_volumes_cum.append(target_volumes[0])
for i in range(1,5):
    target_volumes_cum.append(target_volumes_cum[i-1] + target_volumes[i])

# Accumulating volume position as one big trip
target_volumes_pos_cum = []
target_volumes_pos_cum.append(target_volumes_pos[0])
for i in range(1,5):
    target_volumes_pos_cum.append(target_volumes_pos_cum[i-1] + target_volumes_pos[i])

print("======Target Volumes and Positions (Accumulated)")
print(f"target_volumes_cum:{target_volumes_cum}")
print(f"target_volumes_pos_cum:{target_volumes_pos_cum}")
print("\n")

# Initial guesses for Cd and Pint
initial_guess = [0.1, 500]
print(f"Initial guess:{initial_guess}")

# Bounds for Cd and Pint
bounds = [(0.0, 10), (0, 1000)]

# Print the initial objective value
initial_objective_value = objective(initial_guess, const, df_concat,target_volumes_pos_cum, target_volumes_cum)
print(f"Initial objective value: {initial_objective_value}")

# Perform optimization with tighter tolerances and callback for partial results
result = minimize(
    objective, 
    initial_guess, 
    args=(const, df_concat, target_volumes_pos_cum, target_volumes_cum), 
    bounds=bounds, 
    method='L-BFGS-B', 
    callback=callback, 
    options={
        'disp': True,           # Display the optimization process
        'maxiter': 1000,        # Maximum number of iterations
        'ftol': 1e-9,          # Function tolerance for stopping
        'gtol': 1e-9,          # Gradient tolerance for stopping
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
carDataGen_estimated(Cd_opt,Pint_opt,dfs[4])


