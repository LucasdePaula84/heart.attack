#!/usr/bin/env python
# coding: utf-8

# # Sobre esse conjunto de dados
# 
# <br>
# Age: Idade do paciente<br>
# <br>
# Sex: Sexo do paciente<br>
# <br>
# exang: angina induzida por exercício (1 = sim; 0 = não)<br>
# <br>
# ca: número de embarcações principais (0-3)<br>
# <br>
# cp: Tipo de dor no peito Tipo de dor no peito<br>
# Valor 1: angina típica<br>
# Valor 2: angina atípica<br>
# Valor 3: dor não anginosa<br>
# Valor 4: assintomático<br>
# <br>
# trtbps: pressão arterial em repouso (em mm Hg)<br>
# <br>
# chol: colesterol em mg/dl obtido via sensor de IMC<br>
# <br>
# fbs: (glicemia em jejum > 120 mg/dl) (1 = verdadeiro; 0 = falso)<br>
# <br>
# rest_ecg: resultados eletrocardiográficos em repouso<br>
# Valor 0: normal<br>
# Valor 1: com anormalidade da onda ST-T (inversões da onda T e/ou elevação ou depressão do segmento ST de > 0,05 mV)<br>
# Valor 2: mostrando hipertrofia ventricular esquerda provável ou definitiva pelos critérios de Estes<br>
# <br>
# thalach: frequência cardíaca máxima alcançada.<br>
# <br>
# alvo: 0= menos chance de ataque cardíaco 1= mais chance de ataque cardíaco.

# In[37]:


# Bibliotecas Utilizadas

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[38]:


# Importando dados

df = pd.read_csv('Downloads/heart.csv')
df.head()


# In[39]:


# Substituindo os valores

df['sex'] = df['sex'].replace({0: 'masculino', 1: 'feminino'})
df['exng'] = df['exng'].replace({1: 'sim', 0: 'nao'})
df['cp'] = df['cp'].replace({0: 'angina típica', 1: 'angina atípica', 2: 'dor não anginosa',3: 'assintomático'})
df['fbs'] = df['fbs'].replace({1: 'alta', 0: 'baixa'})
df['restecg'] = df['restecg'].replace({0: 'normal', 1: 'com anormalidade da onda ST-T '})
df.head(10)


# In[40]:


# Verificar os tipos de dados

df.dtypes


# In[41]:


# Verificar por linhas em brancos e valores nulo.

df.isnull().sum()


# In[42]:


#Verificar informacoes da tabela

df.info()


# In[43]:


#Verificar dados estatisticos basicos

df.describe()


# # Iniciando analise univariadas

# In[44]:


# Frequencia de ataque cardiaco por idade.

plt.hist(df['age'], bins=30, edgecolor='black')  # 'bins' define o número de intervalos
plt.title('Frequencia de ataque cardiaco por idade')  # Título do gráfico
plt.xlabel('Idade')  # Rótulo do eixo X
plt.ylabel('Frequência')  # Rótulo do eixo Y
plt.show()  # Exibe o gráfico


# In[45]:


# Frequencia de ataque cardiaco por sexo.

# Contando a frequencia de cada sexo
sex_counts = df['sex'].value_counts()
print(sex_counts)


# In[46]:


# Criando o grafico de Pizza.

plt.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=['pink', 'lightblue'])
plt.title('Frequência de ataque cardíaco por sexo')  # Título do gráfico
plt.axis('equal')  # Para garantir que o gráfico seja um círculo
plt.show()  # Exibe o gráfico


# In[47]:


# Colesterol medio por sexo, e faixa etaria.

