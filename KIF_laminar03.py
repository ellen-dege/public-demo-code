#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 23:15:57 2021

@author: ellendegenn

Purpose: generate laminar distribution histograms
for cells counted using FIJI
Input:
    csv with cell x and y locations and apical/basal surface locations
    csv with animal info metadata (including blinded filenames)
Output:
    new data structures containing all data, including normalized y positions
for all cells
    histograms of laminar position by experimental condition
    
Based on R17_compare01, R17_IHC_layer_compile01, R17_IHC_layer_overlap05flip_Satb2

Vers02, updated 5/12/21:
    - store complete dfs for easier plotting
Updated 5/16/21:
    - normalize number of cells to total per image (for X-axis)
    - save an output of summary stastistics (to give to Xuyu to plot in Prism)
    with means and SEMs for each bin for each condition
Updated 5/18/21:
    - add error bars (SEM) to hist - can't do SEM in seaborn, although seaborn is
    nicer, implemented in both seaborn and pyplot (note default bar height is HUGE)

Vers03, updated 5/19/21:
    - calculate and plot standard deviation instead of SEM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy import stats
import seaborn as sns

############
### load metadata csv
############
BaseDir = '/Users/ellendegenn/Dropbox (MIT)/Walsh Lab/KIF26A/Image Analysis/laminar_quantification/'
OutDir = BaseDir+'210519_out/'
CellDir = BaseDir+'210501_210510_results/'
metafile = 'Master01.csv'

metadf = pd.read_csv(BaseDir+metafile)

############
### load csvs from folder
############

#initialize empty df to store all the data
fulldf = pd.DataFrame()

numfiles = len(metadf)
for current in range(0,numfiles):
    
    #cellfile = 'blind_0001.csv'
    cellfile = metadf['Blinded_Name'][current]+'.csv'

    #now can get cell data
    celldf = pd.read_csv(CellDir+cellfile)

    #let's get all the cells
    allx = celldf['X'][celldf['Counter']==0]
    ally = celldf['Y'][celldf['Counter']==0]

    #check lengths
    if (len(allx)==(np.subtract(len(celldf),2))):
        print('X length ok')
    if (len(ally)==(np.subtract(len(celldf),2))):
        print('Y length ok')

    #now just the ypos of apical and basal - but I won't know which is which yet
    ybounds = celldf['Y'][celldf['Counter']==1]
    #drop indices
    ybounds = ybounds.reset_index(drop=True)
    #figure out which is bigger and assign
    #this will be messed up if things are flipped so you may want to check as early as here!!!
    if np.subtract(ybounds[0],ybounds[1]) < 0:
        ay = ybounds[0]
        by = ybounds[1]
    elif np.subtract(ybounds[0],ybounds[1]) > 0:
        ay = ybounds[1]
        by = ybounds[0]

    #now normalize
    #first calculate the maximum y extent and store
    normval = np.subtract(by,ay)
    #now divide all ypositions by this and store
    allnormy = np.divide(ally,normval)
    #now need to flip y value for all
    allnormy = np.subtract(1,allnormy)

    #now check that normalization worked correctly (range: 0-1)
    print("Verify normalization. Below arrays should be empty")
    print(allnormy[:][allnormy[:]<0])
    print(allnormy[:][allnormy[:]>1])
    
    #to make the df size consistent and combinable, make full arrays of each metadatavalue
    animalarray = np.full(len(allx),metadf['Animal_ID'][current])
    conditionarray = np.full(len(allx),metadf['Condition'][current])
    sxarray = np.full(len(allx),metadf['SX_Age'][current])
    sacarray = np.full(len(allx),metadf['Sac_Age'][current])
    apicalarray = np.full(len(allx),ay)
    normarray = np.full(len(allx),normval)
    basalarray = np.full(len(allx),by)
    numtotarray = np.full(len(allx),len(allx))
    
    #now store in a df, one column at a time
    temp = pd.DataFrame(data=animalarray, columns = ['Animal_ID'])
    temp['Condition'] = conditionarray
    temp['SX_Age'] = sxarray
    temp['Sac_Age'] = sacarray
    temp['Apical_Y'] = apicalarray
    temp['Basal_Y'] = basalarray
    temp['Normalization_Value'] = normarray
    temp['Total_Num_Cells'] = numtotarray
    temp['Cells_X_Pos'] = allx
    temp['Cells_Y_Pos'] = ally
    temp['Norm_Flipped_Cells_Y_Pos'] = allnormy
    #temp will store individual dfs to save, then fulldf will include all
    
    fulldf = fulldf.append(temp, ignore_index=True)
    
    
    #pos_temp = pd.merge(allx, ally, left_index=True, right_index=True, how="outer")
    
    #norm_temp = pd.merge(pos_temp, allnormy, left_index=True, right_index=True, how="outer")
    
    #temp = meta_temp.append(norm_temp)
    
    ###COMMENT OUT IF YOU'VE ALREADY RUN THIS CODE AND SAVED e.g. you just want to re-plot
    """
    #save the df!
    temp.to_csv(OutDir+metadf['Animal_ID'][current]+'.csv', index=False)
    """

