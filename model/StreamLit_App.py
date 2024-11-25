import pandas as pd
import argparse
import pandas as pd
import argparse
#Arguments d linha d-comand
parser = argparse.ArgumentParser(description='Analise de Dados')
parser.add_argument('--file', type=str, help='Caminho para o arquivo de entrada')
parser.add_argument('--output', type=str, help='Caminho para o arquivo de saída')
args = parser.parse_args()
#Ler arqv CSV
tabela = pd.read_csv(args.file, delimiter=';', on_bad_lines='skip')
#Remov colunas indesejadas
colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível"]
colunas_existentes = [col for col in colunas_para_excluir if col in tabela.columns]
if colunas_existentes:
    tabela = tabela.drop(columns=colunas_existentes)
#Converter colunas p/n°
tabela['Km Rodados'] = pd.to_numeric(tabela['Km Rodados'], errors='coerce')
tabela['Litros'] = pd.to_numeric(tabela['Litros'].astype(str).str.replace(',', '').str[:-2], errors='coerce')
tabela['Vlr. Total'] = pd.to_numeric(tabela['Vlr. Total'].astype(str).str.replace(',', ''), errors='coerce')
tabela['Horim. Equip.'] = pd.to_numeric(tabela['Horim. Equip.'], errors='coerce')
#Calcular colunas adicionais
tabela['Km por Litro'] = tabela['Km Rodados'] / tabela['Litros']
tabela['Lucro'] = tabela['Km Rodados'] - tabela['Vlr. Total']
tabela['Horim por Litro'] = tabela['Horim. Equip.'] / tabela['Litros']
#Save results
tabela.to_csv(args.output, index=False)