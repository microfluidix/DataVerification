
# Our numerical workhorse
import numpy as np
import os

# Import plotting tools
import matplotlib.pyplot as plt

# Import file management tools.
import os
import shutil
import pandas

# Magic function to make matplotlib inline; other style specs must come AFTER
#%matplotlib inline

save_dir = '' # Image Repository
seg_dir = '' # Data Folder Repository

current_dir = os.getcwd()
os.chdir(seg_dir)
dfp = pandas.read_csv('DATA FRAME NAME')
os.chdir(current_dir)


# Info about the graphs

def onpick(event,x,y, DataFrame):
	plt.close(2)
	plt.figure(2)
	line = event.artist
	xdata, ydata = line.get_data()
	ind = event.ind
	frame,particle,experiment,xpoint,ypoint= find_data_point(ind,xdata,ydata,x,y, DataFrame)
	print(experiment)
	try:
		open_image(frame,particle,experiment,xpoint,ypoint)
		print('Image plotted, Particule %s, Experiment %s' % (int(particle),experiment))
	except FileNotFoundError:
		print('The file was not found. Please make sure that the path is right for experiment %s' % experiment)
		pass
	plt.figure(1)


### Finds line corresponding to point in the scatter plot

def find_data_point(ind,xdata,ydata,x,y, DataFrame):
	dr = xdata[ind]
	a = ydata[ind]
	point = DataFrame.loc[DataFrame[x]==dr[0]]
	frame = point['frame'].values
	particle = point['particle'].values
	experiment = point['experiment'].values
	xpoint = point['x'].values
	ypoint = point['y'].values
	return frame[0],particle[0],experiment[0],xpoint[0],ypoint[0]


### Finds image corresponding to that line

def open_image(frame,particle,experiment,xpoint,ypoint):
	plt.figure(2)
	try:
		image_dir = '/media/user/Elements/images/hypoxia/'+experiment
		os.chdir(image_dir)
		experiment = experiment.split('/')
		image_name = experiment[0] +'_s%dt' % int(experiment[1][6])+str(format(int(frame),"04"))+'.tif'
		print(image_name)
	except FileNotFoundError:
		image_dir = '/media/user/Elements1/'+experiment
		os.chdir(image_dir)
		experiment = experiment.split('/')
		image_name = experiment[0] +'_s%dt' % int(experiment[1][6])+str(format(int(frame),"03"))+'.tif'
		print(image_name)
#	image_name = '01-06-2018-exp1_s1t'+str(format(int(frame),"04"))+'.tif'
	img_array = plt.imread(image_name)
	os.chdir(current_dir)
	plt.scatter(xpoint,ypoint, marker = '+',c ='red',s=15)
	plt.imshow(img_array)
	plt.show()
#	plt.savefig('Pic_%s_%s_%s.pdf' % (int(particle),x,y))


## Draws the scatter plot. need to say x = 'dx'; y = 'dy' or whatever variables you want to plot

def scatter_plot(DataFrame, x, y):
	fig = plt.figure(1)
	plt.plot(DataFrame[x],DataFrame[y], 'o',picker = 5)
	fig.canvas.mpl_connect('pick_event',lambda event: onpick(event,x,y, DataFrame))
	plt.show()

# Enter the repository with the experiment and 

scatter_plot(dfp, 'Ecc','v')
