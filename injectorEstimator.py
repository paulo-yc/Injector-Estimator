import pandas as pd
import matplotlib.pyplot as plt

# Path to .csv
filePath = 'carData.csv'

# Read .csv and store it as a DataFrame
df = pd.read_csv(filePath)


plt.figure(figsize=(10, 6))  # Define o tamanho da figura
# for column in df.columns:
#     plt.plot(df.index, df[column], marker='o', label=column)  # Plota todas as colunas no mesmo gráfico

plt.plot(df.index, df['Vinj'], marker='o', label='Vinj')  
plt.plot(df.index, df['Vinj cum'], marker='o', label='Vinj cum')  

plt.title('Gráfico de todas as colunas')
plt.xlabel('Índice')
plt.ylabel('Valores')
plt.legend()  # Adiciona uma legenda para identificar cada coluna
plt.grid(True)  # Adiciona uma grade
plt.show()  # Exibe o gráfico