import redis
import yaml

def loadConfig():
    '''Load configuration from the YAML file.

    Returns:
        dict: Configuration data.
    '''
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = loadConfig()

def getRedisConnection():
    '''Create a Redis connection using the configuration.

    Returns:
        Redis: Redis connection object.
    '''
    return redis.Redis(
        port=6379,
        decode_responses=True
    )