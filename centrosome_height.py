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
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from PIL import Image
import os
from skimage.feature import peak_local_max
from skimage import filters
from scipy import interpolate

n_row = 512
n_col = 512
n_ch = 3
channel = ['Nucleus', 'CRACR', 'Centrosome']
color = ['Blues', 'Greens', 'Reds']
nucleus_size = 40
centrosome_size = 10


class Centrosome(object):
    def __init__(self, I, row, col):
        self.row = row
        self.col = col
        size = centrosome_size
        Iz = np.mean(np.mean(I[:,row-size:row+size,col-size:col+size], axis=2), axis=1)
        self.Iz = Iz - np.min(Iz)
        self.Iz = self.Iz / np.max(self.Iz)
        
    def evaluate(self):
        Iz = self.Iz.copy()
        Iz[Iz<0.1] = 0
        dIz = Iz[1:] - Iz[:-1]
        dIz12 = dIz[1:]*dIz[:-1]
        if sum(dIz12<0) == 1:
            return True
        else:
            return False
                   
class Movie(object):
    def __init__(self, movie_name, movie_path):
        self.movie_name = movie_name    
        self.movie_path = movie_path      
        file_list = os.listdir(movie_path) 
        ch_list = []
        for i in range(len(file_list)):
            if file_list[i][0:1] == 'C':
                ch_list.append(file_list[i])

        movie = Image.open(movie_path+'\\'+ch_list[0])
        self.n_frame = movie.n_frames
        self.I = np.zeros((n_ch, self.n_frame, n_row, n_col), dtype=int)

        for i in range(len(ch_list)):
            movie = Image.open(movie_path+'\\'+ch_list[i])
            ch = int(file_list[i][1:2])            
            for j in range(self.n_frame): 
                movie.seek(j) # Move to i-th frame   
                self.I[ch-1, j,] = np.array(movie, dtype=int)
        
    def projection(self):
        self.I_max = []
        s = [5, 1, 1]
        for i in range(n_ch):
            I = self.I[i]
            I_min = np.min(I, axis=0)
            for j in range(self.n_frame):
                I[j,] = I[j,] - I_min    
            I_max = np.max(I, axis=0)
            I_max = gaussian_filter(I_max, sigma=s[i])
            I_max[I_max < np.max(I_max)/10] = 0
            self.I_max.append(I_max)     
                        
    # Find local maxima from movie.I_max                    
    def find_centrosomes(self): 
        I = self.I_max[2]
        I = gaussian_filter(I, sigma=1)
        self.peak = peak_local_max(I, min_distance=centrosome_size)
        self.c_row = self.peak[::-1,0]
        self.c_col = self.peak[::-1,1]
        self.n_centrosomes = len(self.peak[:, 1])
        print(self.n_centrosomes, 'peaks')
        self.centrosomes = []
        for i in range(self.n_centrosomes):
            centrosome = Centrosome(self.I[2], self.c_row[i], self.c_col[i])
            if centrosome.evaluate():
                self.centrosomes.append(centrosome)
        print(len(self.centrosomes), 'centrosomes')


class Data(object):
    def __init__(self):
        self.data_path = os.getcwd()
        path_split = self.data_path.split('\\')
        self.data_name = path_split[len(path_split)-1]
        self.movie_list = os.listdir(self.data_path) 
        self.movie_num = len(self.movie_list)
        self.movies = [] 
        for movie_name in self.movie_list: 
            movie_path = self.data_path + '\\' + movie_name           
            movie = Movie(movie_name, movie_path)
            self.movies.append(movie)
    
    def analysis(self):
        for i in range(self.movie_num):
            movie = self.movies[i]
            movie.projection()
            movie.find_centrosomes()

    def plot(self):
        plt.close('all')
        # Plot overall movie images
        for i in range(self.movie_num):
            movie = self.movies[i] 
            print(i)

            # Figure 1
#            fig1 = plt.figure(self.movie_list[i], figsize = (20, 15), dpi=300)    
            fig1 = plt.figure(self.movie_list[i]) 
            
            sp1 = fig1.add_subplot(131)       
            sp1.imshow(movie.I_max[0], cmap='viridis')
            sp1.set_title('Nucleus')
            
            sp2 = fig1.add_subplot(132)     
            sp2.imshow(movie.I_max[2], cmap='plasma')
            sp2.scatter(movie.c_col, movie.c_row, s=150, facecolors='none', edgecolors='y')
            sp2.set_title('Peaks = %d' % (movie.n_centrosomes))            
            
            sp3 = fig1.add_subplot(133)     
            sp3.imshow(movie.I_max[0], cmap='viridis', alpha=1)            
            sp3.imshow(movie.I_max[2], cmap='plasma', alpha=0.5)
            
            centrosomes = movie.centrosomes
            for j in range(len(movie.centrosomes)):      
                col = centrosomes[j].col
                row = centrosomes[j].row
                sp3.scatter(col, row, s=150, facecolors='none', edgecolors='y')
            title = 'Centrosomes = %d' % (len(centrosomes))          
            plt.title(title)       
            
            # Figure 2
            fig2 = plt.figure(self.movie_list[i]+'_centrosome')

            n_row = 4
            n_col = 10
            Iz_max = []    
            y_sum = np.zeros(movie.n_frame)        
            for j in range(len(movie.centrosomes)):
                y = movie.centrosomes[j].Iz
                y_sum += np.array(y)
                x = np.arange(0, len(y), 1)
                tck = interpolate.splrep(x, y, s=0)   
                xnew = np.arange(0, len(y), 0.01)
                ynew = interpolate.splev(xnew, tck, der=0)    
                Iz_max.append(xnew[np.argmax(ynew)])
                if j < n_row*n_col:
                    sp1 = fig2.add_subplot(n_row, n_col,j+1)
                    sp1.plot(x, y, 'ro', xnew, ynew, 'k')

            tck_sum = interpolate.splrep(x, y_sum, s=0)
            ynew_sum = interpolate.splev(xnew, tck_sum, der=0)     
            Iz_max_sum = xnew[np.argmax(ynew_sum)]         

            fig3 = plt.figure(self.movie_list[i]+'_centrosome_height')
            sp1 = fig3.add_subplot(131) 
            sp1.plot(Iz_max, 'ko', [np.median(Iz_max)]*len(movie.centrosomes), 'r:')
            sp2 = fig3.add_subplot(132) 
            sp2.hist(Iz_max)
            sp2.set_title('Centrosome height = %.1f' % (np.median(Iz_max)))
            sp3 = fig3.add_subplot(133)
            sp3.plot(x, y_sum, 'ro', xnew, ynew_sum, 'k')
            sp3.set_title('Centrosome height = %.1f' % (Iz_max_sum))
                                                                           
        plt.show()      

#Covert lab: DeepCell
#Cell segmentation
#    https://github.com/luispedro/python-image-tutorial/blob/master/Segmenting%20cell%20images%20(fluorescent%20microscopy).ipynb
#Jeremy's machine learning

              
# Start  
plt.close('all')
data = Data()
data.analysis()
data.plot()

