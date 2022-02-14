import argparse
import pathlib
import pandas

def parse_checkM(input_checkm, output_checkm):
    checkm_dict = {}
    for input_file in input_checkm:
        dict_key = "_".join(str(input_file).split("/")[-1].split(".")[0].split("_")[1:]) #get sample name
        
        # add a letter to every sample name so that multiqc will see the name as a string
        dict_key = dict_key + "L"

        infile = open(input_file, "r")
        for line in infile:
            if "scaffolds " in line:
                genus = line.split()[1]
                species = line.split()[2]
                completeness = line.split()[-3]
                contamination = line.split()[-2]
                strain_heterogeneity = line.split()[-1]
                checkm_dict[dict_key] = [genus, species, completeness, contamination, strain_heterogeneity]
        infile.close()
    
    
    # write output to file used for multiQC input
    outfile = open(str(output_checkm),"w")

    # write headers to file
    outfile.write("sample\tgenus\tspecies\tcompleteness\tcontamination\tstrain_heterogeneity\n")
    
    # write CheckM stats to file
    for x, y in checkm_dict.items():
        outfile.write(x +"\t")
        for item in y:
            outfile.write(item + "\t")
        outfile.write("\n") 
    outfile.close()
    
if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('path', type=pathlib.Path, 
                        default=[], nargs='+')
    args = argument_parser.parse_args()
    parse_checkM(input_checkm=args.path, output_checkm='summary_checkm.csv')
    