# Definindo faixas etárias
bins = [30, 40, 50, 60, 70]  # Faixas: 30-40, 40-50, etc.
labels = ['30-40', '40-50', '50-60', '60-70']
df['faixa_etaria'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

# Calculando o colesterol médio por sexo e faixa etária
resultado = df.groupby(['sex', 'faixa_etaria'])['chol'].mean().reset_index()

# Exibindo o resultado
print(resultado)


# In[48]:


# Matriz de correlação, focando em variáveis como colesterol, idade, sexo e outros fatores.

# Converta 'sex' para numérico para facilitar a análise (masculino = 0, feminino = 1)
df['sex_num'] = df['sex'].apply(lambda x: 1 if x == 'feminino' else 0)

# Calcular a matriz de correlação
correlation = df[['age', 'chol', 'sex_num']].corr()

# Plotar a matriz de correlação
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlação (Idade, Colesterol e Sexo)')
plt.show()


# ### Resultados principais:
# Idade e colesterol (age vs. chol): Correlação de 0.21, indicando uma relação positiva, mas fraca. Ou seja, à medida que a idade aumenta, os níveis de colesterol tendem a subir ligeiramente.<br>
# <br>
# Idade e sexo (age vs. sex_num): Correlação de -0.10, muito fraca e negativa. Isso sugere que a idade não influencia significativamente a variável sexo.<br>
# <br>
# Colesterol e sexo (chol vs. sex_num): Correlação de -0.20, fraca e negativa. Mostra que o colesterol tende a ser um pouco mais alto em homens (sex_num = 0) em comparação às mulheres (sex_num = 1).<br>
#     
#    

# In[49]:


# Relação entre idade e colesterol, diferenciando por sexo

# Scatterplot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='age', y='chol', hue='sex', style='sex', palette='Set2', s=100)
plt.title('Relação entre Idade e Colesterol por Sexo')
plt.xlabel('Idade')
plt.ylabel('Colesterol')
plt.legend(title='Sexo')
plt.show()


# ### Relação idade e colesterol:
# Observa-se que, em geral, os níveis de colesterol aumentam com a idade. Apesar de não haver uma correlação forte, a presença de outliers em idades mais avançadas (especialmente em homens) sugere maior variabilidade nos níveis de colesterol em pessoas mais velhas.<br>
# Há uma variação significativa nos níveis de colesterol entre os sexos, com homens mostrando maior dispersão e tendência a valores mais altos.<br>
# A idade tem um impacto leve no colesterol, mas a variabilidade dentro de cada faixa etária indica que outros fatores (como estilo de vida ou condições de saúde) podem estar influenciando os resultados.

# In[50]:


# Distribuição do colesterol

# Histograma
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='chol', hue='sex', kde=True, palette='Set2', bins=10)
plt.title('Distribuição do Colesterol por Sexo')
plt.xlabel('Colesterol')
plt.ylabel('Frequência')
plt.show()


# ### Conclusão
# 
# As mulheres tendem a ter níveis de colesterol mais estáveis e concentrados, enquanto os homens apresentam maior variabilidade e maior probabilidade de ter colesterol elevado.<br>
# Preocupação clínica:<br>
# Indivíduos com colesterol acima de 300 mg/dL merecem atenção especial, sendo essa condição mais prevalente nos homens do conjunto de dados.

# In[52]:


# Colesterol por tipo de dor no peito (cp)

# Boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='cp', y='chol', palette='Set3')
plt.title('Níveis de Colesterol por Tipo de Dor no Peito')
plt.xlabel('Tipo de Dor no Peito')
plt.ylabel('Colesterol')
plt.show()


# ### Resultado
# <br>
# Assintomático
# Níveis de colesterol: Apresentam uma distribuição mais concentrada em torno da mediana, sugerindo uma menor variabilidade nos níveis de colesterol em comparação aos outros grupos.
# Valores atípicos: A presença de alguns valores atípicos indica que, mesmo em indivíduos assintomáticos, podem existir níveis elevados de colesterol.
# Interpretação: A ausência de sintomas não garante níveis de colesterol saudáveis. É fundamental realizar exames regulares, mesmo na ausência de queixas.<br>
# <br>
# Dor não anginosa
# Níveis de colesterol: A distribuição dos níveis de colesterol é similar ao grupo assintomático, com uma leve tendência para valores mais elevados.
# Valores atípicos: A presença de valores atípicos sugere que a dor não anginosa pode estar associada a variações significativas nos níveis de colesterol.
# Interpretação: A dor não anginosa pode ser um sinal de alerta para a presença de dislipidemia (alteração nos níveis de lipídios no sangue), incluindo o colesterol.<br>
# <br>
# Angina atípica
# Níveis de colesterol: Os níveis de colesterol apresentam uma maior dispersão em comparação aos grupos anteriores, com uma leve tendência para valores mais elevados.
# Valores atípicos: A presença de valores atípicos é mais evidente neste grupo, indicando uma maior heterogeneidade nos níveis de colesterol.
# Interpretação: A angina atípica, caracterizada por sintomas menos típicos de angina, pode estar associada a uma maior variabilidade nos níveis de colesterol.<br>
# <br>
# Angina típica
# Níveis de colesterol: Este grupo apresenta os níveis de colesterol mais elevados e com maior dispersão.
# Valores atípicos: A presença de vários valores atípicos indica que a angina típica pode estar associada a níveis de colesterol significativamente elevados em alguns indivíduos.
# Interpretação: A angina típica é classicamente associada à doença arterial coronariana, que está intimamente ligada ao acúmulo de placas de gordura nas artérias, frequentemente causadas pelo excesso de colesterol.

# In[ ]:




