import config as cfg
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

# Load config file and identify file paths
config = cfg.loadConfig()
data_path = config['paths']['data']
save_path = config['paths']['save']

# Load data
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
q1_H     = np.array(data_agg_H['prob_nom-q1'])
median_H = np.array(data_agg_H['prob_nom-median'])
q3_H     = np.array(data_agg_H['prob_nom-q3'])
lb_H     = np.array(data_agg_H['prob_nom-lb'])
ub_H     = np.array(data_agg_H['prob_nom-ub'])

# Spell out 'Senate' variables so plotting code is easier to read
q1_S     = np.array(data_agg_S['prob_nom-q1'])
median_S = np.array(data_agg_S['prob_nom-median'])
q3_S     = np.array(data_agg_S['prob_nom-q3'])
lb_S     = np.array(data_agg_S['prob_nom-lb'])
ub_S     = np.array(data_agg_S['prob_nom-ub'])

all_congress = np.array(sorted(data['congress'].unique()))

plt.figure(figsize=(18, 6))
plt.plot(all_congress, median_H, label='House')
plt.fill_between(all_congress, lb_H, ub_H, alpha=0.3)
plt.plot(all_congress, median_S, label='Senate')
plt.fill_between(all_congress, lb_S, ub_S, alpha=0.3)
plt.xlim(min(all_congress), max(all_congress))
plt.ylim(40, 100)
plt.xlabel('Congress')
plt.ylabel('Probability Member votes consistent with own Party')
plt.title('House of Representatives')
plt.grid(True)
plt.show()

#print(median_H)

'''
# Loop thru each chamber and congress and create figure
for congress in tqdm(all_congress):
    data_tmp_H = data[data['congress']==congress & data['chamber']=='House']
    data_tmp_S = data[data['congress']==congress & data['chamber']=='Senate']

    avg_prob_nom_H[congress-1] = data_tmp_H.groupby()
    votes_tmp = votes.groupby(['congress', 'chamber', 'icpsr']).agg({'prob': 'mean', 'rollnumber': 'size'}).reset_index()

'''