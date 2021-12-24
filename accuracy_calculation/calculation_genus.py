import pandas as pd
import numpy as np 

# Opening files needed 
checkm = pd.read_csv('checkm_report.tsv', sep='\t')
checkm['sample'] = checkm['sample'].replace({'L':''}, regex=True)
#replace kraken and bracken with variable input csv file for genus 
kraken =  pd.read_csv('kraken_genus.csv')
bracken = pd.read_csv('bracken_genus.csv')
phenotype = pd.read_csv('phenotype.csv')
#print(bracken)

# Merging phenotype Ramon and Checkm output in which samples are omitted which showed 
# no phenotypic result and which displayed mismatched genus name
phenotype['monsternr'] = phenotype['monsternr'].astype(str)
merged_phenotype = phenotype.merge(checkm, left_on='monsternr', right_on='sample')
print(merged_phenotype)
df_phenotype = merged_phenotype.dropna(subset=['Genus'])
df_phenotype = df_phenotype.drop(['Species', 'sample', 'strain_heterogeneity'], axis=1)
#print(df_phenotype)

# Merging checkm results and kraken report 
merged_dataframe = kraken.merge(df_phenotype, left_on='Sample name', right_on='monsternr')
merged_dataframe = merged_dataframe.drop(['Sample name', 'Scientific name'], axis=1)
merged_dataframe = merged_dataframe[['monsternr', 'Genus', 'genus', 
        'completeness', 'contamination', 'Covered reads %']]
dict = {'monsternr': 'Sample_number', 'Genus': 'Genus_phenotype', 'genus' : 'Genus_checkm', 
        'Covered reads %' : 'Completeness_kreport', 'completeness': 'Completeness_checkm',
        'contamination': 'Contamination_checkm'}
merged_dataframe.rename(columns=dict, inplace=True)

# Calculation for contamination in kreport
contamination_percentage_kreport = []
for value in merged_dataframe.iloc[:, 5]:
    contamination_kreport = (100.00-value)
    contamination_percentage_kreport.append(contamination_kreport)
merged_dataframe['Contamination_kreport'] = contamination_percentage_kreport

# Calculation accuracy 
merged_dataframe['False positive'] = merged_dataframe['Completeness_checkm'] - merged_dataframe['Completeness_kreport']
merged_dataframe['False negative'] = merged_dataframe['Completeness_kreport'] - merged_dataframe['Completeness_checkm']
num = merged_dataframe._get_numeric_data()
num[num < 0] = 0
merged_dataframe['True positive'] = merged_dataframe [['Completeness_checkm', 'Completeness_kreport']].min(axis=1)
merged_dataframe['True negative'] = merged_dataframe [['Contamination_checkm', 'Contamination_kreport']].min(axis=1)
#print(merged_dataframe)
