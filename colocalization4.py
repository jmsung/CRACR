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
import scipy.stats as st
color = ['Blues', 'Greens', 'Reds']
#color = ['magma']*3
sigma = 1.0
step = 1
row = 2
p1 = 60
p2 = 80

class FramePixelIntensity(object):
    def __init__(self, cell, ch):
        self.name = cell
        movie = Image.open(self.name+'.tif')
        self.ch = ch[0]
        self.sample = ch[1]
        self.n_ch = len(ch[0])
        self.n_frame = int((movie.n_frames)/self.n_ch)
        self.width = movie.width
        self.height = movie.height
        
        # I[channel,frame,row,column]         
        self.I = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=float) 
        self.Is = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=float)  
        self.mask1 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=bool)
        self.mask2 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=bool)
        self.Im1 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=float)  
        self.Im2 = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=float) 
        self.pcc1 = np.zeros((self.n_ch,self.n_frame),dtype=float)    
        self.pcc2 = np.zeros((self.n_ch,self.n_frame),dtype=float)       
      
        # Read data from each channel
        for i in range(self.n_ch): 
            movie_i = Image.open(cell+'-'+ch[0][i]+'.tif')   
            # Read data from each frame   
            for j in range(self.n_frame): 
                movie_i.seek(j) # Move to frame j
                I0 = np.array(movie_i, dtype=float)
                self.I[i,j] = I0 - I0.min()
                self.Is[i,j] = gf(self.I[i,j], sigma)
                               
        # Normalize signal from each channel 
        for i in range(self.n_ch):
            Imax = self.I[i].max()
            self.I[i] = self.I[i] / Imax
            self.Is[i] = self.Is[i] / Imax
                    
        # Masking to find cell boundary and clusters
        for j in range(self.n_frame): # Each frame
            for i in range(self.n_ch): # Each channel
                # Mask1 to find a cell from ch2 (because LAT/LCK are more uniformly spread)
                m1 = self.Is[1,j] > np.percentile(self.Is[1,j], p1)                 
                self.mask1[i,j] = m1
                self.Im1[i,j,m1] = self.I[i,j,m1]
                # Mask2 to find clusters within the cell boundary
                self.mask2[i,j,m1] = self.Is[i,j,m1] > np.percentile(self.Is[i,j,m1], p2)
                self.Im2[i,j,self.mask2[i,j]] = self.I[i,j,self.mask2[i,j]]    
                i1 = i; i2 = (i1+1)%self.n_ch    
                self.pcc1[i,j] = st.pearsonr(self.I[i1,j,m1].flatten(),self.I[i2,j,m1].flatten())[0] 

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
                plt.imshow(self.I[i,j], color[i])
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
                plt.imshow(self.Is[i,j], color[i])
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
                plt.imshow(self.Im1[i,j], color[i])
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
                plt.imshow(self.Im2[i,j], color[i])
                plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1

    def overlay(self):
        # Spatial correlation between two channels
        for i1 in range(self.n_ch):
            i2 = (i1+1)%self.n_ch
            plt.figure()
            suptitle = 'Overlay between %s (%s, B) & %s (%s, R), Mask2 (%d %%)' \
                %(self.sample[i1], self.ch[i1], self.sample[i2], self.ch[i2], p2)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.Im2[i1,j], 'Blues', alpha=0.8), plt.colorbar()             
                plt.imshow(self.Im2[i2,j], 'Reds', alpha=0.3), plt.colorbar()
                plt.title('# %d' % (j+1))
                k+=1 
                             
    def intensity_corr(self):                               
        # Intensity correlation between two channels
        for i1 in range(self.n_ch):
            i2 = (i1+1)%self.n_ch
            plt.figure()
            suptitle = 'Intensity correlation between %s (%s, B) & %s (%s, R)\n'\
                       'Mask1 (%d %%), Mask2 (%d %%) ' \
            %(self.sample[i1], self.ch[i1], self.sample[i2], self.ch[i2], p1, p2)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                mask1 = self.mask1[i1,j] | self.mask1[i1,j]
                mask2 = self.mask2[i1,j] | self.mask2[i2,j]
                plt.plot(self.I[i1,j,mask1], self.I[i2,j,mask1], 'k.', ms=2, alpha=0.1)
                plt.plot(self.I[i1,j,mask2], self.I[i2,j,mask2], 'r.', ms=4, alpha=0.1) 
                plt.axis([0, self.I[i1].max(), 0, self.I[i2].max()])   
                pcc1 = st.pearsonr(self.I[i1,j,mask1].flatten(),self.I[i2,j,mask1].flatten())            
                pcc2 = st.pearsonr(self.I[i1,j,mask2].flatten(),self.I[i2,j,mask2].flatten())   
                self.pcc2[i1,j] = pcc2[0] 
                plt.title('# %d (pcc1 = %.2f, pcc2 = %.2f)' % (j+1, pcc1[0], pcc2[0]))
                k+=1  
                
    def plot_pcc(self):
        plt.figure()
        suptitle = '%s & %s, %s, pcc' % (self.sample[0], self.sample[1], self.name)
        plt.suptitle(suptitle)
        for i in range(self.n_ch):
            title1 = 'pcc1 = %.2f +- %.2f (min = %.2f)'\
                    % (self.pcc1[i].mean(), self.pcc1[i].std(), self.pcc1[i].min())
            title2 = 'pcc2 = %.2f +- %.2f (min = %.2f)'\
                    % (self.pcc2[i].mean(), self.pcc2[i].std(), self.pcc2[i].min())
            plt.subplot(2,3,i+1), plt.plot(self.pcc1[i]), plt.title(title1)
            plt.subplot(2,3,i+4), plt.plot(self.pcc2[i]), plt.title(title2)
                                                                                                                                    
    def plot_all(self):
#        self.plot_I()
#        self.plot_Is()
#        self.plot_Im1()
#        self.plot_Im2()
#        self.overlay()
        self.intensity_corr()
        self.plot_pcc()
        plt.show()                  
               
# Start  
cell = 'cell2'
ch = [['ch1', 'ch2', 'ch3'], ['CRACR', 'LAT', 'TCR']]
#ch = [['ch1', 'ch2', 'ch3'], ['CRACR', 'LCK', 'TCR']]
data = FramePixelIntensity(cell, ch)
plt.close('all')
data.plot_all()


"""
- changes of pcc1, pcc2 over total frames
- histogram, mean, std of pcc1, pcc2 
- pcc of multiple cells
- pcc of LAT vs LCK 
- Auto/Cross-correlation with timelag
- find the centroid
- changes of moment of inertia

"""
