
"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 2
Due Date 4/10/2023
This code to calculate log liklihood of getting the data generated by `betabin.py` and produces a plot based on the draws

 
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import seaborn as sns
import random
from scipy.special import beta

if __name__ == "__main__":


	
	if '-f' in sys.argv:
		p = sys.argv.index('-f')
		InputFile = sys.argv[p+1]
	
	# Opens the datafile and reads it into array   
	
	with open(InputFile) as file:
		table = pd.read_csv(file)
		print(table.head()) 
	
	# Arrays that store the counts of each category for all trials
	pH0_white = table['white H0'] 
	pH0_black = table['black H0']
	
	pH1_white = table['white H1'] 
	pH1_black = table['black H1']

	# alpha vectors used in experiment
	alpha_H0 = [1,2]
	alpha_H1 = [8,9]
	
	
	total = np.sum([pH0_white[0], pH0_black[0]])

	# sum of each alpha vector as input for likelihood functions
	alphaH0_sum = np.sum(alpha_H0)
	alphaH1_sum = np.sum(alpha_H1)

	# Numerator for likelihood functions that is based on sum of alpha vectors and the number of trials
	beta_H0 = beta(total, alphaH0_sum)
	beta_H1 = beta(total, alphaH1_sum)

	likelihoodr_H0 = []
	likelihoodr_H1 = []

	# Calculates likelihood of each hypothesis
	for i in range(len(table)):
		
		LHR_H0 = (beta(alpha_H1[0], alpha_H1[1]) / beta(alpha_H0[0], alpha_H0[1]))*(beta(pH0_white[i] + alpha_H0[0], total - pH0_white[i] + alpha_H0[1]) \
		/ beta(pH0_white[i] + alpha_H1[0], total - pH0_white[i] + alpha_H1[1]))
	
		LHR_H1 = (beta(alpha_H0[0], alpha_H0[1]) / beta(alpha_H1[0], alpha_H1[1]))*(beta(pH0_white[i] + alpha_H1[0], total - pH0_white[i] + alpha_H1[1]) \
		/ beta(pH0_white[i] + alpha_H0[0], total - pH0_white[i] + alpha_H0[1]))
		
		likelihoodr_H0.append(np.log10(LHR_H0))
		likelihoodr_H1.append(np.log10(LHR_H1))
	   
	test = np.quantile(likelihoodr_H0, [.05, .95])
	# Plots the log-likelihood
	sns.histplot(likelihoodr_H0,stat='probability', bins=10, element="step", color = 'blue', alpha= .5, label=rf'H0 - $\alpha = {str(alpha_H0)}$')
	sns.histplot(likelihoodr_H1,stat='probability', bins=10, element="step", color = 'orange', alpha= .5, label=rf'H1 - $\alpha = {str(alpha_H1)}$')
	plt.xlabel('Log-Likelihood (log(P(X | H0)/ P(X| H1)))')
	plt.yscale('log')
	plt.title(rf'Log Likelihood for $\alpha = {str(alpha_H0)}$ vs $\alpha = {str(alpha_H1)}$, {total} draws')
	plt.legend()
	plt.axvline(x = test[0], color='r')
	plt.text(.45*max(likelihoodr_H0), .1, f' reject: LLRH0 < {round(test[0], 2)}')
	#plt.savefig(f'LLH0_{total}')
	plt.show()