# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 20:41:28 2017

@author: Arslanova Linara
"""

import numpy as np

                         

 
# define the L8 channels 
CHANNELS = ['1V', '2B', '3G', '4R', '5N', '6S', '7S']



def AFVI600 (ch):
    ''' function to calculate Aerosol free vegetation index 1600 '''
    return (ch['5N'] - 0.66 + (ch['6S'] / (ch['5N'] + 0.66 * ch['6S'] )))

def ARVI(ch): # DIFFERENT FORMELS
    ''' function to calculate Atmospheric Resistant Vegetation Index '''
    return (ch['5N'] - (2.0 * ch['4R'] - ch['2B'])) / (ch['5N'] + (2.0 * ch['4R'] - ch['2B']))

def ARVI2(ch):
    ''' function to calculate Atmospheric Resistant Vegetation Index 2 '''
    return  - 0.18 + 1.17 * ((ch['5N'] - ch['4R']) / (ch['5N'] +  ch['4R']))

def AVI (ch):
    ''' function to calculate Ashburn Vegetation Index '''
    return  2 * ch['5N'] - ch['4R']

def BWDRVI(ch):
    ''' function to calculate Blue-wide dynamic range vegetation index '''
    return  0.1 * (ch['5N'] - ch['2B']) / 0.1 *(ch['5N'] +  ch['2B'])

def CHL1(ch):
    ''' function to calculate Chlorophyll 1 index '''
    return  ((1 / ch['3G']) - (1 / ch['5N']))  / ((1 / ch['3G']) + (1 / ch['5N']))                                    

def CHL2(ch):
    ''' function to calculate Chlorophyll 2 index '''
    return  ((1 / ch['4R']) - (1 / ch['5N']))  / ((1 / ch['3G']) + (1 / ch['5N']))                                    

def CHLIG(ch):
    ''' function to calculate Chlorophyll Index Green '''
    return  ch['5N'] / ch['3G'] - 1

def CHLVI(ch):
    ''' function to calculate Chlorophyll vegetation index '''
    return  ch['5N'] * (ch['4R'] / ch['3G'] * 2)

def CI(ch):
    ''' function to calculate Corrected Transformed Vegetation Index'''
    return  (ch['4R'] - ch['2B']) / ch['4R']

def CRI1(ch):
    ''' function to calculate Carotenoid Reflectance Index 1  '''
    return  (1 - ch['2B']) - (1 - ch['3G'])

def CTVI(ch):
    ''' function to calculate Corrected Transformed Vegetation Index '''
    return  ((ch['4R'] - ch['3G']) / (ch['4R'] + ch['3G']) + 0.5) / (np.abs((ch['4R'] - ch['3G']) / (ch['4R'] + ch['3G']) + 0.5)) * (np.sqrt(np.abs(((ch['4R'] - ch['3G']) / (ch['4R'] + ch['3G']) + 0.5))))

def DNG(ch):
    ''' function to calculate Difference NIR/Green'''
    return  ch['5N'] - ch['3G']

def DVI(ch):
    ''' function to calculate  Difference Vegetation Index '''
    return (ch['5N'] - ch['4R'])

def DVIMSS(ch):
    ''' function to calculate Differenced Vegetation Index MSS'''
    return  2.4 * ch['5N'] - ch['4R']

def EVI(ch):
    ''' function to calculate   Enhanced Vegetation Index  '''  
    return 2.5 * (ch['5N'] - ch['4R']) / ((ch['5N'] + 6 * ch['4R'] - 7.5 * ch['2B']) + 1)

def EVI2(ch):
    ''' function to calculate   Enhanced Vegetation Index 2 '''  #FOR HIGH BIOMASS REGIONS
    return 2.5 * (ch['5N'] - ch['4R']) / (ch['5N'] + 2.4 * ch['4R'] + 1)

def GARI(ch):
    ''' function to calculate  Green Atmospherically Resistant Vegetation Index '''
    return (ch['5N'] - (ch['3G'] - (ch['2B'] - ch['4R']))) / (ch['5N']  + (ch['3G']  - (ch['2B'] - ch['4R'])))

def GBNDVI(ch):
    ''' function to calculate Green-Blue NDVI '''
    return (ch['5N'] - (ch['3G'] + ch['2B'])) / (ch['5N'] + (ch['3G'] + ch['2B']))

def GEMI(ch):
    ''' function to calculate  Global Environmental Monitoring Index '''
    return (((2*((ch['5N'] **2)-(ch['4R'] **2)) +  1.5 * ch['5N'] + 0.5 * ch['4R']) / (ch['5N'] + ch['4R'] + 0.5)) * (1 - 0.25 * (2 *((ch['5N'] **2)-(ch['4R'] * ch['5N'])) + 1.5 * ch['5N'] + 0.5 * ch['4R']) / (ch['5N'] + ch['4R'] + 0.5))) - ( (ch['4R'] - 0.125) / (1 - ch['4R']))

def GLI(ch):
    ''' function to calculate Green leaf index '''
    return (2 * ch['3G'] - ch['4R'] - ch['2B']) / (2 * ch['3G'] + ch['4R'] + ch['2B'])

def GNDVI(ch):
    ''' function to calculate Green Normalized Difference Vegetation Index '''
    return (ch['5N'] - ch['3G']) / (ch['5N'] + ch['3G'])

def GOSAVI(ch):
    ''' function to calculate Green Optimized Soil Adjusted Vegetation Index '''
    return (ch['5N'] - ch['3G']) / (ch['5N'] + ch['3G'] + 0.16)

def GRNDVI(ch):
    ''' function to calculate Green-Red NDVI '''
    return (ch['5N'] - (ch['3G'] + ch['2B'])) / (ch['5N'] + (ch['3G'] + ch['2B']))

def GRVI1(ch):
    ''' function to calculate Green-red Vegetation Index 1'''
    return ((ch['5N'] + 0.1 ) - (ch['7S'] + 0.02)) / ((ch['5N'] + 0.1 ) + (ch['7S'] + 0.02))

def GSAVI(ch):
    ''' function to calculate Green Soil Adjusted Vegetation Index '''
    return (ch['5N'] - ch['3G']) / (ch['5N'] + ch['3G'] + 0.5) * (1 + 0.5)

def GVI (ch):
    ''' function to calculate Green Vegetation Index  '''
    return ( -0.2848 * ch['2B'] - 0.2435 * ch['3G'] - 0.5436 * ch['4R'] + 0.7243 * ch['5N'] + 0.0840 * ch['5N'] - 0.1800 * ch['7S'])

def GVMI(ch):
    ''' function to calculate Global Vegetation Moisture Index '''
    return (ch['4R'] - ch['3G'])/(ch['4R'] + ch['3G'])

def HUE(ch):
    ''' function to calculate Hue '''
    return np.arctan(2 + ch['4R'] - (ch['3G'] - ch['2B'])) / 30.5 * (ch['3G'] - ch['2B'])

def INTENSITY(ch):
    ''' function to calculate Intensity '''
    return (1 / 30.5) * (ch['4R'] + ch['3G'] + ch['2B'])

def IPVI(ch):
    ''' function to calculate Infrared Percentage Vegetation Index '''
    return ch['5N'] / (ch['5N'] + ch['4R']) / 2 * ((ch['4R'] - ch['3G']) / (ch['4R'] + ch['3G']) +1)

def LAI_SAVI(ch):
    ''' function to calculate Leaf Area Index - Soil Adjusted Vegetation Index '''
    return -(np.log1p(0.371 + 1.5 * (ch['5N'] - ch['4R'])/(ch['5N'] + ch['4R'] + 0.5))) / 2.4

def MIVI(ch):
    ''' function to calculate Mid-infrared vegetation index '''
    return ch['5N'] /ch['7S'] 

def MSAVI(ch):
    ''' function to calculate Modified Soil Adjusted Vegetation Index '''
    return (2 * ch['5N'] + 1 - np.sqrt((2 * ch['5N'] + 1) ** 2 - 8 * (ch['5N'] - ch['4R'])))/2

def MSI(ch):
    ''' function to calculate Moisture Stress Index '''
    return (ch['6S'] / ch['5N'])

def MSR(ch):
    ''' function to calculate Modified Simple Ratio NIR/RED '''
    return (ch['5N'] /ch['4R'] - 1) / np.sqrt(ch['5N'] / ch['4R'] + 1)

def NDGRINBLUE(ch):
    ''' function to calculate Normalized Difference 550/450 '''
    return  (ch['3G'] - ch['2B']) / (ch['3G'] + ch['2B'])

def NDGRINRED(ch):
    ''' function to calculate Normalized Difference 550/650 '''
    return  (ch['3G'] - ch['4R']) / (ch['3G'] + ch['4R'])

def NDNIRBLUE(ch):
    ''' function to calculate Normalized Difference NIR/Blue '''
    return  (ch['5N'] - ch['2B']) / (ch['5N'] + ch['2B'])

def NDNIRGREEN(ch):
    ''' function to calculate Normalized Difference NIR/Green '''
    return  (ch['5N'] - ch['3G']) / (ch['5N'] + ch['3G'])

def NDNIRSWIR1(ch):
    ''' function to calculate Normalized Difference 860/1640 '''
    return  (ch['5N'] - ch['6S']) / (ch['5N'] + ch['6S'])

def NDNIRSWIR2(ch):
    ''' function to calculate Normalized Difference NIR/MIR '''
    return  (ch['5N'] - ch['7S']) / (ch['5N'] + ch['7S'])
                                      
def NDREDGREEN(ch):
    ''' function to calculate Normalized Difference Red/Green '''
    return  (ch['4R'] - ch['3G']) / (ch['4R'] + ch['3G'])

def NDVI(ch):
    ''' function to calculate Normalized Difference Vegetation Index '''
    return (ch['5N'] - ch['4R']) / (ch['5N']  + ch['4R'])

def NDVIREDBLUE(ch):
    ''' function to calculate Red-Blue NDVI'''
    return (ch['5N'] - (ch['4R'] + ch['2B'])) / (ch['5N'] + (ch['4R'] + ch['2B']))

def NDWI(ch):
    ''' function to calculate Normalized Difference Water Index '''
    return (ch['3G'] - ch['5N']) /(ch['3G'] + ch['5N'])

def NG(ch):
    ''' function to calculate Norm G'''
    return  ch['3G'] / (ch['5N'] + ch['4R']  + ch['3G'])

def NNIR(ch):
    ''' function to calculate Norm NIR'''
    return  ch['5N'] / (ch['5N'] + ch['4R']  + ch['3G'])

def NR(ch):
    ''' function to calculate Norm R'''
    return  ch['4R'] / (ch['5N'] + ch['4R']  + ch['3G'])

def OSAVI(ch):
    ''' function to calculate Optimised Soil Adjusted Vegetation Index '''
    return (1.0 + 0.16) * (ch['5N'] - ch['4R']) / (ch['5N'] + ch['4R'] + 0.16)                                    

def PANNDVI(ch):
    ''' function to calculate Pan NDVI'''
    return (ch['5N'] - (ch['3G'] + ch['4R'] + ch['2B'])) / (ch['5N'] + (ch['3G'] + ch['4R'] + ch['2B']))         

def PSIR_NIR(ch):
    ''' function to calculate Plant Senescence Reflectance Index-Near Infra-red '''
    return (ch['4R'] - ch['2B']) / ch['5N']        

def RDVI(ch):
    ''' function to calculate Renormalized difference vegetation index '''
    return np.sqrt((ch['5N'] - ch['4R']) / (ch['5N'] + ch['4R']) * (ch['5N'] + ch['4R']))
                                                    
def SARVI2(ch):
    ''' function to calculate Soil and Atmospherically Resistant Vegetation Index 2 '''
    return 2.5 * (ch['5N'] - ch['4R']) / (1 + ch['5N'] + 6 * ch['4R'] - 7.5 * ch['3G'])

def SHPINDEX(ch):
    ''' function to calculate Shape Index '''
    return (2 * ch['4R'] - ch['3G'] - ch['2B']) / (ch['3G'] - ch['2B'])  

def SIPI(ch):
    ''' function to calculate Structure Intensive Pigment Index '''
    return (ch['5N'] - ch['1V']) / (ch['5N'] - ch['4R'])

def SLAVI(ch):
    ''' function to calculate Specific Leaf Area Vegetation Index '''
    return ch['5N'] / (ch['4R'] + ch['7S'])

def SRCOASTGREEN(ch):
    ''' function to calculate Simple Ratio 450/550 '''
    return (ch['1V'] / ch['3G'])

def SRNIRGRIN(ch):
    ''' function to calculate Simple Ratio NIR/GREEN '''
    return (ch['5N'] / ch['3G'])

def SRGRINRED(ch):
    ''' function to calculate Simple Ratio 550/670 '''
    return (ch['3G'] / ch['4R'])

def SRNIRSWIR2(ch):
    ''' function to calculate Simple Ratio NIR/MIR '''
    return (ch['5N'] / ch['7S'])
                                 
def SRNIRGREEN(ch):
    ''' function to calculate Simple Ratio NIR/G '''
    return (ch['7S'] / ch['3G'])
                                      
def SRNIRRED(ch):
    ''' function to calculate Simple Ratio NIR/RED '''
    return (ch['5N'] / ch['4R'])                           

def SRREDGREEN(ch):
    ''' function to calculate Simple Ratio Red/Green '''
    return (ch['4R'] / ch['3G'])

def SRREDNIR(ch):
    ''' function to calculate Simple Ratio Red/NIR '''
    return (ch['4R'] / ch['5N'])

def SRSWIR(ch):
    ''' function to calculate Simple Ratio MIR/NIR '''
    return (ch['7S'] / ch['5N'])                                     

def SRSWIRRED(ch):
    ''' function to calculate Simple Ratio MIR/Red '''
    return (ch['7S'] / ch['4R'])
                   
#def TCB(ch):
#    ''' function to calculate Tasselled Cap - brightness '''
#    return 0.3037 * ch['2B'] + 0.2793 * ch['3G']  + 0.4743 * ch['4R']  + 0.5585 * ch['5N']  + 0.5052 * ch['9C']  +0.1863 * ch['7S'] 

def TCV(ch):
    ''' function to calculate Tasselled Cap - vegetation '''
    return -0.2848 * ch['2B'] - 0.2435 * ch['3G']  - 0.5436 * ch['4R']  + 0.7243 * ch['5N']  + 0.0840 * ch['6S']  - 0.1800 * ch['7S'] 
                                      
def TCW(ch):
    ''' function to calculate Tasselled Cap - wetness '''
    return 0.1509 * ch['2B'] - 0.1973 * ch['3G']  - 0.3279 * ch['4R']  + 0.3406* ch['5N']  + 0.7112 * ch['6S']  - 0.4572 * ch['7S'] 
                                               
def TVI(ch):
    ''' function to calculate Transformed Vegetation Index '''
    return np.sqrt((ch['4R'] - ch['3G']) / (ch['4R'] + ch['3G']) + 0.5)

def VARIG(ch):
    ''' function to calculate Visible Atmospherically Resistant Index Green '''
    return (ch['3G'] - ch['4R']) / (ch['3G'] + ch['4R'] - ch['2B'])

def WDRVI(ch):
    ''' function to calculate Wide Dynamic Range Vegetation Index '''
    return (0.1 * ch['5N'] - ch['4R']) / (0.1 * ch['5N'] + ch['4R'])











 


 
