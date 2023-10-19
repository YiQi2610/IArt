import csv
import random
import gensim.downloader
from temp_algo import liste_mots_temp
import os

# Generate an image with Stable Diffusion by using dominant color, emotion and heart beat rate of user
def generate_img(main_color, main_emotion, heartrate, temperature, export_path):
    # Open csv file
    
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	f = open("words_diffusion.csv", 'r')

	# Create prompt with data given
	prompt = [int(float(heartrate)), main_emotion, main_color]

	#Create four lists contaning all prompt words in categories
	names = []
	styles = []
	artists = []
	mediums = []
	all_rows = []

	for row in csv.reader(f):
		all_rows.append(row)

	all_rows = all_rows[1:50]

	for row in all_rows:
		for i in range(4):
			if row[5*i] != '':
				if(i==0):
					names.append(row[5*i:5*i+3])
				elif(i==1):
					styles.append(row[5*i:5*i+3])
				elif(i==2):
					artists.append(row[5*i:5*i+3])
				else:
					mediums.append(row[5*i:5*i+3])

	# Find the prompt words corresponding to data given by using the nearest algorithm 
	# Choose randomly if there is more than one prompt word in the same category
	results = []
	for l in [names,styles,artists,mediums]:
		emotions_l = []
		for elt in l:
			if elt[2] == prompt[1]:
				emotions_l.append(elt)
		sorted_dist = []
		for elt in emotions_l:	
			d = abs(int(elt[1]) - prompt[0])
			sorted_dist.append((d,elt))
		sorted_dist.sort()
		m = sorted_dist[0][0]
		i=0
		res = []
		while(sorted_dist[i][0] == m):
			res.append(sorted_dist[i][1])
			i+=1

		results.append(random.choice(res))

	# Use gensim word2vec model to diversify the prompt word for category "name"
	model = gensim.downloader.load("glove-wiki-gigaword-50")

	w1 = results[0][0]
	vector = [w1]
 	# Get some words which are the most similar with initial prompt word 
	words = model.most_similar(positive=w1)
	# Choose randomly a word among all similar words plus the inital prompt word
	for word in words:
		vector.append(word[0])
	selcted_word_from_vector = random.choice(vector)

	phrase = ''
	cpt = 0
	# Create the final prompt phrase
	for elt in results:
		if(cpt==0):phrase+=selcted_word_from_vector+ ', '
		else:phrase+=elt[0] + ', '
		cpt+=1
  
	# Add four prompt words based on temperature
	words_temp = liste_mots_temp(int(temperature))
	for word in words_temp:
		phrase += word + ', '

	# Add color to prompt phrase
	phrase += prompt[2]
	print(phrase)


	### VERSION AVEC INSTALLATION LOCALE ###

	from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
	import torch

	model_id = "stabilityai/stable-diffusion-2"

	## Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
	pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
	pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
	pipe = pipe.to("cuda")

	prompt = phrase
	image = pipe(prompt, width=728, height=728).images[0]
		
	image.save(export_path)
