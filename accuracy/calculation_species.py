import pandas as pd
import numpy as np 

# Opening files needed 
checkm = pd.read_csv('summary_checkm.csv', sep='\t', index_col=False)
checkm['sample'] = checkm['sample'].replace({'L':''}, regex=True)

#replace kraken and bracken with variable input csv file for genus 
kraken =  pd.read_csv('fasta_kraken_species.csv')

#bracken = pd.read_csv('bracken_genus.csv')
phenotype = pd.read_csv('phenotype.csv')

# Merging phenotype Ramon and Checkm output in which samples are omitted which showed 
# no phenotypic result and which displayed mismatched genus name
phenotype['monsternr'] = phenotype['monsternr'].astype(str)
merged_phenotype = phenotype.merge(checkm, left_on='monsternr', right_on='sample')
print(merged_phenotype)
#df_phenotype = merged_phenotype.dropna(subset=['Species'])

df_phenotype = merged_phenotype.drop(['sample', 'strain_heterogeneity'], axis=1)
#print(df_phenotype)

merged_dataframe = kraken.merge(df_phenotype, left_on='Sample name', right_on='monsternr')
#print(merged_dataframe)
merged_dataframe = merged_dataframe.drop(['Sample name', 'Scientific name'], axis=1)
merged_dataframe = merged_dataframe[['monsternr', 'Genus', 'Species', 'genus', 'species',
        'completeness', 'contamination', 'Covered reads %']]
print(merged_dataframe)
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
#print(merged_dataframe)

# Calculation accuracy 
merged_dataframe['False positive'] = merged_dataframe['Completeness_checkm'] - merged_dataframe['Completeness_kreport']
merged_dataframe['False negative'] = merged_dataframe['Completeness_kreport'] - merged_dataframe['Completeness_checkm']
num = merged_dataframe._get_numeric_data()
num[num < 0] = 0
merged_dataframe['True positive'] = merged_dataframe[['Completeness_checkm', 'Completeness_kreport']].min(axis=1)
merged_dataframe['True negative'] = merged_dataframe[['Contamination_checkm', 'Contamination_kreport']].min(axis=1)
false_positive = merged_dataframe['False positive']
false_negative = merged_dataframe['False negative']
true_positive = merged_dataframe['True positive']
true_negative = merged_dataframe['True negative']
merged_dataframe['Precision'] = true_positive / (true_positive + false_positive)
merged_dataframe['Recall'] = true_positive / (true_positive + false_negative)
precision = merged_dataframe['Precision']
recall = merged_dataframe['Recall']
merged_dataframe['F1'] = (2 * precision * recall) / (precision + recall)
merged_dataframe['Accuracy'] = (true_positive + true_negative) / (true_positive + false_positive + true_negative + true_positive)
merged_dataframe['Specificity'] = true_negative / (true_negative + false_positive)
print(merged_dataframe)

merged_dataframe.to_csv('Sensitivity_kraken_species.csv', index=False)