"""
********************************************************************
YouTube Search Term Stats
~~~~~~~~~~~~~~~~~~~~~~~~~

Author: Matt Austen
Class:  Big Data Tools
Prof:   Prof. Ganesh
Assgn:  Homework 3
Date:   03/03/2024
********************************************************************
"""

# Define which SEARCH_TERMS to search in YouTube search bar
SEARCH_TERMS = ['captain america', 'iron man', 'hulk', 'thor']

# Define number of values that will be basis for analysis
NUM_VIDEOS = 10

# Development flags - use these to toggle certain sections of code on/off
USE_API   = False
USE_REDIS = False

print('********************************************************************')
print('HOMEWORK 3')
print('Matt Austen')
print(f'Big Data Tools - Spring 2024\n')
print('This application will...')
print(f'  Utilize the "YouTube Data API v3" to get the top {NUM_VIDEOS}') 
print(f'  videos from the following search terms:\n  {SEARCH_TERMS}.')
print(f'  It will then aggregate the data into plots and statistics.\n')


##### Step 1: Read JSON from API ###################################

print(f'STEP 1: Obtain data via YouTube Data API v3...', end='')

import classes
import json

if USE_API==True:
    # Instantiate YoutubeThing object
    yt = classes.YoutubeThing()

    ### Print first <NUM_VIDEOS> videos for each 
    allStats = {'search_term': [], 'title': [], 'num_comments': [], 'num_likes': [], 'num_views': []}
    for search_term in SEARCH_TERMS:
        search_results = yt.getSearchResults(search_term, NUM_VIDEOS)

        # Store video info
        items = search_results.get('items')
        for item in items:
            video_id = item['id']['videoId']
            data = yt.getVideoDetails(video_id)

            #print(data['items'][0]['statistics'])

            # Extract desired stats from API call
            title        = data['items'][0]['snippet']['title']
            num_comments = data['items'][0]['statistics']['commentCount']
            num_likes    = data['items'][0]['statistics']['likeCount']
            num_views    = data['items'][0]['statistics']['viewCount']
            
            # Append stats to output dict
            allStats['search_term'].append(search_term)
            allStats['title'].append(title)
            allStats['num_comments'].append(num_comments)
            allStats['num_likes'].append(num_likes)
            allStats['num_views'].append(num_views)

    # Convert stats dict to JSON
    stats = json.dumps(allStats, indent=4)

    # Output to file to reduce API calls when testing
    with open('temp.json', 'w') as outfile:
        outfile.write(stats)

    print('Success!')
else:
    print(f'Using pre-generated API data instead...', end='')

    # Load from most recent API call to avoid maxing API quota
    f = open('temp.json')
    stats = json.dumps(json.load(f), indent=4)

    print('Success!')


##### Step 2: Insert into RedisJSON ################################

print(f'STEP 2: Insert JSON data into Redis...', end='')

import config as cfg

if USE_REDIS==True:
    # Establish Redis connection
    redis_conn = cfg.getRedisConnection()

    # Insert data into Redis
    redis_conn.set('youtube:stats:hw3', stats)

    # Extract data from redis
    data_json = redis_conn.get('youtube:stats:hw3')

    print('Success!')
else:
    data_json = stats

    print('Skipping.')


##### Step 3: Output processing ####################################

print('STEP 3: Generate outputs! (see below)')

import pandas as pd
import matplotlib.pyplot as plt 

# Load JSON data into dictionary
data_dict = json.loads(data_json)

# Convert dictionary to pandas dataframe
df = pd.DataFrame.from_dict(data_dict)
df = df.drop(columns='title')

# Convert numeric data to numeric data-type
df[['num_comments', 'num_likes', 'num_views']] = df[['num_comments', 'num_likes', 'num_views']].apply(pd.to_numeric)

# Aggregate average data
df_avg = df.groupby('search_term').aggregate('mean').reset_index()
df_sum = df.groupby('search_term').aggregate('sum').reset_index()

# Adjust font sizes for plot
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# Plot Average aggregated data
plt.figure().set_figwidth(15)
fig,(ax1,ax2,ax3) = plt.subplots(1, 3)
ax1.bar(df_avg['search_term'], df_avg['num_comments'])
ax1.set_title(f'Avg Comments over Top {NUM_VIDEOS} Search Results')
ax2.bar(df_avg['search_term'], df_avg['num_likes'])
ax2.set_title(f'Avg Likes over Top {NUM_VIDEOS} Search Results')
ax3.bar(df_avg['search_term'], df_avg['num_views'])
ax3.set_title(f'Avg Views over Top {NUM_VIDEOS} Search Results')
fig.set_figwidth(15)
fig.savefig('temp.png')

# Output #1: Aggregated dataframes
print(f'\nOUTPUT #1: Aggregated dataframes')
print(df_avg)
print(df_sum)

# Output #2: 
print(f'\nOUTPUT #2: Search term superlatives')
most_talked_about = df_sum['search_term'].iloc[[df_sum['num_comments'].idxmax()]].tolist()[0].upper()
most_liked = df_sum['search_term'].iloc[[df_sum['num_likes'].idxmax()]].tolist()[0].upper()
most_viewed = df_sum['search_term'].iloc[[df_sum['num_views'].idxmax()]].tolist()[0].upper()
print(f'  Most talked about search term: {most_talked_about}')
print(f'  Most liked search term: {most_liked}')
print(f'  Most viewed search term: {most_viewed}')

# Output #3: Bar chart
print(f'\nOUTPUT #3: Bar chart')
print('  Bar chart saved to "temp.png".')

print('********************************************************************')

