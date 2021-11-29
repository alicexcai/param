import sqlite3
import pandas as pd

# SETUP #

db = sqlite3.connect('project.sqlite')
cursor = db.cursor()

# Create a table to store project metadata
cursor.execute('''CREATE TABLE meta (
               name TEXT, 
               timeline TEXT, 
               params TEXT, 
               notes TEXT,
               important_table_links TEXT, )''')

# Create a table to store metadata about the experiments
cursor.execute('''CREATE TABLE project (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT, 
               timestamp TEXT, 
               notes TEXT,
               params_const TEXT,
               params_tested TEXT, 
               experiment_link TEXT, )''')

'''Autofill id column with 1, 2, 3, ...'''

db.commit()  # Commit changes to the database


# ON EXPERIMENT #

'''
Experiment called
Input: T/F Save data? -> name
Outputs: params_tested, results -> results_table
Input post-experiment: notes
Processing: auto-generate timestamp
'''

# Create a table to store metadata about the experiments
experiment_name = input('Experiment name: ')

# Use list comprehension to expand the list of the parameters tested
cursor.execute('''CREATE TABLE {} (
               params_const TEXT, 
               params_tested TEXT, 
               results_primary TEXT,
               full_results_link DATAFRAME )''', experiment_name)