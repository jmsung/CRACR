"""
Colocalization analysis (by Jongmin Sung)

Ch1 = 488 = CRACR
Ch2 = 561 = LCK or LAT
Ch3 = 640 = TCR antibody

Protocol
- ImageJ > open the stacked tif 
- Open Image/Color/Channels Tool
- Play movie and find a cell that looks good
- Select the area and duplicate
- Save the image as, e.g. cell1
- Image/Color/Split Channels 
- Save each colors as, e.g. cell1-ch1, cell1-ch2, cell1-ch3
- Analyze the image using this code


"""
from __future__ import division, print_function, absolute_import
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter as gf
import matplotlib.colors as colors
import scipy.stats as st
color = ['Blues', 'Greens', 'Reds']
#color = ['magma']*3
sigma = 1.0
step = 40
row = 2
p1 = 60
p2 = 80

class FramePixelIntensity(object):
    def __init__(self, cell, ch):
        name = cell+'.tif'
        movie = Image.open(name)
        self.ch = ch[0]
        self.sample = ch[1]
        self.n_ch = len(ch[0])
        self.n_frame = int((movie.n_frames)/self.n_ch)
        self.width = movie.width
        self.height = movie.height
        
        # I[channel,frame,row,column]         
        self.I = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=int) 
        self.Is = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=int)  
        self.mask1 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=bool)
        self.mask2 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=bool)
        self.Im1 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=int)  
        self.Im2 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=int)          
      
        for i in range(self.n_ch): # ith channel
            movie_i = Image.open(cell+'-'+ch[0][i]+'.tif')      
            for j in range(self.n_frame): # jth frame
                movie_i.seek(j) 
                I0 = np.array(movie_i, dtype=int)
                self.I[i,j] = I0 - I0.min()
                self.Is[i,j] = gf(self.I[i,j], sigma)
       
        for j in range(self.n_frame):
            for i in range(self.n_ch):
                # Mask1 to find a cell from ch2
                m1 = self.Is[1,j] > np.percentile(self.Is[1,j], p1)                 
                self.mask1[i,j] = m1
                self.Im1[i,j,m1] = self.I[i,j,m1]
                self.mask2[i,j,m1] = self.Is[i,j,m1] > np.percentile(self.Is[i,j,m1], p2)
                self.Im2[i,j,self.mask2[i,j]] = self.I[i,j,self.mask2[i,j]]
                                
    def plot_all(self):
        self.plot_I()
        self.plot_Is()
        self.plot_Im1()
        self.plot_Im2()
        self.spatial_corr1()
        self.spatial_corr2()
        self.intensity_corr()
        plt.show()


    def plot_I(self):
        # Colormap of each channel
        for i in range(self.n_ch):
            plt.figure()
            suptitle = '%s (%s), #Frame = %d' \
                    %(self.sample[i], self.ch[i], self.n_frame)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.I[i,j], 
                    norm = colors.Normalize(vmin=0, vmax=self.I[i].max()),
                    cmap = color[i])
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1

    def plot_Is(self):
        # Smoothening the image
        for i in range(self.n_ch):
            plt.figure()            
            suptitle = '%s (%s), #Frame = %d, Gaussian filtered (sigma = %d)' \
                    %(self.sample[i], self.ch[i], self.n_frame, sigma)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.Is[i,j], 
                    norm = colors.Normalize(vmin=0, vmax=self.Is[i].max()),
                    cmap = color[i])
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1

    def plot_Im1(self):
        # Masking the image
        for i in range(self.n_ch):
            plt.figure()
            suptitle = '%s (%s), #Frame = %d, Mask1 (%d %%)' \
                    %(self.sample[i], self.ch[i], self.n_frame, p1)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.Im1[i,j], 
                    norm = colors.Normalize(vmin=0, vmax=self.Im1[i].max()),
                    cmap = color[i])
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1

    def plot_Im2(self):
        # Masking the image
        for i in range(self.n_ch):
            plt.figure()
            suptitle = '%s (%s), #Frame = %d, Mask2 (%d %%)' \
                    %(self.sample[i], self.ch[i], self.n_frame, p2)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.Im2[i,j], 
                    norm = colors.Normalize(vmin=0, vmax=self.Im2[i].max()),
                    cmap = color[i])
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1

    def spatial_corr1(self):
        # Spatial correlation between two channels
        for i1 in range(self.n_ch):
            i2 = (i1+1)%self.n_ch
            plt.figure()
            suptitle = 'Spatial correlation1 between %s (%s) & %s (%s), Mask1 (%d %%)' \
            %(self.sample[i1], self.ch[i1], self.sample[i2], self.ch[i2], p1)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.Im1[i1,j]*self.Im1[i2,j], 
                    norm = colors.Normalize(vmin=0, vmax=(self.Im1[i1]*self.Im1[i2]).max()),
                    cmap = 'magma')
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1 

    def spatial_corr2(self):
        # Spatial correlation between two channels
        for i1 in range(self.n_ch):
            i2 = (i1+1)%self.n_ch
            plt.figure()
            suptitle = 'Spatial correlation2 between %s (%s) & %s (%s), Mask2 (%d %%)' \
            %(self.sample[i1], self.ch[i1], self.sample[i2], self.ch[i2], p2)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.Im2[i1,j]*self.Im2[i2,j], 
                    norm = colors.Normalize(vmin=0, vmax=(self.Im2[i1]*self.Im2[i2]).max()),
                    cmap = 'magma')
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1 
                
    def intensity_corr(self):                               
        # Intensity correlation between two channels
        for i1 in range(self.n_ch):
            i2 = (i1+1)%self.n_ch
            plt.figure()
            suptitle = 'Intensity correlation between %s (%s) & %s (%s) \n\
                        Mask1 (Black) = %d %%, Mask2 (Red) = %d %%' \
            %(self.sample[i1], self.ch[i1], self.sample[i2], self.ch[i2], p1, p2)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                mask1 = self.mask1[i1,j] & self.mask2[i2,j]
                plt.plot(self.I[i1,j,mask1], self.I[i2,j,mask1], 'k.', ms=5, alpha=0.2)
                mask2 = self.mask2[i1,j] & self.mask2[i2,j]
                plt.plot(self.I[i1,j,mask2], self.I[i2,j,mask2], 'r.', ms=5, alpha=0.2) 
                plt.axis([0, self.I[i1].max(), 0, self.I[i2].max()])   
                pcc1 = st.pearsonr(self.I[i1,j,mask1].flatten(),self.I[i2,j,mask1].flatten())            
                pcc2 = st.pearsonr(self.I[i1,j,mask2].flatten(),self.I[i2,j,mask2].flatten())    
                plt.title('# %d (pcc1 = %.2f, pcc2 = %.2f)' % (j+1, pcc1[0], pcc2[0]))
                k+=1           
               
# Start  
cell = 'cell1'
#ch = [['ch1', 'ch2', 'ch3'], ['CRACR', 'LAT', 'TCR']]
ch = [['ch1', 'ch2', 'ch3'], ['CRACR', 'LCK', 'TCR']]
data = FramePixelIntensity(cell, ch)
plt.close('all')
data.plot_all()


""" 
- 2 color overlap 50%
- binary overlap
- Intensity multiplication
- A or B (not A and B)

- changes of pcc1, pcc2 over total frames
- histogram, mean, std of pcc1, pcc2 
- pcc of multiple cells
- pcc of LAT vs LCK 
- find the centroid
- changes of moment of inertia

"""
