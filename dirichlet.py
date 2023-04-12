
"""
Name: Craig Brooks
PHSX 815 Spring 2023
Project # 2
Due Date 4/10/2023
This code generates samples from 2 populations of urns from that are Dirichlet distributed. Each urn has 10000 marbles from which 1000 marbles 
are drawn. The results of this sampling is passed to another script `dirichlet_analysis.py` to calculate log liklihood of getting the counts 
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
		N_urns_sample = int(sys.argv[p+1]) #number of sample urns
	else:
		N_urns_sample = 1000
	if '-n' in sys.argv:
		p = sys.argv.index('-n')
		N_marbles_draws = int(sys.argv[p+1])
	else:
		N_marbles_draws = 100 # number of marble draws per urn
	



	# Function that constructs an urn  passing the number of trials and probability array for the urn. 
	def Category(trials, prob):
		x = np.random.multinomial(trials, prob, 1)
		return x

	# Function that picks random samples for N_Trials with N_picks per trial
	def color_samples(N_Trials, N_picks):
	
		#samples the urns from the H0 population
		urnH0_sample = random.sample(outcomes_list, N_Trials)

		# draws marbles from each urn in urnH0_sample
		urnH0_draws = [random.sample(urn,N_picks) for urn in urnH0_sample]
		
		# store the draws as color data
		urnh0_draws_colors = []
		# converts the draws from urnH0_draws into colors
		for urn in urnH0_draws:
			color = []
			for i in range(len(urn)):
				if urn[i] == '1':
					color.append('White')
				elif urn[i] == '2':
					color.append('Green')
				else:
					color.append('Black')
			urnh0_draws_colors.append(color)
		return urnh0_draws_colors
		
	# Determines the number of picks until a successful green pick, then appends to the array green_index
	def color_success(color_list, **args):    
		urnh0_dic = []
		for urn in color_list:
			trial = {'white':urn.count('White'), 'green': urn.count('Green'), 'black':urn.count('Black')}
			urnh0_dic.append(trial)
		#labels = urnh0_dic[0].keys()
		dfH0 = pd.DataFrame(urnh0_dic)
		return dfH0
	
	
	
	
	# Alpha vectors for each population
	alpha_H0 = [1,2,3]
	alpha_H1 = [4,9,5]
	# Number of urns in each population
	N_urn_pop = 10000
	
	
	# Number of marbles per urn
	N_marbles_urn = 10000
	
	
	#Name of file to write data. Notice it changes based on parameters
	InputFile_H0 = f'alpha_H0_D_{N_marbles_draws}_T_{N_urns_sample}.csv'

	# Urns in alpha_H0
	urns_H0 = np.random.dirichlet(alpha_H0, N_urn_pop)
	#  Urns in alpha_H1
	urns_H1 = np.random.dirichlet(alpha_H1, N_urn_pop)

	
	
	occurences_list = []
	# outcomes of each urn as strings
	outcomes_list = []

	# constructs an urn  passing the number of rolls and the probability. Here, the number of marbles is set to N = 100000
	for urn in urns_H0:
		occurences = Category(N_marbles_urn, urn)[0]
		occurences_list.append(occurences)
	for urn in occurences_list:
		outcome = []
		for i in range(len(urn)):
			outcome += str(i+1)*urn[i]
		outcomes_list.append(outcome)
	
	
	urns_color_sampled =  color_samples(N_urns_sample, N_marbles_draws)
	table_H0 = color_success(urns_color_sampled)
	
	doOutputFile = True

	if doOutputFile:
		 table_H0.to_csv(InputFile_H0) 
	

	else:
		print(table_H0.head())
		print(len(table_H0))



	# This plots histograms for each color for the entire ensemble of urns set the '-hist' flag to draw them
	white_H0 = [i[0] for i in urns_H0]
	white_H1 = [i[0] for i in urns_H1]

	green_H0 = [j[1] for j in urns_H0]
	green_H1 = [j[1] for j in urns_H1]

	black_H0 = [k[2] for k in urns_H0]
	black_H1 = [k[2] for k in urns_H1]

	# Histogram for Green marbles under hypothesis 0
	sns.histplot(green_H0,stat='probability', element="step",fill = True, color = 'green', bins='auto', alpha=.25)
	plt.xlabel('Probability Counts')
	plt.title('Distribution of Probabilities for Green Marbles in Left(H0)')
	#plt.savefig('GreenH0.png', dpi=700)
	plt.show()

	# Histogram for Green marbles under hypothesis 1
	sns.histplot(green_H1,stat='probability', element="step",fill = True, color = 'green', bins='auto', alpha=.25)
	plt.xlabel('Probability Counts')
	plt.title('Distribution of Probabilities for Green Marbles in Right(H1)')
	#plt.savefig('GreenH1.png', dpi=700)
	plt.show()
	
	# Histogram for Black marbles under hypothesis 0
	sns.histplot(black_H0,stat='probability', element="step",fill = True, color = 'k', bins='auto', alpha=.25)
	plt.xlabel('Probability Counts')
	plt.title('Distribution of Probabilities for Black Marbles in Left(H0)')
	#plt.savefig('BlackH0.png', dpi=700)
	plt.show()
	
	# Histogram for Black marbles under hypothesis 1
	sns.histplot(black_H1,stat='probability', element="step",fill = True, color = 'k', bins='auto', alpha=.25)
	plt.xlabel('Probability Counts')
	plt.title('Distribution of Probabilities for Black Marbles in Right(H1) ')
	#plt.savefig('BlackH1.png', dpi=700)
	plt.show()
	
	# Histogram for White marbles under hypothesis 0
	sns.histplot(white_H0,stat='probability', element="step",fill = True, color = 'lavender', bins='auto')
	plt.xlabel('Probability Counts')
	plt.title('Distribution of Probabilities for White Marbles in Left(H0)')
	#plt.savefig('WhiteH0.png', dpi=700)
	plt.show()
	
	# Histogram for White marbles under hypothesis 1
	sns.histplot(white_H1,stat='probability', element="step",fill = True, color = 'lavender', bins='auto')
	plt.xlabel('Probability Counts')
	plt.title('Distribution of Probabilities for White Marbles in Right(H1)')
	#plt.savefig('WhiteH1.png', dpi=700)
	plt.show()


	
