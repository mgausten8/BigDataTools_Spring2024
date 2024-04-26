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
data = pd.read_csv(f'{data_path}/HSall_custom.csv')

# Initialize list of all image paths
all_save_paths = []

# Loop thru all congress and create figure
print('Generating images:')
all_congress = sorted(data['congress'].unique())
for congress in tqdm(all_congress):
    data_tmp = data[data['congress']==congress]

    # Create scatter plot of nom dim1/2
    ax = data_tmp.plot.scatter(x='nominate_dim1', 
                               y='nominate_dim2', 
                               c='nominate_dim1_mean',
                               cmap='coolwarm', 
                               vmin=-0.95,
                               vmax=0.95)

    congress_year = congress+1788+(congress-1)

    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)

    num_str = str(congress).zfill(3)
    curr_save_path = f'{save_path}/output1_{num_str}.png'
    all_save_paths.append(curr_save_path)

    ax.set_title(f'Year: {congress_year}  |  Congress {num_str}')
    ax.set_xlabel('Nominate dimension 1')
    ax.set_ylabel('Nominate dimension 2')

    plt.savefig(curr_save_path)

    plt.clf()

frame_duration = 0.1  # Amount of time you see each image
num_frames = len(all_save_paths)  # Number of images (frames)
duration_s = frame_duration * num_frames

clip = ImageSequenceClip(all_save_paths, fps=1/frame_duration)

# Write the video to an AVI file
clip.write_videofile(f'{data_path}/output_video.mp4', codec='libx264', fps=24)

# Delete all image files
for x in all_save_paths:
    os.remove(x)

print(f'Output file length: {duration_s} s')