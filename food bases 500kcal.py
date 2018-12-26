################################################
### values here are per 500 kcal of the food ###
################################################

################################################
# worth mentioning:
# salmon has 73% vit E
# sweet potatoes have 458% vit A
# potatoes 48% vit C 
# corn 44% vit C 
# shrimp has 42% vit A and 62% vit E
# eggs have 54% vit A
# swiss cheese 41% vit A
# cheddar cheese 46% vit A
################################################


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axis as axis
import matplotlib.image as image
from matplotlib.offsetbox import(OffsetImage, AnnotationBbox)


###############################################################
############### setting up lists ##############################
###############################################################
# [name, units, RDI]
bases = [['Omega-3    ', 'g', 1.6], \
		['Omega-6    ', 'g', 17], \
		['vitamin B1 ', 'mg', 1.2], \
		['vitamin B2 ', 'mg', 1.3], \
		['vitamin B3 ', 'mg', 16], \
		['vitamin B5 ', 'mg', 5], \
		['vitamin B6 ', 'mg', 1.3], \
		['vitamin B12', 'µg', 2.4], \
		['Choline    ', 'mg', 550], \
		['Folate     ', 'µg', 400], \
		['Calcium    ', 'mg', 1000], \
		['Copper     ', 'mg', 0.9], \
		['Iron       ', 'mg', 8], \
		['Magnesium  ', 'mg', 400], \
		['Manganese  ', 'mg', 2.3], \
		['Phosphorus ', 'mg', 700], \
		['Potassium  ', 'mg', 4700], \
		['Selenium   ', 'µg', 65], \
		['Zinc       ', 'mg', 11]]

# will be [number, food, trans fat, omega-3, ... , zinc]
foods = [[0, 'soy_beans'], \
		[1, 'tofu'], \
		[2, 'black_beans'], \
		[3, 'chickpeas'], \
		[4, 'kidney_beans'], \
		[5, 'navy_beans'], \
		[6, 'fava_beans'], \
		[7, 'pinto_beans'], \
		[8, 'green_lentils'], \
		[9, 'red_lentils'], \
		[10, 'corn'], \
		[11, 'potatoes'], \
		[12, 'sweet_potatoes'], \
		[13, 'white_rice'], \
		[14, 'basmati_rice'], \
		[15, 'jasmine_rice'], \
		[16, 'brown_rice'], \
		[17, 'couscous'], \
		[18, 'millet'], \
		[19, 'buckwheat'], \
		[20, 'quinoa'], \
		[21, 'oats'], \
		[22, 'pasta'], \
		[23, 'whole_wheat_pasta'], \
		[24, 'wheat_bread'], \
		[25, 'rye_bread'], \
		[26, 'whole_wheat_bread'], \
		[27, 'eggs'], \
		[28, 'yogurt'], \
		[29, 'swiss_cheese'], \
		[30, 'feta_cheese'], \
		[31, 'cheddar_cheese'], \
		[32, 'cottage_cheese'], \
		[33, 'shrimp'], \
		[34, 'canned_tuna'], \
		[35, 'salmon'], \
		[36, 'tilapia'], \
		[37, 'alaska_pollock'], \
		[38, 'catfish_farmed'], \
		[39, 'catfish_wild'], \
		[40, 'cod'], \
		[41, 'chicken_breast'], \
		[42, 'chicken_legs'], \
		[43, 'steak'], \
		[44, 'pork'], \
		[45, 'lamb_breast'], \
		[46, 'lamb_leg']]


# 27         <=> vegan options
# 33         <=> vegetarian options
# 41         <=> pescetarian options
# len(foods) <=> all options
food_range_top = len(foods)

# 0  <=> includes all
# 1  <=> kicks out soy beans
# 10  <=> kicks out legumes
# 27 <=> kicks out legumes and starches
# 35 <=> kicks out legumes, starches and fish
# 41 <=> leaves only meat
# can't be higher than food_range_top
food_range_bottom = 0

# a more handy way to use it
food_range = (food_range_bottom, food_range_top)


# will be [food number, food name, % bases coverage]
foods_single_coverages = [[foods[j][0], foods[j][1]] for j in range(food_range[0], food_range[1]) ]

# will be [food_no_1, food_no_2, food names, % bases coverage]
foods_two_coverages = [[foods[i][0], foods[j][0], foods[i][1] + ' + ' + foods[j][1] ] for i in range(food_range[0], food_range[1]) for j in range(i, food_range[1]) ]

