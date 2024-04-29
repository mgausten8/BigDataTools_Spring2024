import config as cfg
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
from moviepy.editor import ImageSequenceClip

# True: load data from Neo4j database, False: Load from CSV
USE_NEO4J = False

# Load config file and identify file paths
config = cfg.loadConfig()
data_path = config['paths']['data']
save_path = config['paths']['save']

# Load data
if USE_NEO4J:
    print('Loading data from neo4j...')

    # Get neo4j connection
    driver = cfg.getNeo4jConnection()

    query = '''MATCH (m:Member)
    MATCH (c:Congress)
    MATCH (p:Party)
    RETURN m.congress, m.nominate_dim1, m.nominate_dim2, c.congress, p.party_code, p.nominate_dim1_mean;
    '''

    with driver.session() as session:
        result = session.run(query)
        for i,record in enumerate(result):
            print(i,record)
        #tmp = [record.values() for record in tqdm(result)]
        #data = pd.DataFrame(tmp, columns=result.keys())

    #print(tmp)

    driver.close()

    import sys
    sys.exit()
else:
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

    # Calculate first year of current congress
    congress_year = congress+1788+(congress-1)

    # Plot configurations
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    num_str = str(congress).zfill(3)
    ax.set_title(f'Year: {congress_year}  |  Congress {num_str}')
    ax.set_xlabel('Nominate dimension 1')
    ax.set_ylabel('Nominate dimension 2')

    # Save image of congress nomination scores
    curr_save_path = f'{save_path}/out_{num_str}.png'
    all_save_paths.append(curr_save_path)
    plt.savefig(curr_save_path)

    plt.clf()

# Adjust clip duration
frame_duration = 0.1   # Amount of time you see each image
num_frames = len(all_save_paths)  # Number of images (frames)
duration_s = frame_duration * num_frames

# Write the video to an MP4 file
clip = ImageSequenceClip(all_save_paths, fps=1/frame_duration)
clip.write_videofile(f'{data_path}/output1.mp4', codec='libx264', fps=24)

# Delete all image files
for x in all_save_paths:
    os.remove(x)

print(f'Output file length: {duration_s} s')