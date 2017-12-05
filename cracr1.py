# Analysis of CRACR data from Yuxiao

from __future__ import division, print_function, absolute_import
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

class CRACR(object):
    def __init__(self):
        self.path = os.getcwd()
        self.path_split = self.path.split('\\')
        self.data_name = self.path_split[len(self.path_split)-1]
        
    def load(self):
        self.sample_list = os.listdir(self.path)
        self.samples = []
        
        for self.sample_name in self.sample_list:
            self.cell_list = os.listdir(self.path+'\\'+self.sample_name)
            self.cells = []
            
            for self.cell_name in self.cell_list:
                file_to_load = self.path+'\\'+self.sample_name+'\\'+self.cell_name
                img = np.array(Image.open(file_to_load))
                self.cells.append(img)
            self.samples.append(self.cells)
            
    def plot(self):
        for i in range(len(self.samples)):
            plt.figure(i)
            for j in range(len(self.samples[i])):
                plt.subplot(2, np.ceil(len(self.samples[i])/2), j+1)
                plt.imshow(self.samples[i][j])
        plt.show()
        
                

# Start  
data = CRACR()
data.load()
data.plot()