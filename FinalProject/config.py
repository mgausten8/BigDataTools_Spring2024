import yaml
from neo4j import GraphDatabase

# Quick function to print number of row/col of pandas dataframe
def getNumRowsCols(df):
    """
    DESCRIPTION
        Function that returns number of rows and columns of pandas dataframe

    INPUTS
        df - Pandas dataframe

    OUTPUTS
        numRows - (num) number of rows of df
        numCols - (num) number of columns of df
    """
    numRows = len(df.index)
    numCols = len(df.columns)
    return numRows,numCols

def loadConfig():
    """
    DESCRIPTION
        Loads configuration stored within config.yaml
    """
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)
    
config = loadConfig()

def getNeo4jConnection():
    """
    DESCRIPTION
        Creates neo4j connection given parameters listed in config.yaml

    OUTPUTS
        Neo4j driver object
    """
    return GraphDatabase.driver(
        config['neo4j']['uri'],
        auth=(config['neo4j']['user'], config['neo4j']['password']))

def clearDatabase(driver):
    """
    DESCRIPTION
        Clears database connected to 'driver'

    INPUTS
        Neo4j driver object
    """
    with driver.session() as session:
        session.run('MATCH (n) DETACH DELETE n')