# will be [food_no_1, food_no_2, food_no_3,
#          food names, % bases coverage]
foods_three_coverages = [[foods[i][0], foods[j][0], foods[k][0], foods[i][1] + ' + ' + foods[j][1] + ' + ' + foods[k][1] ] for i in range(food_range[0], food_range[1]) for j in range(i, food_range[1]) for k in range(j, food_range[1])]
###############################################################
###############################################################
###############################################################


###############################################################
####### loading data from the .txt files into *foods* #########
###############################################################
# get foods[0] = ['red_lentils', trans, omega-3, omega-6, ...]
for j in range(len(foods)):
	file = open(foods[j][1] + "_500kcal.txt", "r", errors='ignore')
	# save space for trans fats to be the 2nd element of the list
	foods[j].append(0)
	# values are in specific lines, find them and save them
	for i in range(1, 283):
		# omega-3, omega-6, vitamins, minerals
		if i in [171, 174, 215, 218, 221, 224, 227, 230, 233, 236, 255, 258, 261, 264, 267, 270, 273, 276, 282]:
			foods[j].append(float(file.readline().replace('\n', '')))
		# trans fats
		elif i == 180:
			foods[j][2] = file.readline()
		# skip useless line
		else:
			file.readline()
	file.close()
###############################################################
###############################################################
###############################################################


###############################################################
##### defining functions that calculate % bases coverages #####
###############################################################
# single food bases coverage
def single_food(food_number):
	total = 0
	for q in range(len(bases)):
		x = foods[food_number][q+3]/bases[q][2]*100
		if x > 100:
			x = 100
		total += x
	return total/len(bases)

# two foods bases coverage
def two_foods(food_1, food_2):
	total = 0
	for q in range(len(bases)):
		x = (foods[food_1][q+3] + foods[food_2][q+3]) / bases[q][2] * 100
		if x > 100:
			x = 100
		total += x
	return total/len(bases)

# three foods bases coverage
def three_foods(food_1, food_2, food_3):
	total = 0
	for q in range(len(bases)):
		x = (foods[food_1][q+3] + foods[food_2][q+3] + foods[food_3][q+3]) / bases[q][2] * 100
		if x > 100:
			x = 100
		total += x
	return total/len(bases)
###############################################################
###############################################################
###############################################################


###############################################################
#### an infinite loop for checking what a single food has #####
###############################################################
def check_single_food():
	while True:
		
		print("##########################")
		n = input("food number: ")
		
		try:
			n = int(n)
			if  n < len(foods) and n >= 0:
				print("##########################")
				print("###", foods[n][1].replace("_", " ") + ': ###')
				print("##########################")
				print("bases coverage:", round(single_food(n), 1), '%')
				print("##########################")
				for i in range(len(bases)):
					# if value is 0 then maybe Cronometer has no data on it
					if foods[n][i+3] == 0:
						note = "<-- watch out"
					else:
						note = ""

					percent = round(foods[n][i+3]/bases[i][2]*100, 1)
					print(bases[i][0] + ': ', foods[n][i+3], bases[i][1], '<=>', percent, '%', note)
		except:
			if n == 'stop':
				break
			else:
				print("Bad input - try again")
###############################################################
###############################################################
###############################################################


###############################################################
###### an infinite loop for checking what two foods have ######
###############################################################
def check_two_foods():
	while True:
		
		print("##########################")
		n = input("food numbers: ")
		
		try:
			temp = [int(i) for i in n.split()]
			
			if  temp[0] < len(foods) and temp[0] >= 0 and temp[1] < len(foods) and temp[1] >= 0:
				print("##########################")
				print("###", foods[temp[0]][1].replace("_", " ") + ' + ' + foods[temp[1]][1].replace("_", " ") + ': ###')
				print("##########################")
				print("bases coverage:", round(two_foods(temp[0], temp[1]), 1), '%')
				print("##########################")
				
				for i in range(len(bases)):
					percent = round((foods[temp[0]][i+3]+foods[temp[1]][i+3])/bases[i][2]*100, 1)
					print(bases[i][0] + ': ', round(foods[temp[0]][i+3] + foods[temp[1]][i+3], 1), bases[i][1], '<=>', percent, '%')
		
		except:
			if n == 'stop':
				break
			else:
				print("Bad input - try again")
###############################################################
###############################################################
###############################################################


