import config
from googleapiclient.discovery import build
import json

# Load configuration to get API key
cfg = config.loadConfig()

class YoutubeThing:
    """
    DESCRIPTION
        Object containing YouTube API v3 and corresponding key

    ATTRIBUTES
        None

    METHODS
        getSearchResults(query, num_results=2)
        printSearchResults(data)
        getVideoDetails(video_id)
        printVideoDetails(data)
    """


    def __init__(self):
        """
        DESCRIPTION
            Constructor for YoutubeThing object.

        PARAMETERS
            None
        """
        self.api_key = cfg['youtube_api']['api_key']
        self.api = build(
        'youtube',
        'v3', 
        developerKey=self.api_key
        )


    def getSearchResults(self, query, num_results=2):
        """
        DESCRIPTION
            Utilizes Youtube API to search a query and returns the results.

        PARAMETERS
            query ------- (str) text that would go into YouTube search bar
            num_results - (int) maximum number of results to display (default: 2)

        OUTPUTS
            response - (json) response from API query
        """
        request = self.api.search().list(
            part = 'snippet',
            q=query,
            maxResults=num_results
            )
        response = request.execute()

        return response


    def printSearchResults(self, data):
        """
        DESCRIPTION
            Prints search results from getSearchResults() to screen.

        PARAMETERS
            data - (str) response from getSearchResults() or another query

        OUTPUTS
            None
        """
        items = data.get('items')

        for item in items:
            video_id = item['id']['videoId']
            video_response = self.getVideoDetails(video_id)
            self.printVideoDetails(video_response)


    def getVideoDetails(self, video_id):
        """
        DESCRIPTION
            Utilizes Youtube API to get details of a specific video.

        PARAMETERS
            video_id - (int) ID of youtube video

        OUTPUTS
            response - (json) response from API query
        """
        request = self.api.videos().list(
            part = 'snippet,statistics',
            id=video_id
            )
        response = request.execute()

        return response


    def printVideoDetails(self, data):
        """        
        DESCRIPTION
            Prints results from getVideoDetails() to screen.

        PARAMETERS
            data - (str) response from getVideoDetails() or another query

        OUTPUTS
            None
        """
        items = data.get('items')[0]
        snippet    = items['snippet']
        statistics = items['statistics']
        title = snippet['title']
        num_comments = statistics['commentCount']
        num_likes    = statistics['likeCount']
        num_views    = statistics['viewCount']

        print('Title:', title)
        print('  Num comments:', num_comments)
        print('  Num likes:   ', num_likes)
        print('  Num views:   ', num_views)

