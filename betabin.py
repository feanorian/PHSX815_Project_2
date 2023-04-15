
"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 2
Due Date 4/10/2023
This code generates samples from 2 populations of urns from that are beta-binomial distributed. Each urn has 10000 marbles from which 1000 marbles 
are drawn. The results of this sampling is passed to another script `betabin_analysis.py` to calculate log liklihood of getting the counts 
observed
"""


import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import seaborn as sns
import random

if __name__ == "__main__":
	np.random.seed(898)
	


	if '-h' in sys.argv or '--help' in sys.argv:
		print ("Usage: %s [-t -n]" % sys.argv[0])
		print
		sys.exit(1)
	if '-t' in sys.argv:
		p = sys.argv.index('-t')
		N_urns_sample = int(sys.argv[p+1])
	else:
		N_urns_sample = 100
	if '-n' in sys.argv:
		p = sys.argv.index('-n')
		N_marbles_draws = int(sys.argv[p+1])
	else:
		N_marbles_draws = 100
	



	# Function that constructs an urn  passing the number of trials and probability array for the urn. 
	def Category(trials, prob):
		x = np.random.multinomial(trials, prob, 1)
		return x

	# Function that picks random samples for N_Trials with N_picks per trial
	def color_samples(pop_list,N_Trials, N_picks):
	
		#samples the urns from the urn population
		urn_sample = random.sample(pop_list, N_Trials)
		
		# draws marbles from each urn in urn_sample
		urn_draws = [random.sample(urn,N_picks) for urn in urn_sample]

		# store the draws as color data
		urn_draws_colors = []
			
		# converts the draws from urnH0_draws into colors
		for urn in urn_draws:
			color = []
			for i in range(len(urn)):
				if urn[i] == '1':
					color.append('White')
				else:
					color.append('Black')
			urn_draws_colors.append(color)
		return urn_draws_colors
		
	# Determines the counts of White and Black marbles
	def color_success(color_list, **args):    
		urn_dic = []
		for urn in color_list:
			trial = {'white':urn.count('White'), 'black':urn.count('Black')}
				#trial = {'white':round(urn.count('White')/len(urn), 3), 'green': round(urn.count('Green')/len(urn), 3), 'black':round(urn.count('Black')/len(urn), 3)}

			urn_dic.append(trial)
			#labels = urnh0_dic[0].keys()
		df = pd.DataFrame(urn_dic)
		return df
	
	
	
	
	# Alpha vectors for each population
	alpha_H0 = [1,2]
	alpha_H1 = [8,9]
	# Number of urns in each population
	N_urn_pop = 1000
	# Number of urns to sample from N_urn_pop
	#N_urns_sample = 1000
	# Number of marbles per urn
	N_marbles_urn = 10000
	#number of draws per urn
	#N_marbles_draws = 1000
	#Name of file to write data. Notice it changes based on parameters
	InputFile_H0 = f'alpha_H0_D_{N_marbles_draws}_T_{N_urns_sample}.csv'

	# Urns in alpha_H0
	urns_H0 = np.random.dirichlet(alpha_H0, N_urn_pop)
	#  Urns in alpha_H1
	urns_H1 = np.random.dirichlet(alpha_H1, N_urn_pop)
	# combined population of urns
	urn_pops = [urns_H0, urns_H1] 
	
	occurences_list = []
	
	# outcomes of each urn as strings
	outcomes_list= []
	
	# constructs an urn  passing the number of rolls and the probability. Here, the number of marbles is set to N = 100000
	for i in range(len(urn_pops)):
		test = []
		for urn in (urn_pops[i]):
			occurences = Category(N_marbles_urn, urn)[0]
			test.append(occurences)
		occurences_list.append(test)
	
	for j in range(len(occurences_list)):
		outcome = []
		for urn in occurences_list[j]:
			samples = []
			for k in range(len(urn)):
				samples += str(k+1)*urn[k]
			outcome.append(samples)
		outcomes_list.append(outcome) 
	


	urns_color_sampled_H0 = color_samples(outcomes_list[0], N_urns_sample, N_marbles_draws)
	urns_color_sampled_H1 = color_samples(outcomes_list[1], N_urns_sample, N_marbles_draws)
	table_H0 = color_success(urns_color_sampled_H0)
	table_H1 = color_success(urns_color_sampled_H1)
	
	table_H0.rename(columns={'white':'white H0', 'black':'black H0'}, inplace = True)
	table_H1.rename(columns={'white':'white H1', 'black':'black H1'}, inplace = True)

	table_joined = pd.concat([table_H0, table_H1], axis=1)


	doOutputFile = True

	if doOutputFile:
		 table_joined.to_csv(InputFile_H0) 		

	else:
		print(table_joined.head())
		

	# This plots histograms for each color for the entire ensemble of urns set the '-hist' flag to draw them
	#white_H0 = [i[0] for i in urns_H0]
	#white_H1 = [i[0] for i in urns_H1]

	#black_H0 = [k[1] for k in urns_H0]
	#black_H1 = [k[1] for k in urns_H1]

	# Histogram for Black marbles under hypothesis 0
	sns.histplot(table_H0['black H0'],stat='probability', element="step",fill = True, color = 'k', bins='auto', alpha=.25)
	plt.xlabel('Counts')
	plt.title(rf'Distribution of Counts for Black Marbles in $\alpha$_H0 = {str(alpha_H0)}')
	#plt.savefig('BlackH0.png', dpi=700)
	plt.show()##
	
	# Histogram for Black marbles under hypothesis 1
	sns.histplot(table_H1['black H1'],stat='probability', element="step",fill = True, color = 'k', bins='auto', alpha=.25)
	plt.xlabel('Counts')
	plt.title(rf'Distribution of Counts for Black Marbles in $\alpha$_H1 ={str(alpha_H1)} ')
	#plt.savefig('BlackH1.png', dpi=700)
	plt.show()
	
	# Histogram for White marbles under hypothesis 0
	sns.histplot(table_H0['white H0'],stat='probability', element="step",fill = True, color = 'lavender', bins='auto')
	plt.xlabel('Counts')
	plt.title(rf'Distribution of Counts for White Marbles in $\alpha$_H0 = {str(alpha_H0)}')
	#plt.savefig('WhiteH0.png', dpi=700)
	plt.show()
	
	# Histogram for White marbles under hypothesis 1
	sns.histplot(table_H1['white H1'],stat='probability', element="step",fill = True, color = 'lavender', bins='auto')
	plt.xlabel('Counts')
	plt.title(rf'Distribution of Counts for White Marbles in $\alpha$_H1 = {str(alpha_H1)}')
	#plt.savefig('WhiteH1.png', dpi=700)
	plt.show()
