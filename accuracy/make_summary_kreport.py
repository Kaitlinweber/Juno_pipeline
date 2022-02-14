import argparse
import pathlib
import pandas as pd 


def get_sample_name(file_path):
    '''Extracts sample name (stem of file name) from the file path.
    '''
    file_path = pathlib.Path(file_path)
    sample_ID = str(file_path.stem)
    return sample_ID

def get_multiple_sample_names(list_kraken_files):
    '''Makes list of kreport names
    '''
    sample_names = []
    for file_path in list_kraken_files:
        sample_ID = get_sample_name(file_path)
        sample_names.append(sample_ID)
    return sample_names

def read_kreport(list_of_kreports):
    ''' Reads every kreport on the given list and extracts the read coverage percentage,
    the taxonomic rank and the scientific name above a certain read coverage percentage, 
    also adds the sample name. 
    '''
    kreport_result_list =[]
    for file_ in list_of_kreports:
        kreport= pd.read_csv(file_, sep='\t', 
                    names=['Covered reads %', '0', '1', 'Rank', '2', 'Scientific name'])
        threshold_hit = 30    #  the 30 needs to be edited based on the graph for percentage coverage read
        array =['G', 'S'] 
        kreport_result = kreport.loc[(kreport['Covered reads %'] >= threshold_hit) & kreport['Rank'].isin(array)]
        kreport_result = kreport_result.loc[:,['Covered reads %', 'Rank', 'Scientific name']] 
        number_of_rows = int(kreport_result.shape[0])
        sample_name = get_sample_name(file_path=file_)
        kreport_result['Sample name'] = [sample_name] * number_of_rows
        columns_kreport = ['Sample name', 'Covered reads %', 'Rank', 'Scientific name']
        kreport_result = kreport_result.reindex(columns=columns_kreport)
        kreport_result_list.append(kreport_result)
        kreport_result = pd.concat(kreport_result_list)
    return kreport_result

 
if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('path', type=pathlib.Path, 
                        default=[], nargs='+', help='List of Kraken results files (<sample>.kreport2 files).')
    args = argument_parser.parse_args()
    summary_file = read_kreport(list_of_kreports=args.path)
    summary_file.to_csv('summary_file_kreport_raw_reads.csv', index=False)