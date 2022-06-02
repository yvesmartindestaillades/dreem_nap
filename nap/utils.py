import pandas as pd
import numpy as np
import datetime
from os.path import exists
import os


def make_path(path:str)->str:
    """Create directories until path exists on your computer. Turns the keyword 'date' into today's date.

    Args:
        path: series of directories that you want to create.
    
    Returns:
        Updated path with today's date instead of the keyword 'date'  
    """

    path = os.path.normpath(path)
    path=path.split(os.sep)
    try:
        path[path.index('date')] = str(datetime.datetime.now())[:10]
    except:
        'No date in path'
    full_path = ''
    for repo in path:
        full_path = full_path + f"{repo}/"
        if not exists(full_path):
            os.mkdir(full_path)
    return full_path


def get_construct_content(df:pd.DataFrame, column:str):   #TODO I don't know wwhat output    
    """Read columns values that are common to each constructs among the tubes - typically, from the RNAstructure output file. 
    
    Args:
        df: a Pandas dataframe.
        column: the dataframe's column values that you want to look at.
    Returns:
        #TODO
    """   

    return df.set_index('construct').sort_values(column)[column].groupby('construct').apply(lambda x:np.array(x)[0]).sort_values()


def get_roi_info(df, tube, construct):
    np.seterr(invalid='ignore')
    df_use = df.set_index(['tube','construct'])
    start, end = df_use['roi_start_index'].loc[(tube,construct)] , df_use['roi_end_index'].loc[(tube,construct)]     
    mut_per_base = pd.DataFrame({'mut_rate':pd.Series(np.array(df_use[f"mut_bases"].loc[tube, construct][1:])/np.array(df_use[f"info_bases"].loc[tube, construct][1:]), dtype=object),
                            'base':list(df_use['full_sequence'].loc[tube, construct]),
                            'paired': np.array([bool(x != '.') for x in list(df_use['full_structure'].loc[tube,construct])]),\
                            'roi_structure_comparison': pd.Series(list(df_use['roi_structure_comparison'].loc[tube,construct]), index=list(range(start, end)))\
                            ,'roi_deltaG':df_use['roi_deltaG'].loc[tube, construct]})\
                            .dropna()\
                            .reset_index()\
                            .set_index(['base', 'paired', 'roi_structure_comparison','index'])
    return mut_per_base


def columns_to_csv(df, tubes, columns, title, path):
    np.seterr(invalid='ignore')
    full_path = make_path(path)
    df_print = df[df.tube.isin(tubes)]
    df_print = df_print[columns] 
    np.set_printoptions(suppress=True)
    df_print['mut_rate'] = df_print.apply(lambda row: np.float32(np.array(row['mut_bases'])/np.array(row['info_bases'])), axis=1)
    df_print.to_csv(f"{full_path}/{title}.csv")

def deltaG_vs_construct_to_csv(df, title, path, tubes):
    full_path = make_path(path)
    df[df['tube']==tubes[0]][['construct','roi_deltaG','full_deltaG']].reset_index().drop(columns=['index']).to_csv(f"{full_path}/{title}")

def deltaG_vs_construct_to_csv(df, title, path, tubes):
    full_path = make_path(path)
    df[df['tube']==tubes[0]][['construct','roi_deltaG','full_deltaG']].reset_index().drop(columns=['index']).to_csv(f"{full_path}/{title}")
    

def rand_tube_construct(df, n_tubes=1, n_constructs=1):
    all_tubes, constructs = list(df.tube.unique()), list(df.construct.unique())
    these_tubes, these_constructs = np.array(all_tubes)[np.random.randint(0, len(all_tubes),n_tubes)] , np.array(constructs)[np.random.randint(0, len(constructs), n_constructs)]
    if n_tubes == 1:
        these_tubes = these_tubes[0]
    if n_constructs == 1:
        these_constructs = these_constructs[0]

    return these_tubes, these_constructs