###############################################################
##### an infinite loop for checking what three foods have #####
###############################################################
def check_three_foods():
	while True:
		
		print("##########################")
		n = input("food numbers: ")
		
		try:
			temp = [int(i) for i in n.split()]
			
			if  all(x < len(foods) for x in temp) and all(x >= 0 for x in temp):
				print("##########################")
				print("###", foods[temp[0]][1].replace("_", " ") + \
					' + ' + foods[temp[1]][1].replace("_", " ") + \
					' + ' + foods[temp[2]][1].replace("_", " ") + ': ###')
				print("##########################")
				print("bases coverage:", round(three_foods(temp[0], temp[1], temp[2]), 1), '%')
				print("##########################")
				
				for i in range(len(bases)):
					percent = round((foods[temp[0]][i+3]+foods[temp[1]][i+3]+foods[temp[2]][i+3])/bases[i][2]*100, 1)
					print(bases[i][0] + ': ', round(foods[temp[0]][i+3] + foods[temp[1]][i+3] + foods[temp[2]][i+3], 1), bases[i][1], '<=>', percent, '%')
		
		except:
			if n == 'stop':
				break
			else:
				print("Bad input - try again")
###############################################################
###############################################################
###############################################################


###############################################################
####### calculating, sorting descendingly and printing ########
####### % coverages of single foods                    ########
###############################################################
def single_food_ranking():
	global foods_single_coverages
	for i in range(len(foods_single_coverages)):
		foods_single_coverages[i].append(round(single_food(i), 1))

	foods_single_coverages = sorted(foods_single_coverages, reverse=True, key=lambda x: x[2])

	for i in range(len(foods_single_coverages)):
		print(str(i+1) + '.', foods_single_coverages[i][1].replace("_", " ") + ':', foods_single_coverages[i][2], '%')
###############################################################
###############################################################
###############################################################


###############################################################
####### calculating, sorting descendingly and printing ########
####### % coverages of two foods                       ########
###############################################################
def two_foods_ranking():
	global foods_two_coverages
	for i in range(len(foods_two_coverages)):
		j = foods_two_coverages[i][0]
		k = foods_two_coverages[i][1]
		foods_two_coverages[i].append(round(two_foods(j, k), 1))

	foods_two_coverages = sorted(foods_two_coverages, reverse=True, key=lambda x: x[3])

	for i in range(len(foods_two_coverages)):
		print(str(i+1) + '.', foods_two_coverages[i][2].replace("_", " ") + ':', foods_two_coverages[i][3], '%')
###############################################################
###############################################################
###############################################################


###############################################################
####### calculating, sorting descendingly and printing ########
####### % coverages of three foods                     ########
###############################################################
def three_foods_ranking():
	global foods_three_coverages
	for i in range(len(foods_three_coverages)):
		j = foods_three_coverages[i][0]
		k = foods_three_coverages[i][1]
		l = foods_three_coverages[i][2]
		foods_three_coverages[i].append(round(three_foods(j, k, l), 1))

	foods_three_coverages = sorted(foods_three_coverages, reverse=True, key=lambda x: x[4])

	for i in range(len(foods_three_coverages)):
		print(str(i+1) + '.', foods_three_coverages[i][3].replace("_", " ") + ':', foods_three_coverages[i][4], '%')
###############################################################
###############################################################
###############################################################