"""
#can also save fulldf here if you want
fulldf.to_csv(OutDir+'FullDF.csv', index=False)
"""


#########
### hist calculations
#########
#saves the array for hist values in first variable, then the array of bin edges in the second
#If bins is an int, it defines the number of equal-width bins in the given range (10, by default).
#If bins is a sequence, it defines a monotonically increasing array of bin edges, including the rightmost edge,
#allowing for non-uniform bin widths.
#All but the last (righthand-most) bin is half-open.

#10 bins for all
oehist, oe_bines = np.histogram(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='human OE'],
                                range=(0,1), bins=10)
schist, sc_bines = np.histogram(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='mCherry scramble'],
                                range=(0,1), bins=10)
sh1hist, sh1_bines = np.histogram(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='shRNA1'],
                                range=(0,1), bins=10)
sh2hist, sh2_bines = np.histogram(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='shRNA2'],
                                range=(0,1), bins=10)
sh3hist, sh3_bines = np.histogram(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='shRNA3'],
                                range=(0,1), bins=10)

#########
### with bins, can caluclate standard deviation
#########

#function to calculate the standard deviation within each bin range
def binstats(b, cond, i):
    #long and annoying but basically for the condition passed in by cond (string) within fulldf,
    #for passed in iterator, calulate the SEM between passed in bins (b)
    s = np.std(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']==cond][(fulldf['Norm_Flipped_Cells_Y_Pos']>b[i])&(fulldf['Norm_Flipped_Cells_Y_Pos']<b[i+1])])
    #and include the boundary for the last bin
    if i==10:
        s = np.std(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']==cond][(fulldf['Norm_Flipped_Cells_Y_Pos']>b[i])&(fulldf['Norm_Flipped_Cells_Y_Pos']<=b[i+1])])
    return s

#initialize arrays to store
oeSTD = []
scSTD = []
sh1STD = []
sh2STD = []
sh3STD = []

#now call SEM function for each condition
for j in range(0,10):
    oeSTD.append(binstats(oe_bines,'human OE',j))
    scSTD.append(binstats(sc_bines,'mCherry scramble',j))
    sh1STD.append(binstats(sh1_bines,'shRNA1',j))
    sh2STD.append(binstats(sh1_bines,'shRNA2',j))
    sh3STD.append(binstats(sh1_bines,'shRNA3',j))

#########
### now normalize the hist value for each bin
#########

oe_len = len(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='human OE'])
sc_len = len(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='mCherry scramble'])
sh1_len = len(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='shRNA1'])
sh2_len = len(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='shRNA2'])
sh3_len = len(fulldf['Norm_Flipped_Cells_Y_Pos'][fulldf['Condition']=='shRNA3'])

oehist_norm = np.divide(oehist,oe_len)
schist_norm = np.divide(schist,sc_len)
sh1hist_norm = np.divide(sh1hist,sh1_len)
sh2hist_norm = np.divide(sh2hist,sh2_len)
sh3hist_norm = np.divide(sh3hist,sh3_len)

#########
### finally, save everything in one df
#########

#prepare to store in a df to save
#probably a better way to do this but oh well
all_labels = np.full(10,'human OE')
all_labels = np.append(all_labels,np.full(10,'mCherry scramble'))
all_labels = np.append(all_labels,np.full(10,'shRNA1'))
all_labels = np.append(all_labels,np.full(10,'shRNA2'))
all_labels = np.append(all_labels,np.full(10,'shRNA3'))

all_hist = oehist_norm
all_hist = np.append(all_hist,schist_norm)
all_hist = np.append(all_hist,sh1hist_norm)
all_hist = np.append(all_hist,sh2hist_norm)
all_hist = np.append(all_hist,sh3hist_norm)

all_STD = oeSTD
all_STD = np.append(all_STD,scSTD)
all_STD = np.append(all_STD,sh1STD)
all_STD = np.append(all_STD,sh2STD)
all_STD = np.append(all_STD,sh3STD)

