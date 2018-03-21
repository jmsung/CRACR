"""
Analysis of centrosome heigh, taken by u-manager (Jongmin Sung)

class Data() 
- path, data_name, load(), movie_list[], movie_num, movies = [Movie()], plot(), analysis()

class Movie() 
- movie_name, movie_path, frame_number, I

Data
    18-03-05 jurkat-centrosome
"""

from __future__ import division, print_function, absolute_import
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
import os
from skimage.feature import peak_local_max
colors = ['Blues', 'Greens', 'Reds']

def running_avg(x, n):
    return np.convolve(x, np.ones((n,))/n, mode='valid')

class Movie(object):
    def __init__(self, movie_name, movie_path):
        self.movie_name = movie_name           
        file_list = os.listdir(movie_path) 

        for i in range(len(file_list)):
            if file_list[i][-3:] == 'tif':
                self.file_path = movie_path + '\\' + file_list[i]              
                self.movie = Image.open(self.file_path)
        
        self.n_frame = self.movie.n_frames       
        self.n_row = self.movie.size[1]
        self.n_col = self.movie.size[0]
          
        self.I = np.zeros((self.n_frame, self.n_row, self.n_col), dtype=int)
        for i in range(self.n_frame): 
            self.movie.seek(i) # Move to i-th frame
            self.I[i,] = np.array(self.movie, dtype=int)

class Data(object):
    def __init__(self):
        self.data_path = os.getcwd()
        path_split = self.data_path.split('\\')
        self.data_name = path_split[len(path_split)-1]
        self.movie_list = os.listdir(self.data_path) 
        self.movie_num = len(self.movie_list)
        self.movies = [] 
        for movie_name in self.movie_list:            
            movie = Movie(movie_name, self.data_path + '\\' + movie_name)
            self.movies.append(movie)
    
    def analysis(self):
        pass
        
    def plot(self):
        pass
              
# Start  
plt.close('all')
data = Data()
data.analysis()
data.plot()