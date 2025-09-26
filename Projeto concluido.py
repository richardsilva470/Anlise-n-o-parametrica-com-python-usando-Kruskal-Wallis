import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal
import scikit_posthocs as sp

xlsx = pd.ExcelFile('Dados da Paraiba atualizado.xlsx')
print("Planilhas disponíveis:", xlsx.sheet_names)
Borborema_df = 'Borborema'
AgresteParaibano_df = 'AgresteParaibano'
MataParaibana_df = 'MataParaibana'
SertãoParaibano_df = 'SertãoParaibano'
df1 = pd.read_excel('Dados da Paraiba atualizado.xlsx', sheet_name=Borborema_df)
df1['região'] = Borborema_df
df2 = pd.read_excel('Dados da Paraiba atualizado.xlsx', sheet_name=AgresteParaibano_df)
df2['região'] = AgresteParaibano_df
df3 = pd.read_excel('Dados da Paraiba atualizado.xlsx', sheet_name=MataParaibana_df)
df3['região'] = MataParaibana_df
df4 = pd.read_excel('Dados da Paraiba atualizado.xlsx', sheet_name=SertãoParaibano_df)
df4['região'] = SertãoParaibano_df
df = pd.concat([df1, df2, df3, df4], ignore_index=True)
df.head()

df = df.dropna()
df = df[df['Mortalidade infantil - óbitos por mil nascidos vivos [2022]'] != 0]


def analisar_regiao(df, regiao):
    print(df['Mortalidade infantil - óbitos por mil nascidos vivos [2022]'].describe())

    plt.figure(figsize=(13,4))
    plt.suptitle(f'Mortalidade infantil [2022] - {regiao}', fontsize=14, weight='bold', y=1.05)

    plt.subplot(1, 2, 1)
    sns.boxplot(x=df['Mortalidade infantil - óbitos por mil nascidos vivos [2022]'])
    plt.title('Boxplot')
    plt.xlabel('Mortalidade infantil [2022]')

    plt.subplot(1, 2, 2)
    sns.histplot(data=df, x='Mortalidade infantil - óbitos por mil nascidos vivos [2022]', kde=True)
    plt.title('Histograma e KDE')
    plt.xlabel('Mortalidade infantil [2022]')

    plt.tight_layout()
    plt.show()

# Chamada para cada região
analisar_regiao(df1, Borborema_df)
analisar_regiao(df2, AgresteParaibano_df)
analisar_regiao(df3, MataParaibana_df)
analisar_regiao(df4, SertãoParaibano_df)


from scipy.stats import shapiro

shapiro_test = shapiro(df["Mortalidade infantil - óbitos por mil nascidos vivos [2022]"])
print(f"p-valor do Shapiro-Wilk: {shapiro_test.pvalue}")


# Agrupar os dados por região e extrair os valores da variável
grupos = [grupo["Mortalidade infantil - óbitos por mil nascidos vivos [2022]"].
          values for _, grupo in df.groupby("região")]


# Aplicar o teste de Kruskal-Wallis
estatistica, p_valor = kruskal(*grupos)

print(f'Estatística de teste: {estatistica:.4f}')
print(f'Valor-p: {p_valor:.4f}')

# Interpretação
if p_valor < 0.05:
    print("Há evidências de diferença significativa entre as regiões.")
else:
    print("Não há evidências de diferença significativa entre as regiões.")

# Aplicar o teste de Dunn
resultado_posthoc = sp.posthoc_dunn(
    df,
    val_col="Mortalidade infantil - óbitos por mil nascidos vivos [2022]",
    group_col="região",
    p_adjust="bonferroni"
)

print("Matriz de p-valores (teste de Dunn com correção de Bonferroni):")
print(resultado_posthoc)


# Criar o boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="região",
    y="Mortalidade infantil - óbitos por mil nascidos vivos [2022]",
    hue="região",
    palette="Set3",
    legend=False
)

# Títulos e rótulos
plt.title("Distribuição da Mortalidade Infantil por Região ", fontsize=14)
plt.xlabel("Região", fontsize=12)
plt.ylabel("Mortalidade Infantil\n(óbitos por mil nascidos vivos em 2022)", fontsize=12)

# Mostrar o gráfico
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
