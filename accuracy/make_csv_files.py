import pandas as pd 

summary_file_kreport = pd.read_csv('summary_file_kreport.csv')

kraken_result = summary_file_kreport[~summary_file_kreport['Sample name'].str.contains('_bracken_species')]
print(kraken_result)
kraken_genus = kraken_result[kraken_result['Rank'].str.contains('G')]
kraken_genus.drop('Rank', inplace=True, axis=1)
kraken_genus.to_csv('fasta_kraken_genus.csv', index=False)


kraken_species = kraken_result[kraken_result['Rank'].str.contains('S')]
print(kraken_species)
kraken_species.drop('Rank', inplace=True, axis=1)
kraken_species.to_csv('fasta_kraken_species.csv', index=False)
print(kraken_species)

bracken_result = summary_file_kreport[summary_file_kreport['Sample name'].str.contains('_bracken_species')]
bracken_result['Sample name'] = bracken_result['Sample name'].replace({'_bracken_species':''}, regex=True)
bracken_genus = bracken_result[bracken_result['Rank'].str.contains('G')]
bracken_genus.drop('Rank', inplace=True, axis=1)


bracken_species = bracken_result[bracken_result['Rank'].str.contains('S')]
bracken_species.drop('Rank', inplace=True, axis=1)
bracken_species.to_csv('fasta_bracken_species.csv', index=False)