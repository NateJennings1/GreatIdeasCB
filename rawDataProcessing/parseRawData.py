from fastqFormat import *
import os

def main():
    processPath = r'C:\Users\illum\Documents\GitHub\GreatIdeasCBProject\raw data\ena_files\ERR475467'
    for file in os.listdir(processPath):
        lines = dataToLines(processPath+f'/{file}')
        df = parseLines(lines)
        savePath = r'C:\Users\illum\Documents\GitHub\GreatIdeasCBProject\processed data'
        saveDataFrame(df,savePath+f'/{file[:-6]}'+'.pickle')
        
    
if __name__ == '__main__':
    main()