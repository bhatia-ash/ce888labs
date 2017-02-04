import matplotlib
matplotlib.use('Agg')

import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np 


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
        http://stackoverflow.com/questions/8930370/where-can-i-find-mad-mean-absolute-deviation-in-scipy
    """
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))


def boostrap(statistic_func, iterations, data):
    samples  = np.random.choice(data,replace = True, size = [iterations, len(data)])
    #print samples.shape
    data_mean = data.mean()
    vals = []
    for sample in samples:
        sta = statistic_func(sample)
        #print sta
        vals.append(sta)
    b = np.array(vals)
    #print b
    lower, upper = np.percentile(b, [2.5, 97.5])
    return data_mean,lower, upper



if __name__ == "__main__":
    df = pd.read_csv('./vehicles.csv')
    df = df.dropna()
    #print df.columns
    sns_plot = sns.lmplot(df.columns[0], df.columns[1], data=df, fit_reg=False)

    sns_plot.axes[0,0].set_ylim(0,)
    sns_plot.axes[0,0].set_xlim(0,)

    sns_plot.savefig("scaterplot_veh_1.png",bbox_inches='tight')
    sns_plot.savefig("scaterplot_veh_1.pdf",bbox_inches='tight')

    data_1 = df.values.T[1]
    data_0 = df.values.T[0]
    plt.clf()
    sns_plot2 = sns.distplot(data_0, bins=20, kde=False, rug=True).get_figure()
    sns_plot2 = sns.distplot(data_1, bins=20, kde=False, rug=True).get_figure()
    axes = plt.gca()
    axes.set_xlabel('MPG') 
    axes.set_ylabel('Vehicles')

    sns_plot2.savefig("histogram_veh.png",bbox_inches='tight')
    sns_plot2.savefig("histogram_veh.pdf",bbox_inches='tight')
    
    
    boots_0 = []
    boots_1 = []
    for i in range(100,10000,1000):
        boot_0 = boostrap(np.mean, i, data_0)
        boots_0.append([i,boot_0[0], "mean"])
        boots_0.append([i,boot_0[1], "lower"])
        boots_0.append([i,boot_0[2], "upper"])
        boot_1 = boostrap(np.mean, i, data_1)
        boots_1.append([i,boot_1[0], "mean"])
        boots_1.append([i,boot_1[1], "lower"])
        boots_1.append([i,boot_1[2], "upper"])


    plt.clf()
    df_boot_0 = pd.DataFrame(boots_0,  columns=['Boostrap Iterations','Mean',"Value"])
    df_boot_1 = pd.DataFrame(boots_1,  columns=['Boostrap Iterations','Mean',"Value"])
    sns_plot = sns.lmplot(df_boot_0.columns[0],df_boot_0.columns[1], data=df_boot_0, fit_reg=False,  hue="Value")
    sns_plot = sns.lmplot(df_boot_1.columns[0],df_boot_1.columns[1], data=df_boot_1, fit_reg=False,  hue="Value")




    #sns_plot.axes[0,0].set_ylim(0,)
    #sns_plot.axes[0,0].set_xlim(0,100000)
    axes = plt.gca()
    axes.set_xlabel('iterations') 
    axes.set_ylabel('MPG')

    sns_plot.savefig("bootstrap_confidence_veh.png",bbox_inches='tight')
    sns_plot.savefig("bootstrap_confidence_veh.pdf",bbox_inches='tight')
    

    
    
    #print ("Mean: %f")%(np.mean(data))
    #print ("Var: %f")%(np.var(data))
    


    
