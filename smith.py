#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 17:28:26 2021

@author: mseb
"""

import numpy as np
from bokeh.plotting import figure,output_file, show
from bokeh.io import curdoc

class smith:
    """
    Simple Smith Chart drawing.
    """

    def __init__(self, Z0=50, chartSize=850):
        """
        Creates the figure and draws the grid.
        Z0: characteristic impedance | Default: 50 Ohms
        chartSize: Height/Width of the chart | Default: 850 px
        """
        self.Z0 = Z0
        fig1Title = f'Characteristic Impedance: {Z0} Ohms'
        curdoc().theme = 'dark_minimal'
        self.smithChart = figure(title=fig1Title,plot_width=chartSize,plot_height=chartSize,tooltips=[('Parte real','@xcoord'),('Parte imaginaria','@ycoord'),('Impedancia','@zimp')])
        self.smithChart.toolbar.active_drag = None
        self.smithChart.x_range.range_padding = self.smithChart.y_range.range_padding = 0
        self.smithChart.grid.grid_line_width = 0
        self.drawGrid()
        self.smithChart.xaxis.major_tick_line_color = None
        self.smithChart.xaxis.minor_tick_line_color = None
        self.smithChart.yaxis.major_tick_line_color = None
        self.smithChart.yaxis.minor_tick_line_color = None
        self.smithChart.axis.visible = False
        
    def drawZList(self, l, c='b'):
        """
        Draws a list of impedances on the chart and connects them by lines. 
        To get a closed contour, the last impedance should be the same as the 
        first one. Use color c for the drawing.
        """
        xlst = [self.z2gamma(z).real for z in l]
        ylst = [self.z2gamma(z).imag for z in l]
        smithXCoord = [f'{round(z.real/self.Z0,2)}' for z in l] 
        smithYCoord = [f'{round(z.imag/self.Z0,2)}j' for z in l] 
        imped = [f'{round(z.real,2)}' + ('+' if (z.imag>=0) else '-') + f'{abs(round(z.imag,2))}j' for z in l]
        source = dict(
                xlst = xlst,
                ylst = ylst,
                zimp = imped,
                xcoord = smithXCoord,
                ycoord = smithYCoord
            )
        self.smithChart.line(source=source,x='xlst',y='ylst',line_width=0.5)

        
    def drawXCircle(self, x, npts=500):
        """
        Draws a circle with constant real part.
        """
        zlst = [x]+[complex(x, z) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, 'k')
        zlst = [x]+[complex(x, -z) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, 'k')

    def drawYCircle(self, y, npts=500):
        """
        Draws a circle with constant imaginary part.
        """
        zlst = [complex(0, y)]+[complex(z, y) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, 'k')
        
    def manualValues(self):
        """
        Make it look like the old school Smith
        Creates an array of values with those resolutions
        
        Interval | First Value | Last Value | Resolution
        1        | 0           | 0.2        | 0.01
        2        | 0.2         | 0.5        | 0.02
        3        | 0.5         | 1          | 0.05
        4        | 1           | 5          | 0.2
        5        | 5           | 10         | 1
        6        | 10          | 20         | 2
        7        | 20          | 50         | 10
        """
        
        self.gridValues = np.arange(0,0.21,0.01)
        self.gridValues = np.concatenate((self.gridValues,np.arange(0.2,0.52,0.02)))
        self.gridValues = np.concatenate((self.gridValues,np.arange(0.55,1.05,0.05)))
        self.gridValues = np.concatenate((self.gridValues,np.arange(1.2,5.2,0.2)))
        self.gridValues = np.concatenate((self.gridValues,np.arange(6,10,1)))
        self.gridValues = np.concatenate((self.gridValues,np.arange(10,22,2)))
        self.gridValues = np.concatenate((self.gridValues,np.arange(30,60,10)))
        
    def drawGrid(self):
        """
        Draws the Smith Chart grid.
        """
        self.manualValues()
        for i in self.gridValues:
            self.drawXCircle(i*self.Z0)
            self.drawYCircle(i*self.Z0)
            if i > 0:
                self.drawYCircle(-i*self.Z0)
        
    def markZ(self, z, c='red', size=7):
        """
        Marks an impedance with a dot.
        """
        g = self.z2gamma(z)   
        data = dict(
            x = [g.real],
            y = [g.imag],
            xcoord = [f'{round(z.real/self.Z0,2)}'],
            ycoord = [f'{round(z.imag/self.Z0,2)}j'],
            zimp = [f'{round(z.real,2)}+{round(z.imag,2)}j']
            )
        self.smithChart.circle(source = data,x='x',y='y', fill_color=c, line_width=0, size = size)
        
    def markZarray(self, z, c='white'):
        """
        Marks an array impedance with a line.
        """
        data = dict(
            x = [self.z2gamma(l).real for l in z],
            y = [self.z2gamma(l).imag for l in z],
            xcoord = [f'{round(j.real/self.Z0,2)}' for j in z],
            ycoord = [f'{round(j.imag/self.Z0,2)}j' for j in z],
            zimp = [f'{round(j.real,2)}+{round(j.imag,2)}j' for j in z]
            )
        self.smithChart.line(source = data,x='x',y='y', color=c, line_width=1.25)

    def z2gamma(self, zl):
        """
        Converts an impedance to a reflection coefficient.
        """
        return complex(zl-self.Z0)/(zl+self.Z0)       
                    
    def save(self, filename = 'smithChart'):
        """
        Saves the plot to filename. The extension defines the filetype.
        """
        output_file(filename+'.html', title="Smith Chart")
        show(self.smithChart)

if __name__ == '__main__':
    smith = smith()
    smith.markZ(20+30j)
    smith.markZ(2-30j)
    smith.markZarray(np.array([20+30j,20+35j,15+20j,10+5j]))
    smith.save()