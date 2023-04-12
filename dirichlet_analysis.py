
"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 2
Due Date 4/10/2023
This code to calculate log liklihood of getting the data generated by `dirichlet.py` and produces a plot based on the draws

 
"""



import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import seaborn as sns
import random
import matplotlib.tri as tri
from scipy.special import beta

if __name__ == "__main__":


	
	if '-f' in sys.argv:
		p = sys.argv.index('-f')
		InputFile = sys.argv[p+1]
	if '-n' in sys.argv:
		p = sys.argv.index('-n')
		picks = int(sys.argv[p+1])
	else:
		picks = 20

	# Opens the datafile and reads it into array   
	
	with open(InputFile) as file:
		table_H0 = pd.read_csv(file, usecols=range(1,4))
		print(table_H0.head()) 
	pH0_white = table_H0['white']
	pH0_green = table_H0['green'] 
	pH0_black = table_H0['black']
	alpha_H0 = [1,2,3]
	alpha_H1 = [4,9,5]
	
	table_H0['sum'] = table_H0.sum(axis=1)
	
	total = table_H0['sum']
	
	alphaH0_sum = np.sum(alpha_H0)
	alphaH1_sum = np.sum(alpha_H1)
	
	beta_H0 = beta(picks, alphaH0_sum)
	beta_H1 = beta(picks, alphaH1_sum)

	likelihood_H0 = []
	likelihood_H1 = []

	for i in range(len(table_H0)):
		
		LH0 = (beta_H0/beta_H1)*(beta(pH0_white[i], alpha_H1[0]) *  beta(pH0_green[i], alpha_H1[1]) * beta(pH0_black[i], alpha_H1[2])) \
				/ (beta(pH0_white[i], alpha_H0[0]) *  beta(pH0_green[i], alpha_H0[1]) * beta(pH0_black[i], alpha_H0[2]))
		LH1 = (beta_H1/beta_H0)*(beta(pH0_white[i], alpha_H0[0]) *  beta(pH0_green[i], alpha_H0[1]) * beta(pH0_black[i], alpha_H0[2])) \
				/ (beta(pH0_white[i], alpha_H1[0]) *  beta(pH0_green[i], alpha_H1[1]) * beta(pH0_black[i], alpha_H1[2]))
		likelihood_H0.append(LH0)
		likelihood_H1.append(LH1)
	   

		
	sns.histplot(np.log(likelihood_H0),stat='probability', bins=10, element="step", color = 'blue', alpha= .5, label=r'H0 - $\alpha = (1,2,3)$')
	sns.histplot(np.log(likelihood_H1),stat='probability', bins=10, element="step", color = 'orange', alpha= .5, label=r'H1 - $\alpha = (4,9,5)$')
	plt.xlabel('Log-Likelihood (log(P(X | H0)/ P(X| H1)))')
	plt.title(rf'Log Likelihood for $\alpha = (1,2,3)$ vs $\alpha = (4,9,5)$, {picks} trials')
	plt.savefig(f'LLH0_{picks}')
	plt.legend()
	
	plt.show()