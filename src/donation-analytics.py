#!/usr/bin/python

import pandas as pd
import numpy as np

def find_repeat_donor_zipcodes(input_donor_data, percentile_value, output_donor_data):

    donor_dataframe = pd.read_csv(input_donor_data, sep='|', header=None, usecols=[0, 7, 10, 13, 14, 15], names=['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID'], dtype={'TRANSACTION_AMT':np.float, 'ZIP_CODE':np.str}).dropna(subset = ['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT']) #Reads in file, specifies '|' as separator, notes that there is no header in the input file, seleects only the 6 columns that are relevant to my analysis, provides header names for each column for greater ease of working with data, converts the 'TRANSACTION_AMT' column to a float to allow for all possible dollar amounts, drops null values from a subset of columns, but not the 'OTHER_ID' column where we want to keep all null values
    
    
    donor_dataframe = donor_dataframe[pd.isnull(donor_dataframe['OTHER_ID'])] # Keeps all rows where 'OTHER_ID' is a null value, removes all rows where 'OTHER_ID' is not a null value
    
    
    donor_dataframe['ZIP_CODE'] = donor_dataframe.ZIP_CODE.str[0:5] #All values in ZIP_CODE column that are longer than 5 characters are converted to 5 characters
    donor_dataframe = donor_dataframe[~(donor_dataframe.ZIP_CODE.str.len() != 5)] #After reducing all 'ZIP_CODE' values that are longer than 5 down to 5 or less values, this line eliminates any remaining rows where the 'ZIP_CODE' column is less than length 5.
    donor_dataframe = donor_dataframe[pd.to_numeric(donor_dataframe['ZIP_CODE'], errors='coerce').notnull()] #After identifying only rows where ZIP_CODE is 5 characters long, this line eliminates rows with non-numeric values in the 'ZIP_CODE' column
            
    
    donor_dataframe['TRANSACTION_DT'] = pd.to_datetime(donor_dataframe['TRANSACTION_DT'], format='%m%d%Y') #Transforms 'TRANSACTION_DT' into a datetime column
    donor_dataframe['YEAR'] = donor_dataframe['TRANSACTION_DT'].dt.year #From 'TRANSACTION_DT' as a datetime column, this line creates a new column 'YEAR' containing just the year of the transaction
    donor_dataframe = donor_dataframe[~(donor_dataframe.TRANSACTION_AMT <= 0)] #Eliminates any values for 'TRANSACTION_AMT' that are zero or negative values, because those can't be valid contribution amounts
    
    
    donor_dataframe['COUNTER_BY_DONOR_NAME'] = donor_dataframe.groupby(['ZIP_CODE', 'NAME', 'YEAR']).cumcount() #Creates a column 'COUNTER_BY_DONOR_NAME' that indicates a running count of the number donations from a given donor in a given year. This is needed to identify which donors are repeat donors.
    donor_dataframe = donor_dataframe[donor_dataframe.duplicated(['NAME', 'ZIP_CODE']) | donor_dataframe.duplicated(['NAME', 'ZIP_CODE'])] #Eliminates rows for any one-time, non-repeating donors
    
    
    percentile_integer = int(open(percentile_value, 'r').read())/100
    
    donor_dataframe['RUNNING_PERCENTILE'] = donor_dataframe.groupby(['CMTE_ID', 'ZIP_CODE', 'YEAR'])['TRANSACTION_AMT'].cumsum().quantile(percentile_integer)
    donor_dataframe['RUNNING_PERCENTILE'] = donor_dataframe['RUNNING_PERCENTILE'].round(0) #Rounds the 'RUNNING_PERCENTILE' values to the nearest who number
    donor_dataframe['RUNNING_PERCENTILE'] = pd.to_numeric(donor_dataframe['RUNNING_PERCENTILE'], downcast='integer') #Converts the 'RUNNING_PERCENTILE' values to integers
    
    
    donor_dataframe['RUNNING_CONTR_SUM'] = pd.to_numeric(donor_dataframe.groupby(['CMTE_ID', 'ZIP_CODE', 'YEAR'])['TRANSACTION_AMT'].cumsum(), downcast='integer') #Creates a column with a running sum total of all of the donations made from a particular 'ZIP_CODE' during a particular 'YEAR' and received by a recipient of a unique 'CMTE_ID'. Also converts the 'RUNNING_CONTR_SUM' column to an integer.
    
    
    donor_dataframe['COUNTER_BY_CMTE_ID'] = donor_dataframe.groupby(['CMTE_ID', 'ZIP_CODE', 'YEAR']).cumcount() + 1 #Creates a column 'COUNTER_BY_CMTE_ID' that indicates a running count of the number donations to a given recipient in a given year
    
    
    donor_dataframe = donor_dataframe.drop(labels=['NAME', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID', 'COUNTER_BY_DONOR_NAME'], axis=1)
    
    
    donor_dataframe.to_csv(output_donor_data, sep='|', header=False, index=False) #Writes dataframe to csv file 'repeat_donors.txt' with the correct '|' separator. Also, to match the desired format, this line removes the headers and the index column.
