#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:18:25 2022

@author: tom

REF2021 plots

#Uses conda env in environment.yml
conda env create --name munge --file environment.yml

#export conda env with 
conda env export > environment.yml



#download ref spreadsheet from 
https://results2021.ref.ac.uk/profiles/export-all

"""

SAVEENV = False #toggle, export conda environment

#set up environment

import socket #to get host machine identity
import os #file and folder functions
import numpy as np #number function
import pandas as pd #dataframes!
import matplotlib.pyplot as plt #plotting function
#matplotlib named colours https://matplotlib.org/stable/gallery/color/named_colors.html
import squarify #treeplots
import seaborn as sns #fancy plots
from matplotlib import cm #making colour maps

print("identifying host machine")
#test which machine we are on and set working directory
if 'tom' in socket.gethostname():
    os.chdir('/home/tom/t.stafford@sheffield.ac.uk/A_UNIVERSITY/toys/ref2021')
else:
    print("Running in expected location, we are in :" + os.getcwd())
    print("Maybe the script will run anyway...")
    
#export environment in which this was last run
if SAVEENV:
    os.system('conda env export > environment2.yml') 
    
def UoAshort(inval):
    '''replace UoA names with a short version'''
    if inval=='Agriculture, Food and Veterinary Sciences':
        return 'Agriculture'
    if inval=='Allied Health Professions, Dentistry, Nursing and Pharmacy':
        return 'Allied\nHealth'
    if inval=='Anthropology and Development Studies':
        return 'Anthropology'
    if inval=='Architecture, Built Environment and Planning':
        return 'Architecture'
    if inval=='Art and Design: History, Practice and Theory':
        return 'Art &\nDesign' 
    if inval=='Biological Sciences':
        return 'Biology'    
    if inval=='Business and Management Studies':
        return 'Business &\n Management'
    if inval=='Communication, Cultural and Media Studies, Library and Information Management':
        return 'Media\nStudies'
    if inval=='Computer Science and Informatics':
        return 'Computer\nScience'
    if inval=='Clinical Medicine':
        return 'Clinical\nMedicine'
    if inval=='Earth Systems and Environmental Sciences':
        return 'Env. Science'
    if inval=='Economics and Econometrics':
        return 'Economics'
    if inval=='English Language and Literature':
        return 'English'
    if inval=='Geography and Environmental Studies':
        return 'Geography'
    if inval=='Mathematical Sciences':
        return 'Maths'
    if inval=='Modern Languages and Linguistics':
        return 'Languages &\nLinguistics'
    if inval=='Music, Drama, Dance, Performing Arts, Film and Screen Studies':
        return 'Performing\nArts'
    if inval=='Politics and International Studies':
        return 'Politics'
    if inval=='Psychology, Psychiatry and Neuroscience':
        return 'Psychology'
    if inval=='Public Health, Health Services and Primary Care':
        return 'Public\nHealth'
    if inval=='Social Work and Social Policy':
        return 'Social\nWork'
    if inval=='Sport and Exercise Sciences, Leisure and Tourism':
        return 'Sport\nSciences'
    if inval=='Theology and Religious Studies':
        return 'Theology'
    else:
        return inval
    
def instshort(inval):
    '''replace institution names with a short version'''
    if inval=='Anglia Ruskin University Higher Education Corporation':
        return 'Anglia Ruskin University'
    if inval=='University of South Wales / Prifysgol De Cymru':
        return 'University of South Wales'
    if inval=='Institute of Cancer Research: Royal Cancer Hospital (The)':
        return 'Institute of Cancer Research'    
    if inval=='Imperial College of Science, Technology and Medicine':
        return 'Imperial College'
    if inval=='The London School of Economics and Political Science':
        return 'LSE'
    if inval=='London School of Hygiene and Tropical Medicine':
        return 'LSHTM'
    if inval=='Swansea University / Prifysgol Abertawe':
        return 'Swansea University'
    if inval=='Trinity Laban Conservatoire of Music and Dance':
        return 'Trinity Laban Conservatoire'
    if inval=='University of Wales Trinity Saint David / Prifysgol Cymru Y Drindod Dewi Sant':
        return 'Trinity Saint David'
    if inval=='Cardiff Metropolitan University / Prifysgol Metropolitan Caerdydd':
        return 'Cardiff Metropolitan University'
    if inval=='Cardiff University / Prifysgol Caerdydd':
        return 'Cardiff University'
    if inval=='Wrexham Glyndŵr University / Prifysgol Glyndŵr Wrecsam':
        return 'Wrexham Glyndŵr University'
    else:
        return inval
    
    
#get data    
filename='REF 2021 Results - All - 2022-05-06.xlsx'

df= pd.read_excel(filename,skiprows=6)

    #4* "world leading'
    #3* 'internationally excellent'

#calculate GPA    
df['GPA']=pd.to_numeric(df['4*'],errors='coerce').fillna(0)/100*4+pd.to_numeric(df['3*'],errors='coerce').fillna(0)/100*3+pd.to_numeric(df['2*'],errors='coerce').fillna(0)/100*2+pd.to_numeric(df['1*'],errors='coerce').fillna(0)/100*1

#show total FTE per institution - max= oxford with 3404.62
df[df['Profile']=='Overall'].groupby('Institution name')['FTE of submitted staff'].sum().sort_values()

maxFTE=3404.62

profile='Overall'

#make plot for each individual institution
for place in df['Institution name'].unique():
    print(place)

    #place='The University of Sheffield';shortplace='Sheffield'
    #place='University of Southampton';shortplace='Southampton'
    #place='The University of Bradford';shortplace='Bradford'
    #place='Sheffield Hallam University';shortplace='Hallam'
    #place='University of Oxford';shortplace='Oxford'
    
    mask=(df['Institution name']==place) & (df['Profile']==profile)
    

    
    #get FTE for that place
    placeFTE=df[(df['Profile']=='Overall') & (df['Institution name']==place)]['FTE of submitted staff'].sum()
 
    #unique code for filename
    shortplace=str(int(df[mask]['Institution sort order'].unique())) #number code as string
    shortplace=str(int(placeFTE)).zfill(4)+'_'+shortplace
    
    #fontsize for labels
    fsize=(placeFTE/maxFTE)*12
    if fsize<5:
        fsize=5
    if place == 'University of Oxford':
        fsize=9
        
    #extract institution data for plotting data frame (pf)    
    pf=df[mask]
    pf.sort_values('FTE of submitted staff', ascending=False, inplace=True)
    
    
    #this helped
    #https://towardsdatascience.com/professional-treemaps-in-python-how-to-customize-matplotlib-squarify-efd5dc4c8755
    
    #define colourmap for GPAs
    cmap = cm.get_cmap('hot') #function converts 0 to 1 to a colour
    #https://matplotlib.org/3.5.0/tutorials/colors/colormaps.html
    
    def gpa_to_colour(input):
        return (input-2.5)/1.5
    
    
    #plot parameters
    sizes= pf['FTE of submitted staff'].values# proportions of the categories
    label=pf['Unit of assessment name'].apply(UoAshort)
    gpas=pf['GPA'].values
    
    
    #we scale the plot so that the max size reflects the Oxford FTE
    
    maxdim=np.sqrt(maxFTE/placeFTE*(100**2)) 
    
    mapped_list = [cmap(gpa_to_colour(gpa)) for gpa in gpas]
    
    bboxwidth=3
    
    #make plot!
    plt.clf()
    sns.set_style(style="white") # set seaborn plot style
    
    #draw bounding box
    plt.plot([0,0],[maxdim,0],color='k',lw=bboxwidth)
    plt.plot([maxdim,0],[maxdim,maxdim],color='k',lw=bboxwidth)
    plt.plot([maxdim,maxdim],[0,maxdim],color='k',lw=bboxwidth)
    plt.plot([0,maxdim],[0,0],color='k',lw=bboxwidth)
    
    #fill colour
    plt.fill([0, maxdim, maxdim, 0],[0,0,maxdim,maxdim],'lightgray')
    
    #instutitonal treemap
    squarify.plot(sizes=sizes, label=label[:21], alpha=0.6,color=mapped_list,text_kwargs={'fontsize': fsize, 'rotation': 25})
    #  put name of place on plot
    annotext=instshort(place)+' ('+str(int(placeFTE))+' FTE)'
    plt.title(annotext)
     
    #plt.annotate(annotext, (5,105),fontsize=fsize*2)
    annotext='University of Oxford (3404 FTE)'   
    if place != 'University of Oxford':
        plt.annotate(annotext, (maxdim*0.94,maxdim*0.12),fontsize=10,rotation=270)
    #else:
        #plt.annotate(annotext, (maxdim*0.12,maxdim*1.04),fontsize=fsize*2)
        
    #scale to size of Oxford - this needs to come after the rest
    plt.xlim([-bboxwidth,maxdim+bboxwidth])
    plt.ylim([-bboxwidth,maxdim+bboxwidth])
    plt.axis('off')
    
    
    
    #caption at bottom
    txt='Area scaled to FTE of that UoA, colour scaled to Overall GPA\nGrey box is the FTE area of the largest institution in REF2021'
    plt.figtext(0.5, 0.05, txt, wrap=True, horizontalalignment='center', fontsize=10)
    #export
    plt.savefig('figs/squares/'+shortplace+ '.png',dpi=240,bbox_inches='tight')
    
    

#this'll only work if you have ffmpeg installed (and probably if you are on linux)   
txt="ffmpeg -framerate 0.25 -pattern_type glob -i 'figs/squares/*.png'  -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' slow.mp4"
os.system(txt)

txt="ffmpeg -framerate 0.5 -pattern_type glob -i 'figs/squares/*.png'  -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' fast.mp4"
os.system(txt)

txt="ffmpeg -framerate 1 -pattern_type glob -i 'figs/squares/*.png'  -c:v libx264 -preset slow -crf 18 -c:a copy -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' faster.mp4"
os.system(txt)