# Analysis of CRACR data from Yuxiao

from __future__ import division, print_function, absolute_import
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os


class Data(object):
    def __init__(self):
        self.path = os.getcwd()
        self.path_split = self.path.split('\\')
        self.data_name = self.path_split[len(self.path_split)-1]
        
    def load(self):
        self.sample_list = os.listdir(self.path) # list[sample1, sample2]
        self.samples = []
        
        for self.sample_name in self.sample_list:
            self.cell_list = os.listdir(self.path+'\\'+self.sample_name)
            self.cells = []
            
            for self.cell_name in self.cell_list:
                Cell(self.cell_name)
                file_name = self.path+'\\'+self.sample_name+'\\'+self.cell_name
                
                img = np.array(Image.open(file_name))
                self.cells.append(img)
            self.samples.append(self.cells)
            
    def plot(self):
        color = 'magma'
        plt.close('all')
        for i in range(len(self.samples)):
            plt.figure(i)
            cell_num = len(self.samples[i])
            for j in range(cell_num):
                plt.subplot(np.floor(cell_num**0.5), np.ceil(cell_num/np.floor(cell_num**0.5)), j+1)
                plt.imshow(self.samples[i][j], color)
        plt.show()
        
class Cell(object):
    def __init__(self):
        pass
                

# Start  
data = Data()
data.load()
data.plot()