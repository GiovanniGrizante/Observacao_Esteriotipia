import pandas as pd
from scipy.stats import levene, f_oneway, shapiro, ttest_ind, spearmanr, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from colorama import Fore, Style

tab = pd.read_csv('Planilhas/Planilha_Esteriotipia.csv', sep=',')
tab = tab.drop(columns=['ID','Data'])
tab = tab.dropna()

# Ajustar os valores da coluna 'Estresse'
tab['Estresse'] = tab['Estresse'].str.title().str.replace(' ', '')
tab['Período'] = tab['Período'].str.title().str.replace(' ', '')
tab['Estresse_Num'] = tab['Estresse'].map({'Alto': 3, 'Médio': 2, 'Baixo': 1, 'Nulo': 0})
#tab['Estresse_Num'] = tab['Estresse'].astype('category').cat.codes

est_tot_per = {'Manhã': tab.groupby('Período').get_group('Manhã').sum()['Est_Total'],
           'Tarde': tab.groupby('Período').get_group('Tarde').sum()['Est_Total']}

est_tot_est = {'Nulo': tab.groupby('Estresse').get_group('Nulo').sum()['Est_Total'],
         'Baixo': tab.groupby('Estresse').get_group('Baixo').sum()['Est_Total'],
         'Medio': tab.groupby('Estresse').get_group('Médio').sum()['Est_Total'],
         'Alto': tab.groupby('Estresse').get_group('Alto').sum()['Est_Total']}

n_per = {'Manhã': tab.groupby('Período').get_group('Manhã').sum()['N_total'],
         'Tarde': tab.groupby('Período').get_group('Tarde').sum()['N_total']}

n_est = {'Nulo': tab.groupby('Estresse').get_group('Nulo').sum()['N_total'],
         'Baixo': tab.groupby('Estresse').get_group('Baixo').sum()['N_total'],
         'Medio': tab.groupby('Estresse').get_group('Médio').sum()['N_total'],
         'Alto': tab.groupby('Estresse').get_group('Alto').sum()['N_total']}


ind_per = {'Manhã': est_tot_per['Manhã'] / (n_per['Manhã'] + est_tot_per['Manhã']),
           'Tarde': est_tot_per['Tarde'] / (n_per['Tarde'] + est_tot_per['Tarde'])}

ind_est = {'Nulo': est_tot_est['Nulo'] / (n_est['Nulo'] + est_tot_est['Nulo']),
           'Baixo': est_tot_est['Baixo'] / (n_est['Baixo'] + est_tot_est['Baixo']),
           'Medio': est_tot_est['Medio'] / (n_est['Medio'] + est_tot_est['Medio']),
           'Alto': est_tot_est['Alto'] / (n_est['Alto'] + est_tot_est['Alto'])}


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

    # Teste T de Student por período - Média
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

    # Teste de Correlação de Spearman entre Estresse_Num e Est_Total
    x = list(tab['Estresse_Num'])
    y = list(tab['Est_Total'])

    coef, p = spearmanr(x, y)

    print(f"{Fore.CYAN}Correlação de Spearman{Style.RESET_ALL} entre Estresse_Num e Est_Total")
    print(f"Coeficiente: {coef:.4f}")
    print(f"Valor-p: {p:.4e}")
    if p < 0.05:
        print("A correlação é estatisticamente significativa (Rejeitamos H0).\n")
    else:
        print("A correlação não é estatisticamente significativa (Falha ao rejeitar H0).\n")

    # Teste de Kruskal-Wallis por estresse
    stat, p = kruskal(tab.loc[tab['Estresse'] == 'Nulo', 'Est_Total'],
                      tab.loc[tab['Estresse'] == 'Baixo', 'Est_Total'],
                      tab.loc[tab['Estresse'] == 'Médio', 'Est_Total'],
                      tab.loc[tab['Estresse'] == 'Alto', 'Est_Total'])

    print(f'\n{Fore.MAGENTA}Kruskal-Wallis{Style.RESET_ALL} - Teste das variâncias dos grupos por estresse')
    print(f"Estatística H: {stat:.4f}")
    print(f"Valor-p: {p:.4e}")
    if p < 0.05:
        print(f"As variâncias são significativamente diferentes (Rejeitamos H0).\n")
    else:
        print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).\n")

    # Teste de Kruskal-Wallis por índice de esteriotipia do estresse
    stat, p = kruskal(ind_est['Nulo'],
                      ind_est['Baixo'],
                      ind_est['Medio'],
                      ind_est['Alto'])
    
    print(f'\n{Fore.MAGENTA}Kruskal-Wallis{Style.RESET_ALL} - Teste das variâncias dos grupos por índice de esteriotipia do estresse')
    print(f"Estatística H: {stat:.4f}")
    print(f"Valor-p: {p:.4e}")
    if p < 0.05:
        print(f"As variâncias são significativamente diferentes (Rejeitamos H0).\n")
    else:
        print(f"As variâncias não são significativamente diferentes (Não rejeitamos H0).\n")