#rather than putting the left or right or center bin edge, just save as decile number - idk what Prism takes
deciles = np.arange(1,11,1)
for i in range(0,4):
    deciles = np.append(deciles,np.arange(1,11,1))
    
#centers makes more sense though
decile_centers = np.arange(0.05,1.05,0.1)
decile_centers_all = np.arange(0.05,1.05,0.1)
for i in range(0,4):
    decile_centers_all = np.append(decile_centers_all,np.arange(0.05,1.05,0.1))

#now make and append to a df
STDdf = pd.DataFrame(data=all_labels, columns=['Condition'])
STDdf['Normalized_Cell_Freq'] = all_hist
STDdf['Stdev'] = all_STD
#SEMdf['Decile'] = deciles
STDdf['Decile_Centers'] = decile_centers_all

#and save!
STDdf.to_csv(OutDir+'StdevDF.csv', index=False)

############
### plot these histograms with Seaborn - so no SEM error bars
############
#colors from: https://matplotlib.org/stable/gallery/color/named_colors.html

#basic plots without error bars
ax1 = sns.histplot(data=fulldf[fulldf['Condition']=='human OE'],
                   y='Norm_Flipped_Cells_Y_Pos',
                   bins=10,
                   binrange=(0,1),
                   stat='probability',
                   color='mediumblue',
                   )
ax1.set_ylabel('Laminar Position')
ax1.set_xlabel('Relative Frequency')
ax1.set_title('Human OE')
#probability normalizes counts so that the sum of the bar heights is 1

plt.savefig(OutDir+"210519_seaborn_HumanOE.svg", format="svg")
plt.savefig(OutDir+"210519_seaborn_HumanOE.png", format="png")
plt.clf()

###
ax2 = sns.histplot(data=fulldf[fulldf['Condition']=='mCherry scramble'],
                   y='Norm_Flipped_Cells_Y_Pos',
                   bins=10,
                   binrange=(0,1),
                   stat='probability',
                   color='darkgreen',
                   )
ax2.set_ylabel('Laminar Position')
ax2.set_xlabel('Relative Frequency')
ax2.set_title('mCherry Scramble')
#probability normalizes counts so that the sum of the bar heights is 1

plt.savefig(OutDir+"210519_seaborn_Scramble.svg", format="svg")
plt.savefig(OutDir+"210519_seaborn_Scramble.png", format="png")
plt.clf()

###
ax3 = sns.histplot(data=fulldf[fulldf['Condition']=='shRNA1'],
                   y='Norm_Flipped_Cells_Y_Pos',
                   bins=10,
                   binrange=(0,1),
                   stat='probability',
                   color='darksalmon',
                   )
ax3.set_ylabel('Laminar Position')
ax3.set_xlabel('Relative Frequency')
ax3.set_title('shRNA1')
#probability normalizes counts so that the sum of the bar heights is 1

plt.savefig(OutDir+"210519_seaborn_shRNA1.svg", format="svg")
plt.savefig(OutDir+"210519_seaborn_shRNA1.png", format="png")
plt.clf()

###
ax4 = sns.histplot(data=fulldf[fulldf['Condition']=='shRNA2'],
                   y='Norm_Flipped_Cells_Y_Pos',
                   bins=10,
                   binrange=(0,1),
                   stat='probability',
                   color='indianred',
                   )
ax4.set_ylabel('Laminar Position')
ax4.set_xlabel('Relative Frequency')
ax4.set_title('shRNA2')
#probability normalizes counts so that the sum of the bar heights is 1

plt.savefig(OutDir+"210519_seaborn_shRNA2.svg", format="svg")
plt.savefig(OutDir+"210519_seaborn_shRNA2.png", format="png")
plt.clf()

###
ax5 = sns.histplot(data=fulldf[fulldf['Condition']=='shRNA3'],
                   y='Norm_Flipped_Cells_Y_Pos',
                   bins=10,
                   binrange=(0,1),
                   stat='probability',
                   color='maroon',
                   )
ax5.set_ylabel('Laminar Position')
ax5.set_xlabel('Relative Frequency')
ax5.set_title('shRNA3')
#probability normalizes counts so that the sum of the bar heights is 1

plt.savefig(OutDir+"210519_seaborn_shRNA3.svg", format="svg")
plt.savefig(OutDir+"210519_seaborn_shRNA3.png", format="png")
plt.clf()

############
### now plot with plt.barh
############

fig, ax1 = plt.subplots(1)

