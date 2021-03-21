# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:22:51 2020

@author: nowak
"""

#Step 1: Import packages and set the working directory
import os
import glob
import pandas as pd
#os.chdir("/mydir")

#Step 2: Use glob to match the pattern ‘csv’

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]




#Step 3: Combine all files in the list and export as CSV

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')