# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 18:59:32 2024

@author: Andreia Chamas
"""

#%%
import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt
#%%
print("Diretório de trabalho atual:", os.getcwd())
#%%
cult = pd.read_excel(r'C:\Users\Andreia Chamas\Documents\AC_PAD\dados_lei_x_UF.xlsx',header=7)
#%%
cult.info()
#%%
cult.isnull().sum()
#%%
cult.dropna(inplace = True)
#%% transformando as linhas em indice
cult.set_index(cult.columns[0], inplace=True)
cult.info()
#%%
del cult['Subsídio mensal para manutenção de espaços artísticos, culturais etc. (inciso 2 da Lei)']
del cult['Editais (inciso 3 da Lei)']
del cult['Chamadas públicas (inciso 3 da Lei)']
del cult['Prêmios (inciso 3 da Lei)']
del cult['Aquisição de bens e serviços']
del cult['Outros instrumentos (inciso 3 da Lei)']
del cult['Menos de 50%']
del cult['Entre 50% e 90%']
del cult['Entre 90% e 100%']
del cult['Não sabe informar']
del cult['No seu website']
del cult['Por e-mail']
del cult['Nas redes sociais']
del cult['Por aplicativos de mensagens (Whatsapp, Telegram, Signal, etc.)']
del cult['Por rádio']
del cult['Por carro de som ou porta a porta']
del cult['Por outro meio.1']
del cult['Por telefone de contato para informação sobre o auxílio']
del cult['Não divulgou porque não teve permissão da procuradoria municipal ou justiça eleitoral']
del cult['Não divulgou']
del cult['Pela internet']
del cult['Por telefone']
del cult['Pelo correio']
del cult['Presencial-mente']
del cult['Cadastro pré-existente municipal']
del cult['Cadastro pré-existente estadual']
del cult['Cadastro pré-existente federal']
del cult['Por outro meio']
del cult['Total']
del cult['Critérios sociais']
del cult['Unnamed: 2']
del cult['Unnamed: 33']
del cult['Unnamed: 34']
del cult['Unnamed: 35']
del cult['Unnamed: 36']
del cult['Unnamed: 37']
del cult['Unnamed: 38']
del cult['Unnamed: 39']
del cult['Unnamed: 40']

#%%
cult.info()

#%%
cult=cult.rename(columns={ 'Unnamed: 1':'Total_Lugar',
                            'Manifestação tradicional popular':'Tradicao',
                            'Dança':'Danca',
                            'Bloco carnavalesco':'Carnaval',
                            'Cultura_digital':'Cultura_digital',
                            'Escola de samba':'Escola_de_samba ',
                            'Associação literária':'Literatura',
                            'Artes visuais':'Artes_visuais',
                            'Nenhum grupo ou atividade':'Nenhum'})


print(cult.info())
#%% FAZENDO A MEDIA DE INVESTIMENTOS TOTAIS POR REGIAO
cult['Media'] = cult.mean(axis=1).round(1)
#%% CATEGORIZANDO OS INVESTIMENTOS
cult['Investimento']=''
cult.loc[(cult['Total_Lugar']<=70),'Investimento']="Baixo"
cult.loc[(cult['Total_Lugar']>70),'Investimento']="Mediano"
cult.loc[(cult['Total_Lugar']>200),'Investimento']="Alto"

#%%
cult.reset_index(inplace=True)
cult.rename(columns={'Unnamed: 0': 'UF'}, inplace=True)
#%%
cult.to_excel(r'C:\Users\Andreia Chamas\Documents\AC_PAD\base_adaptada.xlsx', index=False)
#%%
 '''                                     TRATAMENTO DE ESCOLARIDADE
 '''
#%%
edu =  pd.read_excel(r'C:\Users\Andreia Chamas\Documents\AC_PAD\base_estudo.xlsx',header=4)
#%%
edu.info()
#%%
edu.isnull().sum()
#%%
edu.dropna(inplace = True)
#%%
#edu.set_index(edu.columns[0], inplace=True)
edu.info()
#%%
del edu['VL_APROVACAO_2023_4']
del edu['VL_APROVACAO_2023_2']
del edu['VL_APROVACAO_2023_3']
del edu['VL_APROVACAO_2023_1']
del edu['VL_OBSERVADO_2023']
del edu['VL_NOTA_PORTUGUES_2023']
del edu['VL_NOTA_MATEMATICA_2023']
del edu['VL_INDICADOR_REND_2021']
#%%
edu=edu.rename(columns={ 'Unnamed: 1':'Escola',
                        'Unnamed: 0':'UF',
                        'VL_NOTA_MEDIA_2023':'Nota_Media',
                        'VL_PROJECAO_2021':'Projecao_Notas',
                        'VL_APROVACAO_2023_SI_4':'Indice_Aprovacao'})
#%%
edu.loc[(edu['Escola']=='Total (3)(4)'),'Escola']='Total'
edu.loc[(edu['Escola']=='Total (4)'),'Escola']='Total'
edu.loc[(edu['Escola']=='Privada (2)'),'Escola']='Privada'
#%%
edu['Escola'] = edu['Escola'].astype(str)
edu.info()
#%% NIVEL DE DESEMPENHO
edu['Desempenho']=''
edu.loc[(edu['Indice_Aprovacao']<=85),'Desempenho']="Baixo"
edu.loc[(edu['Indice_Aprovacao']>85),'Desempenho']="Médio"
edu.loc[(edu['Indice_Aprovacao']>95),'Desempenho']="Alto"

#%%
edu['Diferenca'] = edu['Projecao_Notas'] - edu['Nota_Media']
#%%
cult.to_excel(r'C:\Users\Andreia Chamas\Documents\AC_PAD\base_adaptada2.xlsx', index=False)
#%%
 '''                                     INICIO DAS ANALISES 
 '''
#%% INDICE DE APROVAÇAO X NOTA
plt.figure(figsize=(10, 6))
plt.scatter(edu['Indice_Aprovacao'], edu['Nota_Media'], alpha=0.5)
plt.title('Dispersão: Índice de Aprovação vs Nota Média')
plt.xlabel('Índice de Aprovação')
plt.ylabel('Nota Média')
plt.grid(True)
plt.show()
#%% TP DE ESCOLA
escola_counts = edu['Escola'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(escola_counts, labels=escola_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Distribuição de Tipos de Escola')
plt.show()
#%% fununcia meio bosta
plt.figure(figsize=(12, 6))
edu_sorted = edu.sort_values('Diferenca')
plt.bar(edu_sorted['Escola'], edu_sorted['Diferenca'], color='skyblue')
plt.xticks(rotation=360)
plt.title('Diferença entre Nota Média e Nota Projetada por Tipo de Escola')
plt.xlabel('Escola')
plt.ylabel('Diferença Nota Média - Projeção')
plt.show()

#%%
cult.boxplot(column='Media', by='Investimento', 
             figsize=(10, 6), 
             patch_artist=True, 
             showfliers=False)
plt.title('Distribuição da Média por Categoria de Investimento')
plt.suptitle('')  
plt.xlabel('Investimento')
plt.ylabel('Média')
plt.show()

#%%
cult.set_index('UF', inplace=True)

cult[['Teatro', 'Tradicao', 'Danca', 'Musical']].plot(kind='bar', 
                                                      stacked=True, 
                                                      figsize=(10, 6), 
                                                      color=['blue', 'green', 'red', 'purple'],
                                                      title='Atividades Culturais por UF')
plt.xlabel('UF')
plt.ylabel('Quantidade de Atividades')
plt.xticks(rotation=90)  
plt.show()
#%%
cult['Total_Lugar'].plot(kind='bar', color='purple', alpha=0.7, 
                         title='Distribuição de Total de Lugares Culturais por UF')
plt.xlabel('UF')
plt.ylabel('Total de Lugares')
plt.xticks(rotation=90)  
plt.show()
#%% Perfeita
total_investimentos = cult[['Teatro', 'Tradicao', 'Danca', 'Musical', 'Artes_visuais','Moda','Gastronomia','Design',
                            'Literatura', 'Capoeira', 'Cineclube','Circo','Carnaval','Artesanato','Cultura digital', 'Escola_de_samba ']].sum()

total_investimentos.plot(kind='bar', figsize=(10, 6), color='orange', 
                         title='Total Investido em Atividades Culturais')
plt.xlabel('Atividade Cultural')
plt.ylabel('Total Investido')
plt.xticks(rotation=45)
plt.show()
#%%
edu.set_index('UF', inplace=True)

notas_total = edu[edu['Escola'] == 'Total']['Nota_Media']

notas_total.plot(kind='bar', color='skyblue', figsize=(10, 6))

plt.title('Diferença das Notas Médias (Total) por Estado')
plt.xlabel('UF')
plt.ylabel('Nota Média')
plt.xticks(rotation=90)  
plt.show()

#%%
notas_privada = edu[edu['Escola'] == 'Privada']['Nota_Media']
notas_estadual = edu[edu['Escola'] == 'Estadual']['Nota_Media']

comparativo_notas = pd.DataFrame({
    'Privada': notas_privada,
    'Estadual': notas_estadual
})

comparativo_notas.plot(kind='bar', figsize=(12, 6), color=['blue', 'red'], alpha=0.7)


plt.title('Média das Notas por Tipo de Escola (Privada vs Estadual) em Cada Estado')
plt.xlabel('UF')
plt.ylabel('Nota Média')
plt.xticks(rotation=90)  # Para exibir os nomes das UF verticalmente
plt.legend(title='Tipo de Escola')
plt.show()

#%%