mport pandas as pd
import numpy as np 

# Opening files needed 
checkm = pd.read_csv('checkm_report.tsv', sep='\t')
checkm['sample'] = checkm['sample'].replace({'L':''}, regex=True)
#replace kraken and bracken with variable input csv file for genus 
kraken =  pd.read_csv('kraken_species.csv')
bracken = pd.read_csv('bracken_species.csv'
phenotype = pd.read_csv('phenotype.csv')

phenotype['monsternr'] = phenotype['monsternr'].astype(str)
merged_phenotype = phenotype.merge(checkm, left_on='monsternr', right_on='sample')
print(merged_phenotype)
df_phenotype = merged_phenotype.dropna(subset=['])
df_phenotype = df_phenotype.drop(['Species', 'sample', 'strain_heterogeneity'], axis=1)