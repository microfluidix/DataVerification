
# Our numerical workhorse
import numpy as np
import os

# Import plotting tools
import matplotlib.pyplot as plt
# Import file management tools.
import glob
import os
import shutil
import pandas

# Magic function to make matplotlib inline; other style specs must come AFTER
#%matplotlib inline


home_dir = r'D:\sondeCalcium\\'

current_dir = os.getcwd()
os.chdir(home_dir)
dfp = pandas.read_csv('NonOVA.csv')
os.chdir(current_dir)

dfp['Intensity'] = dfp['mass']/41**2

# Info about the graphs

def onpick(event,x,y, DataFrame):
	plt.close(2)
	plt.close(3)
	plt.figure(2)
	plt.figure(3)

	line = event.artist
	xdata, ydata = line.get_data()
	ind = event.ind
	frame,particle,xpoint,ypoint= find_data_point(ind,xdata,ydata,x,y, DataFrame)
	try:
		plot_single(particle, x, y, DataFrame)
		print('Image plotted, Particule %s' % int(particle))
	except:
		print('Could not print the single selected plot.')
	try:
		open_image(frame,particle,xpoint,ypoint)
		print('Image plotted, Particule %s' % int(particle))
	except FileNotFoundError:
		pass
	plt.figure(1)


### Finds line corresponding to point in the scatter plot

def find_data_point(ind,xdata,ydata,x,y, DataFrame):
	dr = xdata[ind]
	a = ydata[ind]
	point = DataFrame.loc[(DataFrame[x]==dr[0])&(DataFrame[y]==a[0])]
	frame = point['frame'].values
	particle = point['particle'].values

	print(particle)

	points = DataFrame.loc[(DataFrame['particle'] == particle[0])]
	xpoints = points['x'].values
	ypoints = points['y'].values
	return frame[0],particle[0],xpoints,ypoints


### Finds image corresponding to that line

def plot_single(particle, x, y, DataFrame):

	plt.figure(2)

	for k in DataFrame['particle'].unique():

		locFrame = DataFrame.loc[DataFrame['particle'] == k]

		if k != particle:

			plt.plot(locFrame[x], locFrame[y], '--k', alpha = 0.1)

		if k == particle:

			 plt.plot(locFrame[x], locFrame[y], '-r')

	plt.ylabel('Intensity (AU)')
	plt.xlabel('Time')
	plt.show()

def open_image(frame,particle,xpoint,ypoint):
	plt.figure(3)

	_imshow_style = dict(origin='lower', interpolation='nearest',
                         vmin = 300, vmax = 10000, cmap=plt.cm.gray)

	try:
		image_dir = r'D:\sondeCalcium\B16CD8nonOVA'
		os.chdir(image_dir)
		image_name = os.listdir(image_dir)[frame]
		print(image_name)
	except FileNotFoundError:
		print(image_name)

	os.chdir(r'D:\sondeCalcium\B16CD8nonOVA')

	img_array = plt.imread(image_name)
	os.chdir(current_dir)
	plt.plot(xpoint,ypoint,c ='red')
	plt.imshow(img_array, **_imshow_style)
	plt.show()
#	plt.savefig('Pic_%s_%s_%s.pdf' % (int(particle),x,y))


## Draws the scatter plot. need to say x = 'dx'; y = 'dy' or whatever variables you want to plot

def scatter_plot(DataFrame, x, y):

	fig = plt.figure(1)

	for particle in dfp['particle'].unique():

		locFrame = dfp.loc[dfp['particle'] == particle]
		plt.plot(locFrame[x],locFrame[y],picker = 1)

	fig.canvas.mpl_connect('pick_event',lambda event: onpick(event,x,y, DataFrame))
	plt.ylabel('Intensity (AU)')
	plt.xlabel('Time')
	plt.show()

scatter_plot(dfp, 'time','Intensity')
