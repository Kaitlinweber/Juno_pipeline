import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#input from calculation accuracy
df_kraken_fastq = pd.read_csv('Sensitivity_kraken_fastq_genus.csv')
df_kraken = pd.read_csv('Sensitivity_kraken_genus.csv')
df_bracken_fastq = pd.read_csv('Sensitivity_bracken_fastq_genus.csv')
df_bracken = pd.read_csv('Sensitivity_bracken_genus.csv')

#df_kraken_fastq = pd.read_csv('Sensitivity_kraken_fastq_species.csv')
#df_kraken = pd.read_csv('Sensitivity_kraken_species.csv')
#df_bracken_fastq = pd.read_csv('Sensitivity_bracken_fastq_species.csv')
#df_bracken = pd.read_csv('Sensitivity_bracken_species.csv')


df_precision = pd.concat([df_kraken['Precision'], df_kraken_fastq['Precision'], df_bracken['Precision'], df_bracken_fastq['Precision']], axis=1, keys=['Kraken2 \n Unassembled reads', 'Kraken2 \n Assembled reads', 'Kraken2 + Bracken \n Unassembled reads', 'Kraken2 + Bracken \n Assembled reads'])
df_recall = pd.concat([df_kraken['Recall'],  df_kraken_fastq['Recall'], df_bracken['Recall'], df_bracken_fastq['Recall']], axis=1, keys=['Kraken2 \n Unassembled reads', 'Kraken2 \n Assembled reads', 'Kraken2 + Bracken \n Unassembled reads', 'Kraken2 + Bracken \n Assembled reads'])
df_f1 = pd.concat([df_kraken['F1'], df_kraken_fastq['F1'], df_bracken['F1'], df_bracken_fastq['F1']], axis=1, keys=['Kraken2 \n Unassembled reads', 'Kraken2 \n Assembled reads', 'Kraken2 + Bracken \n Unassembled reads', 'Kraken2 + Bracken \n Assembled reads'])
df_accuracy = pd.concat([df_kraken['Accuracy'], df_kraken_fastq['Accuracy'], df_bracken['Accuracy'], df_bracken_fastq['Accuracy']], axis=1, keys=['Kraken2 \n Unassembled reads', 'Kraken2 \n Assembled reads', 'Kraken2 + Bracken \n Unassembled reads', 'Kraken2 + Bracken \n Assembled reads'])
#df_specificity = pd.concat([df_kraken_fastq['Specificity'], df_kraken['Specificity'], df_bracken_fastq['Specificity'], df_bracken['Specificity']], axis=1, keys=['Kraken2 \n Assembled reads', 'Kraken2 \n Raw reads', 'Kraken2 + Bracken \n Assembled reads', 'Kraken2 + Bracken \n Raw reads'])


df_precision.boxplot(fontsize=17)
#recall = df_recall.boxplot(fontsize=17)
#df_f1.boxplot(fontsize=17)
#df_accuracy.boxplot(fontsize=17)
#df_specificity.boxplot()
plt.title('Precision value at genus level', fontsize=30)
plt.ylabel('Value', fontsize=20)
plt.xlabel('Used tool and input data', fontsize=20)
plt.gcf().set_size_inches(13,12)
plt.savefig('/data/BioGrid/weberk/precision_genus_2.png')