###############################################################
######### function that makes horizontal bar charts ###########
###############################################################
def bar_chart(y_labels, x_values, figname, version, y_numbers, dimensions):
	fig, ax = plt.subplots(figsize=dimensions)
	#plt.title("Coverage of nutritional bases* by two foods (500 kcal each)", fontsize=19)
	#plt.suptitle("*all vitamins, minerals, omega 6 and omega 3 fatty acids -\n- except vitamins A, C, E, K (found mostly in fruits and veggies) and sodium (found in salt)", fontsize=12)
	
	if dimensions[1] == 60: # height of the chart in inches (100 items on chart)
		plt.figtext(.5,.991,'Coverage of nutritional bases* by ' + version, fontsize=20, ha='center')
		plt.figtext(.5,.98,'*all vitamins, minerals, omega 6 and omega 3 fatty acids\nexcept vitamins A, C, E, K (found mostly in fruits and veggies),\nvitamin D (sun vitamin), sodium and iodine (found in salt)', fontsize=12, ha='center')
	else: # smaller chart for single food because there are only 47 foods 
		plt.figtext(.5,.98,'Coverage of nutritional bases* by ' + version, fontsize=20, ha='center')
		plt.figtext(.5,.96,'*all vitamins, minerals, omega 6 and omega 3 fatty acids\nexcept vitamins A, C, E, K (found mostly in fruits and veggies),\nvitamin D (sun vitamin), sodium and iodine (found in salt)', fontsize=12, ha='center')

	ax.set_xlabel('% RDI (Recommended Daily Intake)', fontsize=12)
	ax.xaxis.set_label_position('top') 
	ax.xaxis.tick_top()
	ax.set_xlim(0, 100)
	ax.set_ylim(0, len(y_labels)+1)
	ax.invert_yaxis()
	ax.set_yticks(range(1, len(y_labels)+1))
	ax.set_yticklabels(y_numbers)
	scores = ax.barh(range(1, len(y_labels) + 1), x_values, color='#f6b352')
	# to change margins we change only the first number in the brackets
	# so in (20/25.4) we change 20 (in milimeters)
	plt.subplots_adjust(left = (20/25.4)/dimensions[0], bottom = (20/25.4)/dimensions[1], right = 1 - (20/25.4)/dimensions[0], top = 1 - (50/25.4)/dimensions[1])

	# show percentages next to the bars
	if figname != '_Coverage by three foods - top 100.png':
		for i in range(len(scores)):
			width = scores[i].get_width()
			height = scores[i].get_height()
			ax.text(width - 1, scores[i].get_y() + height/2 + 0.03, '%g%%' % width, ha='right', va='center', fontsize=12)
			ax.text(1, scores[i].get_y() + height/2 + 0.03, '%s' % y_labels[i].replace("_", " "), ha='left', va='center', color='black', fontsize=12)
	else:
		for i in range(len(scores)):
			width = scores[i].get_width()
			height = scores[i].get_height()
			ax.text(width - 1, scores[i].get_y() + height/2, '%g%%' % width, ha='right', va='center', fontsize=12)
			ax.text(1, scores[i].get_y() + height/2 + 0.03, '%s' % y_labels[i].replace("_", " "), ha='left', va='center', color='black', fontsize=12)

	# add images to the plot
	# sadly it looks worse and only makes it harder to look at the graph
	'''for i in range(len(scores)):
					# load .png file as an array
					image_as_array = image.imread("_" + foods_single_coverages[i][1] + ".png")
													
					# set zoom (all pictures are 500x500 px)
					imagebox = OffsetImage(image_as_array, zoom=0.09)
					imagebox.image.axes = ax
												
					# place the pictures a bit above the bars
					width = scores[i].get_width() + 4.5
															
					# i is the number of the bar starting from the top 
					ab = AnnotationBbox(imagebox, (width, i+1), xycoords='data', frameon=False)	
					ax.add_artist(ab)'''
			
	#plt.show()
	fig.savefig(figname, dpi=100)
###############################################################
###############################################################
###############################################################


###############################################################
###################### CONTROL PANEL ##########################
###############################################################

# checking nutrients in specific combinations
#check_single_food()
#check_two_foods()
#check_three_foods()


# to create a chart you have to enable both the ranking and 
# the appropriate bar_chart function
foods_on_chart = len(foods)

#single_food_ranking()  # set foods_on_chart = len(foods) if you want a chart
#bar_chart([foods_single_coverages[i][1] for i in range(foods_on_chart)], [foods_single_coverages[j][2] for j in range(foods_on_chart)], '_Coverage by one food.png', 'staple foods (per 500 kcal)', range(1, foods_on_chart+1), (13,30))   

two_foods_ranking()
# two foods - top 100
bar_chart([foods_two_coverages[i][2] for i in range(foods_on_chart)], [foods_two_coverages[j][3] for j in range(foods_on_chart)], '_Coverage by two foods - no soy.png', 'two staple foods (500 kcal each) - no soy', range(1, foods_on_chart+1), (13,60))
# two foods - bottom 100
#bar_chart([foods_two_coverages[i-foods_on_chart][2] for i in range(foods_on_chart)], [foods_two_coverages[j-foods_on_chart][3] for j in range(foods_on_chart)], '_Coverage by two foods - bottom 100.png', 'two staple foods (500 kcal each) - bottom 100', range(len(foods_two_coverages)+1-foods_on_chart, len(foods_two_coverages)+1), (13,60))

#three_foods_ranking()
# three foods - top 100
#bar_chart([foods_three_coverages[i][3] for i in range(foods_on_chart)], [foods_three_coverages[j][4] for j in range(foods_on_chart)], '_Coverage by three foods - no soy.png', 'three staple foods (500 kcal each) - no soy', range(1, foods_on_chart+1), (13,60))
# three foods - bottom 100
#bar_chart([foods_three_coverages[i-foods_on_chart][3] for i in range(foods_on_chart)], [foods_three_coverages[j-foods_on_chart][4] for j in range(foods_on_chart)], '_Coverage by three foods - bottom 100.png', 'three staple foods (500 kcal each) - bottom 100', range(len(foods_three_coverages)+1-foods_on_chart, len(foods_three_coverages)+1), (13,60))

###############################################################
###############################################################
###############################################################


