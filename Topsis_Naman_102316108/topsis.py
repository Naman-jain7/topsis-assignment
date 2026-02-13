import sys
import os

import pandas as pd
import numpy as np


def check_input(args):
    if(len(args)!=5):
        error_exit('incorrect number of parameters.')
    
    input_file = args[1]
    weights=args[2]
    impacts=args[3]
    output_file=args[4]

    if not os.path.isfile(input_file):
        error_exit('file not found')

    return input_file, weights, impacts, output_file

def error_exit(msg):
    print(f'error: {msg}')
    sys.exit(1)

def load_data(input_file):
    try:
        df=pd.read_csv(input_file)
    except Exception as e:
        error_exit('unable to read file')
    
    if df.shape[1]<3:
        error_exit('file must contain at least 3 columns')
    
    numeric_df = df.iloc[:,1:]
    if not all(numeric_df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
        error_exit('from 2nd to last columns must contain numeric values only')
    
    return df

def validate_weights_impacts(weights, impacts, num_cols):
    weights = weights.split(',')
    impacts = impacts.split(',')

    if len(weights)!=num_cols or len(impacts)!=num_cols:
        error_exit('number of weights, impacts and columns must be same')

    try:
        weights = [float(w) for w in weights]
    except:
        error_exit('weights must be numeric')

    if not all(i in ["+", "-"] for i in impacts):
        error_exit("impacts must be either + or -")
    return weights, impacts

def topsis(df, weights, impacts):
    data = df.iloc[:,1:].values.astype(float)
    norm = np.sqrt((data**2).sum(axis=0))
    normalized = data/norm
    weighted = normalized*weights

    ideal_best=[]
    ideal_worst=[]

    for i in range(weighted.shape[1]):
        if impacts[i]=='+':
            ideal_best.append(np.max(weighted[:,i]))
            ideal_worst.append(np.min(weighted[:,i]))
        else:
            ideal_best.append(np.min(weighted[:, i]))
            ideal_worst.append(np.max(weighted[:, i]))

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(method="max", ascending=False).astype(int)
    return df

def main():
    input_file, weights, impacts, output_file = check_input(sys.argv)
    df = load_data(input_file)

    num_cols = df.shape[1]-1
    weights, impacts = validate_weights_impacts(weights, impacts, num_cols)
    
    result = topsis(df, weights, impacts)

    result.to_csv(output_file, index=False)
    print('Topsis successful.')

if __name__ == "__main__":
    main()