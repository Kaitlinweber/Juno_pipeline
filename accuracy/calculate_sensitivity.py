import pandas as pd
import argparse


def get_summary_file_kreport(summary_file):
    summary_file_kreport = pd.read_csv(summary_file)
    kraken_result = summary_file_kreport[~summary_file_kreport['Sample name'].str.contains('_bracken_species')]
    kraken_genus = kraken_result[kraken_result['Rank'].str.contains('G')]
    kraken_genus.drop('Rank', inplace=True, axis=1)
    kraken_genus.to_csv('kraken_genus.csv', index=False)

    kraken_species = kraken_result[kraken_result['Rank'].str.contains('S')]
    kraken_species.drop('Rank', inplace=True, axis=1)
    kraken_genus.to_csv('kraken_species.csv', index=False)

    bracken_result = summary_file_kreport[summary_file_kreport['Sample name'].str.contains('_bracken_species')]
    bracken_result['Sample name'] = bracken_result['Sample name'].replace({'_bracken_species':''}, regex=True)
    bracken_genus = bracken_result[bracken_result['Rank'].str.contains('G')]
    bracken_genus.drop('Rank', inplace=True, axis=1)
    bracken_genus.to_csv('bracken_genus.csv', index=False)

    bracken_species = bracken_result[bracken_result['Rank'].str.contains('S')]
    bracken_species.drop('Rank', inplace=True, axis=1)
    bracken_species.to_csv('bracken_species.csv', index=False)
    return kraken_genus, kraken_species, bracken_species, bracken_genus



if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('filename')
    args = argument_parser.parse_args()
    summary_file = get_summary_file_kreport(summary_file=args.filename)
