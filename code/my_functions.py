import pandas as pd
import datetime
import numpy as np
import os

from scipy import stats
from tqdm import tqdm


def full_describe(dataframe,variables="all",variability=20,completeness=10):
    """
    Function to calculate exploratory statistics (univariate).

    :param dataframe: Dataset to use in DataFrame format
    :param variables: Variables to compute the univariate (EDA) analysis.
                      Posible values: "all",
                      input sequence (ie. "1:8"),
                      input list of numbers or list of variable's names (i.e. '1,4,9' or 'var1,var2,var3')
    :param variability: Minimum of accepted completeness per variable (value vetween 0 and 100)
    :param completeness: Minimum of accepted variability per variable (posible values: 0, 2, 10, 20, 50, 100)
    :return:
    """

    print("Describe process started, Time: "+ datetime.datetime.now().strftime("%H:%M:%S"))
    start1 = datetime.datetime.now()
    if variables == "all": #If you wish to analyze all the variables
        #Apply "describe" function and add  adicionar (concatenated) rows with Missing values
        resumen=pd.concat([dataframe.describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.isnull().sum().to_frame(name = 'missing').T],sort=False)
    elif ":" in variables: #If you wish to analyze the sequence of variables n1:n2
        #Apply "describe" function and add  adicionar (concatenated) rows with Missing values
        variables_serie=list(pd.to_numeric((variables).split(':')))
        variables_serie=list(pd.Series(range(variables_serie[0],variables_serie[1])))
        resumen=pd.concat([dataframe.iloc[:,variables_serie].describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.iloc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
    else:
        try: #If you wish to analyze variables of numericala array (positions)[n1,n2,n3,...]
            # Split variable by comma
            variables_serie=list(pd.to_numeric((variables).split(',')))
            #Apply "describe" function and add  adicionar (concatenated) rows with Missing values
            resumen=pd.concat([dataframe.iloc[:,variables_serie].describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.iloc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
        except: 
            if set(list(variables.split(","))).issubset(list(dataframe.columns)): #If you wish to analyze variables using array string (field names) ['nom1','nom2','nom3',...]
                # Split variable by comma, creating a string list
                variables_serie=list(variables.split(","))
                #Apply "describe" function and add  adicionar (concatenated) rows with Missing values
                resumen=pd.concat([dataframe.loc[:,variables_serie].describe(include="all",percentiles =[0,0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99,1]), dataframe.loc[:,variables_serie].isnull().sum().to_frame(name = 'missing').T],sort=False)
            else: #Garbage Collector for different cases
                resumen="Invalid entry for variables"
    print("Describe process finished. Elapsed Time: "+str((datetime.datetime.now() - start1).seconds)+" segs")

    start2 = datetime.datetime.now()
    print("Completeness and variability process started, Time: "+ datetime.datetime.now().strftime("%H:%M:%S"))
    if isinstance(resumen, pd.DataFrame)==True: #Verify if there is any error in the imputed parameters 
        #Calculate total count of records
        resumen.loc['total count']=resumen.loc[['count','missing']].sum()
        #Calculate percentage os Missing values
        resumen.loc['% missing']=np.around((resumen.loc['missing']*100/resumen.loc['total count']).astype(np.double),4)
        #Transpose to use better the code
        resumen=resumen.T
        #Calculate variability
        resumen['variability'] = np.where(resumen['min']==resumen['max'], '00_variation', 
                                           np.where(resumen['1%']==resumen['99%'], '02_variation', 
                                                   np.where(resumen['5%']==resumen['95%'], '10_variation', 
                                                           np.where(resumen['10%']==resumen['90%'], '20_variation', 
                                                                   np.where(resumen['25%']==resumen['75%'], '50_variation', 
                                                                           'high_variation')))))
        if variability == 0:
            resumen['variability_decision'] = "accept"
        elif variability == 2:
            resumen['variability_decision'] = np.where(resumen['variability']=='00_variation', 'reject',
                                                        'accept')
        elif variability == 10:
            resumen['variability_decision'] = np.where((resumen['variability']=='00_variation') | (resumen['variability']=='02_variation'), 'reject',
                                                        'accept')
        elif variability == 20:
            resumen['variability_decision'] = np.where((resumen['variability']=='00_variation') | (resumen['variability']=='02_variation') | (resumen['variability']=='10_variation'), 'reject',
                                                        'accept')
        elif variability == 50:
            resumen['variability_decision'] = np.where((resumen['variability']=='00_variation') | (resumen['variability']=='02_variation') | (resumen['variability']=='10_variation') | (resumen['variability']=='20_variation'), 'reject',
                                                        'accept')
        elif variability == 100: 
            resumen['variability_decision'] = np.where((resumen['variability']=='00_variation') | (resumen['variability']=='02_variation') | (resumen['variability']=='10_variation') | (resumen['variability']=='20_variation') | (resumen['variability']=='50_variation'), 'reject',
                                                        'accept')
        else:
            resumen['variability_decision']="VALOR NO VALIDO"
            print("Invalid entry for parameter variability")

        #Calcular completeness
        resumen['completeness_decision']=np.where(resumen['% missing']==0,'accept_100',
                                                 np.where(resumen['% missing']>completeness, 'reject','accept')) 
    else:
        resumen="Invalid entry for variables"
        
    print("Completeness and variability process finished. Elapsed time: "+str((datetime.datetime.now() - start2).seconds)+" segs")
    
    print("Complete process finished. Total Elapsed time: "+str((datetime.datetime.now() - start1).seconds)+" segs")

    return resumen


def treatoutliers(df=None, columns=None, factor=2.0, method='IQR', treament='cap', pct_min=0.05, pct_max=0.95):
    """

    :param df:
    :param columns:
    :param factor:
    :param method:
    :param treament:
    :param pct_min:
    :param pct_max:
    :return:
    """

    for column in columns:
        if method == 'STD':
            permissable_std = factor * df[column].std()
            col_mean = df[column].mean()
            floor, ceil = col_mean - permissable_std, col_mean + permissable_std
        elif method == 'IQR':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            floor, ceil = Q1 - factor * IQR, Q3 + factor * IQR
        elif method == 'PCT':
            floor, ceil = df[column].quantile(pct_min), df[column].quantile(pct_max)
        if treament == 'remove':
            df = df[(df[column] >= floor) & (df[column] <= ceil)]
        elif treament == 'cap':
            df[column] = df[column].clip(floor, ceil)

    return df


def kruskall_relation(data, vars):
    """

    :param data:
    :param vars:
    :return:
    """

    p_vals = []

    for variable in tqdm(vars):
        fvalue, pvalue = stats.kruskal(data.loc[data['Heat_wave'] == 1][variable],
                                       data.loc[data['Heat_wave'] == 0][variable], nan_policy='omit')

        p_vals.append(pvalue)

    results_ranking = pd.DataFrame(pd.concat([pd.Series(vars), pd.Series(p_vals)], axis=1))
    results_ranking.columns = ["variable", "pvalue"]
    results_ranking["-logpval"] = -np.log(results_ranking['pvalue'])
    results_ranking.sort_values(by='-logpval', inplace=True, ascending=False)

    return results_ranking


def read_gbd(path,name):
    """
    Read and concatentate data associated to the Global Burden of Disease study (GBD).

    :param path:
    :param name:
    :return:
    """

    # Get all the files in the directory
    all_files = os.listdir(path + "\\" + name)

    # Keep only the folders
    folders = [name for name in all_files if name.lower() != "citation.txt"]

    # Loop to get the names of the CSV files
    csv_files_app = []
    for i in folders:
        # List all files in directory
        files = os.listdir(path + "\\" + name + "\\" + i)

        # Keep only CSV files
        csv_files = [x for x in files if ".csv" in x]

        # Append file name
        csv_files_app += csv_files

    # Loop to read and append data
    appended_data = []
    for i in range(len(folders)):
        # Read each CSV file
        aux = pd.read_csv(path + "\\" + name + "\\" + str(folders[i]) + "\\" + str(csv_files_app[i]))

        # Append in a list the contents
        appended_data.append(aux)

    # Convert appended files in single big dataframe
    GBD_data = pd.concat(appended_data)

    return GBD_data