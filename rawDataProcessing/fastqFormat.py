################################################################################
# Nathaniel Jennings
# fasqFormat.py
################################################################################
'''
Takes raw data of sequences listed in the fastq format and turns it into a
pandas array of length |sequences| and three columns [identity,sequence,scores]
'''
import pandas as pd

# Takes data from path in fastq and converts to list of lines
def dataToLines(path):
    f = open(path,"r")
    lines = f.read().splitlines()
    return lines

# Takes lines and converts to three lists > pandas columns
def parseLines(lines):
    data = []
    for item in range(len(lines)):
        # parse fastq format
        if item % 4 == 0:
            data.append([lines[item]])
        elif item % 4 == 2:
            continue
        else:
            data[-1].append(lines[item])
    columns = ['Identities','Sequences','Scores']
    df = pd.DataFrame(data=data,columns=columns)
    return df

# Saves a dataframe to a pickle format
def saveDataFrame(df,path):
    df.to_pickle(path)
    return

# Loads a dataframe from pickle format
def loadDataFrame(path):
    df = pd.read_pickle(path)
    return df
    

def main():
    processPath = r'C:\Users\illum\Documents\GitHub\GreatIdeasCBProject\raw data\ena_files\ERR475467'
    name = f'/ERR475467_1.fastq'
    lines = dataToLines(processPath+name)
    df = parseLines(lines)
    savePath = r'C:\Users\illum\Documents\GitHub\GreatIdeasCBProject\processed data'
    saveDataFrame(df,savePath+name[:-6]+'.pickle')
    df = loadDataFrame(savePath+name[:-6]+'.pickle')
    print(df['Sequences'])
    
if __name__ == '__main__':
    main()
