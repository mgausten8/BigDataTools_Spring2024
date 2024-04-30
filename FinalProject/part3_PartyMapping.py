"""
part3_PartyMapping.py
---------------------
AUTHOR: Matt Austen
DATE:   02 May 2024

DESCRIPTION
    This script calculated and mean and standard deviation of selected sets of
    legislators' Nominate scores (dimension 1 only) and plots normal curves
    aggregated over certain parties. Specifcally, the script plots the Democratic
    and Republican party of modern day AND the Federalist and Democratic 
    Republican parties of approx. 1800. Three sessions of congress are used for
    each party (i.e. Federalist Party is represented by Congress 5, 6, and 7).


OUTPUT
    PNG file of party normal curve comparisons of nominate scores
"""

import config as cfg
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

# True: load data from Neo4j database, False: Load from CSV
USE_NEO4J = True

# Load config file and identify file paths
config = cfg.loadConfig()
data_path = config['paths']['data']
save_path = config['paths']['save']

# Load data
if USE_NEO4J:
    print('Loading data from neo4j...')

    # Get neo4j connection
    driver = cfg.getNeo4jConnection()

    # Generate query for output3
    query = '''MATCH (m:Member)-[:MEMBER_OF]->(p:Party)
    MATCH (m:Member)-[:SERVED_DURING]->(c:Congress)
    RETURN c.congress AS congress,
           m.nominate_dim1 AS nominate_dim1,
           p.party_name AS party_name;'''

    # Execute query
    with driver.session() as session:
        result = session.run(query)
        tmp = [record.values() for record in tqdm(result)]
        data = pd.DataFrame(tmp, columns=result.keys())

    # Close connection to neo4j
    driver.close()
else:
    data = pd.read_csv(f'{data_path}/HSall_custom.csv')

# Capture dataframes consisting of desired Congresses
data_old = data[data['congress'].isin(range(5, 8))]      # Congress 5,6,7
data_new = data[data['congress'].isin(range(116, 119))]  # Congress 116,117,118

# Calculate stats of Congress 5-7
stdev_DR = data_old['nominate_dim1'][data_old['party_name']=='Democrat-Republican'].std()
mean_DR  = data_old['nominate_dim1'][data_old['party_name']=='Democrat-Republican'].mean()
stdev_Fd = data_old['nominate_dim1'][data_old['party_name']=='Federalist'].std()
mean_Fd  = data_old['nominate_dim1'][data_old['party_name']=='Federalist'].mean()

# Calculate stats of Congress 116-118
stdev_D = data_new['nominate_dim1'][data_new['party_name']=='Democrat'].std()
mean_D  = data_new['nominate_dim1'][data_new['party_name']=='Democrat'].mean()
stdev_R = data_new['nominate_dim1'][data_new['party_name']=='Republican'].std()
mean_R  = data_new['nominate_dim1'][data_new['party_name']=='Republican'].mean()

# Function that computes x,y coordinates of normal curve given std_dev and mean
def calcXYnorm(std_dev, mean):
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
    y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    return x,y

x_DR,y_DR = calcXYnorm(stdev_DR, mean_DR)
x_Fd,y_Fd = calcXYnorm(stdev_Fd, mean_Fd)
x_D,y_D = calcXYnorm(stdev_D, mean_D)
x_R,y_R = calcXYnorm(stdev_R, mean_R)

# Generate Democrat curve (modern day)
plt.plot(x_D, y_D, ':', color='blue', label='Democrat')
plt.fill_between(x_D, y_D, color='blue', alpha=0.1)

# Generate Republican curve (modern day)
plt.plot(x_R, y_R, ':', color='red', label='Republican')
plt.fill_between(x_R, y_R, color='red', alpha=0.1)

# Generate Democratic Republican curve (past)
plt.plot(x_DR, y_DR, color='cyan', label='Dem. Republican')
plt.fill_between(x_DR, y_DR, color='cyan', alpha=0.4)

# Generate Federalist curve (past)
plt.plot(x_Fd, y_Fd, color='magenta', label='Federalist')
plt.fill_between(x_Fd, y_Fd, color='magenta', alpha=0.4)

plt.xlim(-1, 1)
plt.title('Party Nominate Score Comparison - 1800s vs Present')
plt.xlabel('Nominate Economic Dimension')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()
plt.savefig(f'{save_path}/output3.png', dpi=300)