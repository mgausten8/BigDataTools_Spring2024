"""
YouTube's Favorite Superhero
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author: Matt Austen
Class:  Big Data Tools
Prof:   Prof. Ganesh
Assgn:  Homework 3
Date:   03/03/2024

DESCRIPTION
    This application utilizes the YouTube Data API v3 to perform search queries 
    on specific superhero names and extract statistics pertaining to the Top N
    (where N is defined by the user) search results. These results include (1)
    the number of comments, (2) the number of views, and (3) the number of likes.
    These statistics are then used to infer 'YouTube's Favorite Superhero'.
"""

# Define which superheros to search in YouTube search bar
SUPERHEROES = ['captain america', 'iron man']#, 'hulk', 'thor']

# Define number of values that will be basis for analysis
NUM_VIDEOS  = 2

# Development flags - use these to toggle certain sections of code on/off
STEP_1 = False
STEP_2 = False
STEP_3 = True


##### Step 1: Read JSON from API ###############################

import classes
import json

if STEP_1==True:
    # Instantiate YoutubeThing object
    yt = classes.YoutubeThing()

    ### Print first <NUM_VIDEOS> videos for each 
    allStats = {'superhero': [], 'title': [], 'num_comments': [], 'num_likes': [], 'num_views': []}
    for superhero in SUPERHEROES:
        search_results = yt.getSearchResults(superhero, NUM_VIDEOS)

        # Store video info
        items = search_results.get('items')
        for item in items:
            video_id = item['id']['videoId']
            data = yt.getVideoDetails(video_id)

            title        = data['items'][0]['snippet']['title']
            num_comments = data['items'][0]['statistics']['commentCount']
            num_likes    = data['items'][0]['statistics']['likeCount']
            num_views    = data['items'][0]['statistics']['viewCount']


            allStats['superhero'].extend(superhero)
            allStats['title'].extend(title)
            allStats['num_comments'].extend(num_comments)
            allStats['num_likes'].extend(num_likes)
            allStats['num_views'].extend(num_views)
            '''
            stats = {'superhero': superhero, 
                     'title': title, 
                     'num_comments': num_comments, 
                     'num_likes': num_likes, 
                     'num_views': num_views}
            allStats.extend(stats)
            '''
            #print(allStats)


    json_stats = json.dumps(allStats, indent=4)
    print(json_stats)


##### Step 2: Insert into RedisJSON ############################

import redis

if STEP_2==True:
    # Establish Redis connection
    redis_conn = cfg.getRedisConnection()

    # Insert data into Redis
    redis_conn.set('youtube:stats:Mangs1337', response)

    # Extract data from redis
    json_data = redis_conn.get('youtube:stats:Mangs1337')

    print(json_data)


##### Step 3: Output processing ################################

import pandas as pd
import matplotlib.pyplot as plt 

if STEP_3==True:
    # Obtain data
    if STEP_1==False and STEP_2==False:
        import random

        print('WARNING! API not being called. Using dummy data...')
        dummy_data = {'superhero': ['captain america', 'iron man', 'hulk', 'thor'],
                      'title': ['NA', 'NA', 'NA', 'NA'],
                      'num_comments': random.sample(range(1, 100), 4),
                      'num_likes': random.sample(range(1, 100), 4),
                      'num_views': random.sample(range(1, 100), 4)}

        data = dummy_data
    elif STEP_1==False:
        print('WARNING! API not being called. Getting data from Redis...')
    elif STEP_2==False:
        print('WARNING! Calling API but bypassing Redis...')
    else:
        # Use API data from Redis (normal)
        pass

    # Convert data to pandas dataframe
    data_pd = pd.DataFrame.from_dict(data)

    data_pd.plot(x='superhero', y=['num_comments', 'num_likes', 'num_views'], kind='bar') 
    plt.show()


    #print(data_pd)



'''
response = json.dumps(
    request.execute(), 
    indent=4
    )'''

'''
request2 = youtube.comments().list(
    part='snippet',
    parentId=channel_id
    )
response2 = json.dumps(
    request2.execute(),
    indent=4
    )
'''
