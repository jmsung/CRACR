"""
Analysis of CRACR data from Yuxiao

class Data() 
- path, data_name, load(), sample_list[], sample_num, samples = [Sample()], plot()

class Sample() 
- sample_name, cell_list[], cell_num, cells = [Cell()]

class Cell() 
- cell_name, intensity[array], analysis(), 

"""

from __future__ import division, print_function, absolute_import
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

color = 'magma'

class Cell(object):
    def __init__(self, cell_name, sample_path):
        self.cell_name = cell_name
        self.cell_path = sample_path + '\\' + cell_name   
        self.intensity = np.array(Image.open(self.cell_path))

class Sample(object):
    def __init__(self, sample_name, data_path):
        self.sample_name = sample_name
        self.sample_path = data_path + '\\' + sample_name
        self.cell_list = os.listdir(self.sample_path)
        self.cell_num = len(self.cell_list)
        self.cells = []   
        for cell_name in self.cell_list:
            cell = Cell(cell_name, self.sample_path)
            self.cells.append(cell)

class Data(object):
    def __init__(self):
        self.data_path = os.getcwd()
        path_split = self.data_path.split('\\')
        self.data_name = path_split[len(path_split)-1]
        self.sample_list = os.listdir(self.data_path) 
        self.sample_num = len(self.sample_list)
        self.samples = []   
        for sample_name in self.sample_list:
            sample = Sample(sample_name, self.data_path)
            self.samples.append(sample)
                        
    def plot(self):
        plt.close('all')
        for i in range(self.sample_num):
            plt.figure(self.sample_list[i])
            sample = self.samples[i]
            cell_num = sample.cell_num
            for j in range(cell_num):
                row = np.floor((cell_num/1.5)**0.5)
                col = np.ceil(cell_num/row)
                plt.subplot(row, col, j+1)
                cell = sample.cells[j]
                plt.imshow(cell.intensity, color)
                plt.title(cell.cell_name[-8:-4])
            plt.subplots_adjust(wspace=0.3, hspace=0.3)
        plt.show()
                      
                          
# Start  
data = Data()
data.plot()