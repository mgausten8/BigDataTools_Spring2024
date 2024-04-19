import pandas as pd
import numpy as np
import config as cfg

# Load Voteview.com data
print(' ')
print('Loading data...')
members = pd.read_csv('https://voteview.com/static/data/out/members/HSall_members.csv')  # Member Ideology
parties = pd.read_csv('https://voteview.com/static/data/out/parties/HSall_parties.csv')  # Congressional Parties
votes   = pd.read_csv('https://voteview.com/static/data/out/votes/HSall_votes.csv')      # Members' Votes

# Add 'party_name', 'party_dim1_median', 'party_dim2_median', 'party_dim1_mean', 'party_dim2_mean' columns
print('Preparing data...')
df = pd.merge(members, parties, on=['congress', 'party_code', 'chamber'], how='left')

# Remove rows where chamber=='President'
df = df[df['chamber'] != 'President']

# Aggregate 'votes' on congress, chamber, icpsr... then add to df
votes_tmp = votes.groupby(['congress', 'chamber', 'icpsr']).agg({'prob': 'mean', 'rollnumber': 'size'}).reset_index()
df = pd.merge(df, votes_tmp, on=['congress', 'chamber', 'icpsr'], how='left')
df = df.rename(columns={'prob': 'prob_nom', 'rollnumber': 'n_prob_nom'})
df = df.fillna(value=np.nan)

# Output to file
print('Outputting data to csv...')
df.to_csv('HSall_custom.csv', index=False)

# Output smaller version of file for testing purposes
df_small = df[df['congress'].isin([1, 117, 118])]
df_small.to_csv('HSall_custom_small.csv', index=False)
print('Done.')

# Print data sizes to screen
print(' ')
print('Member_Ideology:       ',cfg.getNumRowsCols(members))
print('Congressional_Parties: ',cfg.getNumRowsCols(parties))
print('Members_Votes:         ',cfg.getNumRowsCols(votes))
print(' ')
print('Final Dataframe:       ',cfg.getNumRowsCols(df))
print(' ')