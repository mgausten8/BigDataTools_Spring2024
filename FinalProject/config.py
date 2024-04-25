from neo4j import GraphDatabase
import yaml

# Quick function to print number of row/col of pandas dataframe
def getNumRowsCols(df):
    """
    DESCRIPTION
        todo

    INPUTS
        df - todo

    OUTPUTS
        numRows - todo
        numCols - todo
    """
    numRows = len(df.index)
    numCols = len(df.columns)
    return numRows,numCols

def loadConfig():
    """
    DESCRIPTION
        todo

    OUTPUTS
        todo
    """
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)
    
config = loadConfig()

def getNeo4jConnection():
    """
    DESCRIPTION
        todo

    OUTPUTS
        todo
    """
    return GraphDatabase.driver(
        config['neo4j']['uri'],
        auth=(config['neo4j']['user'], config['neo4j']['password']))

def clearDatabase(driver):
    """
    DESCRIPTION
        todo

    INPUTS
        todo
    """
    with driver.session() as session:
        session.run('MATCH (n) DETACH DELETE n')

def quickCypher(neo4jDriver, query, verbose=False):
    """
    DESCRIPTION
        todo

    INPUTS
        todo
    """
    with neo4jDriver.session() as session:
        result = session.run(query)
        if verbose==True:
            for record in result:
                print(record)