ax1.barh(decile_centers, oehist_norm, height=0.08, align='center', color='lightskyblue', xerr=oeSTD)
ax1.set_title('Human OE')
ax1.set_ylabel('Laminar Position')
ax1.set_xlabel('Relative Frequency')
ax1.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_HumanOE.svg", format="svg")
plt.savefig(OutDir+"210519_plt_HumanOE.png", format="png")
plt.show()

###
fig, ax2 = plt.subplots(1)

ax2.barh(decile_centers, schist_norm, height=0.08, align='center', color='darkseagreen', xerr=scSTD)
ax2.set_title('mCherry Scramble')
ax2.set_ylabel('Laminar Position')
ax2.set_xlabel('Relative Frequency')
ax2.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_Scramble.svg", format="svg")
plt.savefig(OutDir+"210519_plt_Scramble.png", format="png")
plt.show()

###
fig, ax3 = plt.subplots(1)

ax3.barh(decile_centers, sh1hist_norm, height=0.08, align='center', color='darksalmon', xerr=sh1STD)
ax3.set_title('shRNA1')
ax3.set_ylabel('Laminar Position')
ax3.set_xlabel('Relative Frequency')
ax3.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_shRNA1.svg", format="svg")
plt.savefig(OutDir+"210519_plt_shRNA1.png", format="png")
plt.show()

###
fig, ax4 = plt.subplots(1)

ax4.barh(decile_centers, sh2hist_norm, height=0.08, align='center', color='indianred', xerr=sh2STD)
ax4.set_title('shRNA2')
ax4.set_ylabel('Laminar Position')
ax4.set_xlabel('Relative Frequency')
ax4.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_shRNA2.svg", format="svg")
plt.savefig(OutDir+"210519_plt_shRNA2.png", format="png")
plt.show()

###
fig, ax5 = plt.subplots(1)

ax5.barh(decile_centers, sh3hist_norm, height=0.08, align='center', color='sienna', xerr=sh3STD)
ax5.set_title('shRNA3')
ax5.set_ylabel('Laminar Position')
ax5.set_xlabel('Relative Frequency')
ax5.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_shRNA3.svg", format="svg")
plt.savefig(OutDir+"210519_plt_shRNA3.png", format="png")
plt.show()

#and all in one why not
fig, (ax1, ax2) = plt.subplots(1,2)

ax1.barh(decile_centers, oehist_norm, height=0.08, align='center', color='lightskyblue', xerr=oeSTD)
ax1.set_title('Human OE')
ax1.set_ylabel('Laminar Position')
ax1.set_xlabel('Relative Frequency')
ax1.set_ylim(bottom=0, top=1.0)
##
ax2.barh(decile_centers, schist_norm, height=0.08, align='center', color='darkseagreen', xerr=scSTD)
ax2.set_title('mCherry Scramble')
#ax2.set_ylabel('Laminar Position')
ax2.set_xlabel('Relative Frequency')
ax2.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_hOE_scrb.svg", format="svg")
plt.savefig(OutDir+"210519_plt_hOE_scrb.png", format="png")
plt.show()

#now the shRNAs
fig, (ax2, ax3, ax4, ax5) = plt.subplots(1,4)

##
ax2.barh(decile_centers, schist_norm, height=0.08, align='center', color='darkseagreen', xerr=scSTD)
ax2.set_title('mCherry Scramble')
ax2.set_ylabel('Laminar Position')
#ax2.set_xlabel('Relative Frequency')
ax2.set_ylim(bottom=0, top=1.0)
##
ax3.barh(decile_centers, sh1hist_norm, height=0.08, align='center', color='darksalmon', xerr=sh1STD)
ax3.set_title('shRNA1')
#ax3.set_ylabel('Laminar Position')
ax3.set_xlabel('Relative Frequency')
ax3.set_ylim(bottom=0, top=1.0)
##
ax4.barh(decile_centers, sh2hist_norm, height=0.08, align='center', color='indianred', xerr=sh2STD)
ax4.set_title('shRNA2')
#ax4.set_ylabel('Laminar Position')
#ax4.set_xlabel('Relative Frequency')
ax4.set_ylim(bottom=0, top=1.0)
##
ax5.barh(decile_centers, sh3hist_norm, height=0.08, align='center', color='sienna', xerr=sh3STD)
ax5.set_title('shRNA3')
#ax5.set_ylabel('Laminar Position')
#ax5.set_xlabel('Relative Frequency')
ax5.set_ylim(bottom=0, top=1.0)
plt.savefig(OutDir+"210519_plt_allshRNA.svg", format="svg")
plt.savefig(OutDir+"210519_plt_allshRNA.png", format="png")
plt.show()