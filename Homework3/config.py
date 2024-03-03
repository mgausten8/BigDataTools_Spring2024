import redis
import yaml

def loadConfig():
    """
    DESCRIPTION
        Load configuration from the YAML file.

    OUTPUTS
        (dict) configuration data
    """
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = loadConfig()

def getRedisConnection():
    """
    DESCRIPTION
        Create a Redis connection using the configuration.

    OUTPUTS:
        (redis obj) Redis connection object
    """
    return redis.Redis(
        port=6379,
        decode_responses=True
    )