import pandas as pd
from scipy.stats import levene, f_oneway, shapiro, ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tab = pd.read_excel('Planilhas/Planilha_Esteriotipia.xlsx')
tab = tab.drop(columns=['ID','Data'])
tab = tab.dropna()

if __name__ == "__main__":
  # Teste de normalidade total - SHAPIRO-WILK
  stat, p = shapiro(tab['Est_Total'])

  print('\nTeste de normalidade total - SHAPIRO-WILK:\n')
  print(f"Estatística: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p > 0.05:
      print(f'A amostra parece vir de uma distribuição normal (Falha ao rejeitar H0)')
  else:
      print(f'A amostra não parece vir de uma distribuição normal (Rejeitar H0)')

  # Teste de normalidade por período - SHAPIRO-WILK
  # print('\n',tab2.apply(stats.shapiro))  # Função groupby não funciona

  # Teste de Levene por estresse
  stat, p = levene(tab.loc[tab['Estresse'] == 'Baixo', 'Est_Total'],
                    tab.loc[tab['Estresse'] == 'Médio', 'Est_Total'],
                    tab.loc[tab['Estresse'] == 'Alto', 'Est_Total'],
                    tab.loc[tab['Estresse'] == 'Nulo', 'Est_Total'])

  print('\nTeste de homogeneidade das variâncias por estresse - LEVENE\n')
  print(f"Estatística: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).\nFaça ANOVA.")

  # Teste de Levene por período
  stat, p = levene(tab.loc[tab['Período'] == 'Manhã', 'Est_Total'],
                    tab.loc[tab['Período'] == 'Tarde', 'Est_Total'])

  print('\nTeste de homogeneidade das variâncias por período - LEVENE\n')
  print(f"Estatística: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).\nFaça ANOVA.")

  # Teste ANOVA por estresse
  stat, p = f_oneway(tab.loc[tab['Estresse'] == 'Baixo', 'Est_Total'],
                    tab.loc[tab['Estresse'] == 'Médio', 'Est_Total'],
                    tab.loc[tab['Estresse'] == 'Alto', 'Est_Total'],
                    tab.loc[tab['Estresse'] == 'Nulo', 'Est_Total'])

  print('\nTeste das variâncias dos grupos por estresse - ANOVA\n')
  print(f"Estatística F: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).")

  # Teste ANOVA por período
  stat, p = f_oneway(tab.loc[tab['Período'] == 'Manhã', 'Est_Total'],
                    tab.loc[tab['Período'] == 'Tarde', 'Est_Total'])

  print('\nTeste das variâncias dos grupos por período - ANOVA')
  print(f"Estatística F: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).")

  # Teste T de Student por período
  stat, p = ttest_ind(tab.loc[tab['Período'] == 'Manhã', 'Est_Total'],
                      tab.loc[tab['Período'] == 'Tarde', 'Est_Total'])

  print('\nTeste T de Student por período')
  print(f"Estatística T: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p < 0.05:
      print(f"As médias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As médias não são significativamente diferentes (Não rejeitamos H0).")

  # Teste de Tukey por estresse
  tukey = pairwise_tukeyhsd(endog=tab['Est_Total'],
                            groups=tab['Estresse'],
                            alpha=0.05)

  print('\nTeste de Tukey por estresse')
  print(f'{tukey}\n')