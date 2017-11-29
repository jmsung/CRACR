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
import scipy.stats as st
colors = ['Blues', 'Greens', 'Reds']

class FramePixelIntensity(object):
    def __init__(self, cell, ch):
        name = cell+'.tif'
        movie = Image.open(name)
        self.sample = ch[1]
        self.n_ch = len(ch[0])
        self.n_frame = int((movie.n_frames)/self.n_ch)
        self.width = movie.width
        self.height = movie.height
        
        # I[channel,frame,row,column]         
        self.I = np.zeros((self.n_ch,self.n_frame,self.height,self.width),dtype=int) 
        for i in range(self.n_ch): # ith channel
            movie_i = Image.open(cell+'-'+ch[0][i]+'.tif')      
            for j in range(self.n_frame): # jth frame
                movie_i.seek(j) 
                I0 = np.array(movie_i, dtype=int)
                self.I[i,j] = I0 - I0.min()
                
    def plot_all(self):
        step = 10
        row = 3 
              
        for i in range(self.n_ch):
            plt.figure()
            suptitle = 'Ch %d, %s, #Frame = %d' \
                    %(i+1, self.sample[i], self.n_frame)
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.I[i,j], colors[i])
                plt.title('# %d' % (j+1))
                k+=1

        for i in range(self.n_ch):
            plt.figure()
            suptitle = 'Colocalization of %s & %s' \
                        %(self.sample[i], self.sample[(i+1)%self.n_ch])
            plt.suptitle(suptitle)
            k = 1
            for j in range(0,self.n_frame,step):
                plt.subplot(row, np.ceil(self.n_frame/row/step),k)
                plt.imshow(self.I[i,j], colors[i])
                plt.title('# %d' % (j+1))
                k+=1                
                
        plt.show()
        
"""                    
    def plot_all(self):
        frames = range(self.n_frame)
        frames = range(3,4)
        frame_display = 0
        for i in frames:
            self.movie.seek(i)
            im
            
            I1 = I[:,:,0] - I[:,:,0].min()
            I2 = I[:,:,1] - I[:,:,1].min()
            I12 = I1*I2; 

#            if i = frame_display: 
            plt.figure(i+1); plt.title('Frame %d' %i) 
            col = 5
            for j in range(3):
                plt.subplot(3,col,col*j+1); plt.imshow(In[j], colors[j])
                plt.subplot(3,col,col*j+2); plt.imshow(I12[j], 'plasma'); plt.colorbar()
                plt.subplot(3,col,col*j+3); plt.plot(In[j],In[(j+1)%3],'k.',ms=1)
                pcc = st.pearsonr(In[j].flatten(),In[(j+1)%3].flatten())
                plt.title('pcc = %.3f' %(pcc[0]))
                plt.subplot(3,col,col*j+4); plt.imshow(Imn[j]**2, 'plasma'); plt.colorbar()
                plt.subplot(3,col,col*j+5); plt.plot(In[j]**2,In[(j+1)%3]**2,'k.',ms=1)

        plt.show()
"""    

# Start  
cell = 'cell1'
ch = [['ch1', 'ch2', 'ch3'],
      ['CRACR', 'LCK', 'TCR']]
data = FramePixelIntensity(cell, ch)
plt.close('all')
data.plot_all()


"""
To-do
- remove repetition by making a function   
- mask for cell (inside membrane)
- threshold and set zero for low values

- plot I1/I2/I3 of first 10 frames 
- plot I12/I23/I31 of first 10 frames
- plot I1 vs I2 of first 10 frames
- pcc of 12, 23, 31
- changes of pcc over frames
- pcc of multiple cells
- pcc of LAT vs LCK 
- find the centroid
- changes of moment of inertia

"""
