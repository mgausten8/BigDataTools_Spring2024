from neo4j import GraphDatabase
import yaml

# Quick function to print number of row/col of pandas dataframe
def getNumRowsCols(df):
    """

    """
    numRows = len(df.index)
    numCols = len(df.columns)
    return numRows,numCols

def loadConfig():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)
    
config = loadConfig()

def getNeo4jConnection():
    return GraphDatabase.driver(
        config['neo4j']['uri'],
        auth=(config['neo4j']['user'], config['neo4j']['password']))

def clearDatabase(driver):
    with driver.session() as session:
        session.run('MATCH (n) DETACH DELETE n')

def quickCypher(neo4jDriver, query, verbose=False):
    with neo4jDriver.session() as session:
        result = session.run(query)
        if verbose==True:
            for record in result:
                print(record)
