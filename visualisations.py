from typing import ByteString, List
import numpy as np 
import matplotlib.pyplot as plt
import json
import os

from numpy.lib.index_tricks import MGridClass 


def visualise_stock_prices(S,DeltaT,start_time = 0):
    """
    Plots stock prices 

    :param S: Stock prices of a bundle of stocks
    :type S: d x T np 2D array
    :param DeltaT: array of evaluation moments for stock prices
    :type DeltaT: list of len T-1
    :param start_time: time relative to which the DeltaT array times are expressed, defaults to 0
    :type start_time: int, optional
    """
    d,T = S.shape
    time = np.ones(T)*start_time
    for i in range(1,len(time)):
        time[i] = time[i-1] + DeltaT[i-1]
    plt.figure()

    for index in range(S.shape[0]): 
        plt.plot(time,S[index,:],"-o", label=f"stock {index}")
    
    plt.xlabel("time")
    plt.ylabel("stock value")
    plt.legend()
    plt.show()


def visualise_json_grid_files(file_names, M_grid,alpha_grid,ref_error, title):

    means = np.ones((len(alpha_grid),len(M_grid)))
    sigmas = np.ones((len(alpha_grid),len(M_grid)))
    # open files, extract the result array
    for filename in file_names:

        with open(filename,"r") as f:
            data = f.read()
            data = json.loads(data)
            for run in data["errors"]:
                m,alpha, results  = run[0],run[1],run[2]
                run_errors = np.array(results)
                means[alpha_grid.index(alpha),M_grid.index(m)] = run_errors.mean()
                sigmas[alpha_grid.index(alpha),M_grid.index(m)] = run_errors.std()
    



    plt.hlines(ref_error,xmin=M_grid[0],xmax=M_grid[-1],linestyles='dashed',label="reference error")
    for i in range(len(alpha_grid)):
        plt.errorbar(np.array(M_grid),means[i,:],sigmas[i,:],marker ='o',label = f"alpha = {alpha_grid[i]}")
    plt.title(title)
    plt.xlabel("M")
    plt.xticks(M_grid)
    plt.ylabel("normalized error")
    plt.ylim(0.10,0.16)
    plt.legend(loc='upper right')
    plt.show()



if __name__ == "__main__":
    filenames = ["SCITAS-results\mpi_bagging2020-12-09.15-41-43.json","SCITAS-results\mpi_bagging2020-12-09.19-25-34.json",
    "SCITAS-results\mpi_bagging2020-12-09.21-04-17.json","SCITAS-results\mpi_bagging2020-12-10.00-05-00.json",
    "SCITAS-results\mpi_bagging2020-12-10.16-00-54.json"]

    visualise_json_grid_files(filenames,[1,4,7,10,13,16,19],[0.3,0.4,0.5,0.6,0.7],.124,"Soft Bagging Normalized error: N_train = 20 000, d= 6, N_test= 100 000")

    
    filenames = ["SCITAS-results\mpi_bagging2020-12-10.03-56-54.json"]
    visualise_json_grid_files(filenames,[1,4,7,10,13,16,19,22,25,28],[0.6],.124,"Soft Bagging Normalized error: N_train = 20 000, d= 6, N_test= 100 000")