import pandas as pd
from scipy.stats import levene, f_oneway, shapiro, ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from colorama import Fore, Style

tab = pd.read_csv('Planilhas/Planilha_Esteriotipia.csv', sep=',')
tab = tab.drop(columns=['ID','Data'])
tab = tab.dropna()

# Ajustar os valores da coluna 'Estresse'
tab['Estresse'] = tab['Estresse'].str.title().str.replace(' ', '')
tab['Período'] = tab['Período'].str.title().str.replace(' ', '')

if __name__ == "__main__":
  # Teste de normalidade total - SHAPIRO-WILK
  stat, p = shapiro(tab['Est_Total'])

  print(f'\n{Fore.BLUE}SHAPIRO-WILK{Style.RESET_ALL} - Teste de normalidade total')
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

  print(f'\n{Fore.GREEN}LEVENE{Style.RESET_ALL} - Teste de homogeneidade das variâncias por estresse')
  print(f"Estatística: {stat:.4f}")
  print(f"Valor-p: {p:.4f}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).\nFaça ANOVA.")

  # Teste de Levene por período
  stat, p = levene(tab.loc[tab['Período'] == 'Manhã', 'Est_Total'],
                    tab.loc[tab['Período'] == 'Tarde', 'Est_Total'])

  print(f'\n{Fore.GREEN}LEVENE{Style.RESET_ALL} - Teste de homogeneidade das variâncias por período')
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

  print(f'\n{Fore.YELLOW}ANOVA{Style.RESET_ALL} - Teste das variâncias dos grupos por estresse')
  print(f"Estatística F: {stat:.4f}")
  print(f"Valor-p: {p}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).")

  # Teste ANOVA por período
  stat, p = f_oneway(tab.loc[tab['Período'] == 'Manhã', 'Est_Total'],
                    tab.loc[tab['Período'] == 'Tarde', 'Est_Total'])

  print(f'\n{Fore.YELLOW}ANOVA{Style.RESET_ALL} - Teste das variâncias dos grupos por período')
  print(f"Estatística F: {stat:.4f}")
  print(f"Valor-p: {p}")
  if p < 0.05:
      print(f"As variâncias são significativamente diferentes (Rejeitamos H0).")
  else:
      print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).")

  # Teste T de Student por período
  stat, p = ttest_ind(tab.loc[tab['Período'] == 'Manhã', 'Est_Total'],
                      tab.loc[tab['Período'] == 'Tarde', 'Est_Total'])

  print(f'\n{Fore.RED}Teste T de Student{Style.RESET_ALL} por período')
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

  print(f'\n{Fore.YELLOW}Teste de Tukey{Style.RESET_ALL} por estresse')
  print(f'{tukey}\n')