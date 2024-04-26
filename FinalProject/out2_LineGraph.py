import config as cfg
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
from moviepy.editor import ImageSequenceClip

# Load config file and identify file paths
config = cfg.loadConfig()
data_path = config['paths']['data']
save_path = config['paths']['save']

# Load data
data = pd.read_csv(f'{data_path}/HSall_custom_all.csv')

# Initialize list of all image paths
all_save_paths = []


# Loop thru each chamber and congress and create figure
all_congress = sorted(data['congress'].unique())
for congress in tqdm(all_congress):
    data_tmp = data[data['congress']==congress]

    boxplot = data_tmp.boxplot(column='prob_nom', by='chamber')

    congress_year = congress+1788+(congress-1)

    #plt.xlim(-1.1, 1.1)
    #plt.ylim(-1.1, 1.1)

    num_str = str(congress).zfill(3)
    curr_save_path = f'{save_path}/output2_{num_str}.png'
    #all_save_paths.append(curr_save_path)

    boxplot.set_title(f'Year: {congress_year}  |  Congress {num_str}')

    plt.savefig(curr_save_path)

    plt.clf()
