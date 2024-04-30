"""
part2_LineGraph.py
------------------
AUTHOR: Matt Austen
DATE:   29 Apr 2024

DESCRIPTION
    This script uses the computed value 'prob_nom' which is the average estimated
    probability that a member making the vote would make the vote they made. A
    higher probability suggests a member voted with the majority of their own 
    party, whereas a lower percentage suggests a member was more willing to vote
    against their own party at times. This is calcualted separately for the House
    and Senate and is show over time.

OUTPUT
    PNG file showing average probability of voting with own party over time
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

    # Generate query for output2
    query = '''MATCH (m:Member)-[:SERVED_IN]->(h:Chamber)
    MATCH (m:Member)-[:SERVED_DURING]->(c:Congress)
    RETURN c.congress AS congress,
           m.prob_nom AS prob_nom,
           h.chamber AS chamber;'''

    # Execute query
    with driver.session() as session:
        result = session.run(query)
        tmp = [record.values() for record in tqdm(result)]
        data = pd.DataFrame(tmp, columns=result.keys())

    # Close connection to neo4j
    driver.close()
else:
    data = pd.read_csv(f'{data_path}/HSall_custom.csv')

# Quick functions to compute 1st and 3rd quartiles
def q1(x):
    return x.quantile(0.25)
def q3(x):
    return x.quantile(0.75)

# Aggregate data on congress and chamber, computing average of prob_nom plus 
# other metrics based on those values
data_agg = data.groupby(['congress', 'chamber']).agg({'prob_nom': [q1, 'median', q3]}).reset_index()
data_agg.columns = ['-'.join(col).strip() for col in data_agg.columns.values]
data_agg = data_agg.rename(columns={'congress-': 'congress', 'chamber-': 'chamber'})

# Add IQR and Upper/Lower Bounds
data_agg['prob_nom-iqr'] = data_agg['prob_nom-q3'] - data_agg['prob_nom-q1']
data_agg['prob_nom-lb'] = data_agg['prob_nom-q1'] - (1.5*data_agg['prob_nom-iqr'])
data_agg['prob_nom-ub'] = data_agg['prob_nom-q3'] + (1.5*data_agg['prob_nom-iqr'])

# Split out dataframe between chambers of Congress
data_agg_H = data_agg[data_agg['chamber']=='House']
data_agg_S = data_agg[data_agg['chamber']=='Senate']

# Spell out 'House' variables so plotting code is easier to read
q1_H = np.array(data_agg_H['prob_nom-q1'])
q2_H = np.array(data_agg_H['prob_nom-median'])
q3_H = np.array(data_agg_H['prob_nom-q3'])
lb_H = np.array(data_agg_H['prob_nom-lb'])
ub_H = np.array(data_agg_H['prob_nom-ub'])

# Spell out 'Senate' variables so plotting code is easier to read
q1_S = np.array(data_agg_S['prob_nom-q1'])
q2_S = np.array(data_agg_S['prob_nom-median'])
q3_S = np.array(data_agg_S['prob_nom-q3'])
lb_S = np.array(data_agg_S['prob_nom-lb'])
ub_S = np.array(data_agg_S['prob_nom-ub'])

all_congress = np.array(sorted(data['congress'].unique()))

# Generate and save plot
fig,ax = plt.subplots(2, 1)
fig.suptitle('Average Probability of Voting with Own Party')
ax[0].plot(all_congress, q2_H, label='House', color='blue')
ax[0].fill_between(all_congress, lb_H, ub_H, alpha=0.3, color='cyan')
ax[0].set(ylabel='Probability')
ax[0].grid()
ax[0].legend()
ax[1].plot(all_congress, q2_S, label='Senate', color='red')
ax[1].fill_between(all_congress, lb_S, ub_S, alpha=0.3, color='magenta')
ax[1].set(xlabel='Congress', ylabel='Probability')
ax[1].grid()
ax[1].legend()
plt.setp(ax, xlim=(min(all_congress), max(all_congress)), ylim=(40, 100))
plt.savefig(f'{save_path}/output2.png', dpi=300)