import matplotlib.pyplot as plt
import main

# Gráfico de Boxplot dos Níveis de Estresse

# Obtendo os valores de máximo, mínimo e média para cada categoria de "Estresse"
val = main.tab.groupby('Estresse')['Est_Total'].agg(['max', 'min', 'mean'])#.apply(list, axis=1)

# Personalizando as cores e a linha central do boxplot
colors = ["#2E7D32", "#388E3C", '#66BB6A', '#81C784']  # Cores personalizadas

fig, ax = plt.subplots(1, 1)

# Criando o boxplot com cores personalizadas
box = ax.boxplot([val.iloc[0], 
                   val.iloc[2], 
                   val.iloc[1], 
                   val.iloc[3]],
                  patch_artist=True)

# Alterando as cores de cada box
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Alterando a linha central (mediana)
for median in box['medians']:
    median.set_color('black')  # Cor da linha central
    median.set_linewidth(1)    # Espessura da linha central

ax.set_xticklabels(["Alto", "Médio", "Baixo", "Nulo"])
ax.set_title("Gráfico de Esteriotipia por Níveis de Estresse")
ax.set_xlabel("Nível de Estresse")
ax.set_ylabel("Frequências de Estereotipia por Hora") 
plt.grid()
plt.show()


# Gráfico de Boxplot dos Períodos do Dia

# Obtendo os valores de máximo, mínimo e média para cada categoria de "Período"
val = main.tab.groupby('Período')['Est_Total'].agg(['max', 'min', 'mean']).apply(list, axis=1)
print(val)
# Personalizando as cores e a linha central do boxplot
colors = ["#F2C974", "#E6A175"]  # Cores personalizadas

fig, ax = plt.subplots(1, 1)

# Criando o boxplot com cores personalizadas
box = ax.boxplot([val.iloc[0], 
                   val.iloc[1]],
                  patch_artist=True)

# Alterando as cores de cada box
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Alterando a linha central (mediana)
for median in box['medians']:
    median.set_color('black')  # Cor da linha central
    median.set_linewidth(1)    # Espessura da linha central

ax.set_xticklabels(["Manhã", "Tarde"])
ax.set_title("Gráfico de Esteriotipia por Período do Dia")
ax.set_xlabel("Nível de Estresse")
ax.set_ylabel("Frequências de Estereotipia por Hora") 
plt.grid()
plt.show()