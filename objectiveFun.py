import numpy as np

# Function to calculate Vinj cum based on given Cd and Pint for a DataFrame
def calculate_Vinj_cum(const, Cd, Pint, df):
    A, rho = const
    Pdif = df['Prail'] - Pint
    Vinj = Cd * A * np.sqrt(2 * Pdif*100000 / rho) * df['Tinj']/1000000
    #Vinj = Cd * A  + (2*Pdif*100000 /rho) * df['Tinj']/1000000 #simple one

    df['Vinj_cum'] = Vinj.cumsum()    
    return df['Vinj_cum']

# Objective function to minimize the difference for all datasets
# def objective(params, const, df, target_volsPos, target_vols):
#     Cd, Pint = params
#     A, rho = const
#     total_error = 0
    
#     # Loop over all dataframes to calculate total error
#     for i in range(len(target_vols)):        
#         Vinj_cum_pred = calculate_Vinj_cum(const, Cd, Pint, df)
#         total_error += (Vinj_cum_pred[target_volsPos[i]] - target_vols[i]) ** 2  # Sum of squared errors
        
#     print(f"total_error:{total_error}")

#     return total_error

# objective_with_penalty
def objective(params, const, df, target_volsPos, target_vols):
    Cd, Pint = params
    A, rho = const
    total_error = 0

    # Penalização para garantir que Pint está entre 0 e 1000
    if Pint < 0 or Pint > 1000:
        return 1e6  # Um valor grande que vai "punir" o otimizador
    
    # Calcula o erro acumulado normalmente
    for i in range(len(target_vols)):
        Vinj_cum_pred = calculate_Vinj_cum(const, Cd, Pint, df)
        total_error += (Vinj_cum_pred[target_volsPos[i]] - target_vols[i]) ** 2

    print(f"total_error:{total_error}")

    return total_error

# Callback function to print partial results during optimization
def callback(params):
    Cd, Pint = params
    print(f"Partial results - Cd: {Cd:.4f}, Pint: {Pint:.2f}")


    