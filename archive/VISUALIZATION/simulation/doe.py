import pandas as pd
from components.params import MetaParams, Params
import sqlite3

import importlib

# import subprocess
# bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()

def doe(experiment_name, params_tested, params_const, meta_params, func_file):
    
    # import market as tosim
    tosim = importlib.import_module(func_file)
    
    db = sqlite3.connect("%s.sqlite"%experiment_name)
    cursor = db.cursor()
    
    experiment_data = pd.DataFrame(columns=meta_params.params_const + meta_params.params_tested + meta_params.results_primary + ['results_full'])
    
    params = list()
    for i in range(len(params_tested)):
        params_all = params_const
        params_tested_dict = params_tested.iloc[i].to_dict()
        
        for param in params_tested_dict.keys():
            params_all[param] = params_tested_dict[param]
        
        # print('PARAMS ALL', params_all)
        
        run_id = i
        print("\n\n============= Run %s =============\n\n"%run_id)
        params = Params(params_all)
        
        # write results primary to sqlite database
        results_full, results_primary = tosim.sim(params, meta_params)
        
        # print("\n\n============= Results Full =============\n\n", results_full)
        
        for result in meta_params.results_primary:
            experiment_data.at[i, result] = results_primary[result]
        
        for param in meta_params.params_tested:
            experiment_data.at[i, param] = params_tested.iloc[i][param]
            
        for param_const in meta_params.params_const:
            experiment_data.at[i, param_const] = params_const[param_const]
        
        results_full.to_csv('Run%s_data.csv'%run_id)
        # print(results_full.dtypes)
        
        # results_full_str = pd.DataFrame(results_full.to_dict())
        # results_full_str = pd.DataFrame()
        # results_full_str = results_full.copy()
        # for col in list(results_full.columns.values):
        #     # if type(results_full[param]) != int or str:
        #     #     results_full_str[param] = results_full[param].astype(str)
        #     # else:
        #     #     results_full_str[param] = results_full[param]
        #     results_full_str[col] = results_full[col].astype(str) if type(results_full[col]) != int or str else results_full[col]
        # # print(results_full_str)
        # # print(results_full_str.dtypes)
        
        results_full.to_sql('run_data', con=db, if_exists='replace')
        
        cursor.execute("""DROP TABLE IF EXISTS run%s_data"""%run_id)
        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS run%s_data as 
        select * from run_data
        """%run_id)
        # cursor.execute("SELECT * FROM run%s_data"%run_id).fetchall()
        
        # return experiment_data
    
    # print("\n\n============= Experiment Data =============\n\n", experiment_data)
    
    # experiment_data_str = pd.DataFrame()
    experiment_data_str = experiment_data.copy()
    for col in list(experiment_data.columns.values):
        # if type(results_full[param]) != int or str:
        #     results_full_str[param] = results_full[param].astype(str)
        # else:
        #     results_full_str[param] = results_full[param]
        experiment_data_str[col] = experiment_data[col].astype(str) if type(experiment_data[col]) != int or str else experiment_data[col]
    print(experiment_data_str)
    print(experiment_data_str.dtypes)
        
    print("\n\n\nERROR\n\n\n", experiment_data)
    experiment_data.to_csv('%s.csv'%experiment_name) 
    experiment_data_str.to_sql('experiment_data', con=db, if_exists='replace')

    cursor.execute("""DROP TABLE IF EXISTS %s_data"""%experiment_name)
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS %s_data as 
    select * from experiment_data
    """%experiment_name)
    
    
    print("\n\n================= ULTIMATE TEST ================\n\n")
    
    print(cursor.execute("SELECT * FROM %s_data"%experiment_name).fetchall())
    
    
    # cleanup
    cursor.execute("""DROP TABLE IF EXISTS experiment_data""")
    cursor.execute("""DROP TABLE IF EXISTS new_data""")
