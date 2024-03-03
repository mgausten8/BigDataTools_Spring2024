'''
Name: Matt Austen
Date: 03/03/2024



'''


import classes
import json
import redis


SUPERHEROES = ['captain america', 'iron man']#, 'hulk', 'thor']
NUM_VIDEOS  = 1

'''
channel_handle = 'Mangs1337'

yt = classes.YoutubeThing()

response = yt.getHandleStats(channel_handle)

channel_id = response['items'][0]['id']

print(channel_id)
'''

# Plan:
#   For the following search terms, determine the number of comments, likes, and views among the top 5 videos.



### Step 1: Read JSON from API ###############################

import classes
import json

# Instantiate YoutubeThing object
yt = classes.YoutubeThing()

# Print first <NUM_VIDEOS> videos for each 
#allStats = dict.fromkeys(['superhero', 'title', 'num_comments', 'num_likes', 'num_views'])
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


### Step 2: Insert into RedisJSON ############################

'''
redis_conn = cfg.getRedisConnection()

redis_conn.set('youtube:stats:Mangs1337', response)

# Get JSON and decode 
json_data = redis_conn.get('youtube:stats:Mangs1337')

print(json_data)

'''



### Step 3: Output processing ################################





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
