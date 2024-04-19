import config as cfg

#data_path = 'https://raw.githubusercontent.com/mgausten8/BigDataTools_Spring2024/main/FinalProject/HSall_custom.csv'
data_path = 'https://raw.githubusercontent.com/mgausten8/BigDataTools_Spring2024/main/FinalProject/HSall_custom_small.csv'

# Create MEMBER node
query1 = '''
    LOAD CSV WITH HEADERS FROM '%s' AS row
    WITH row
    CREATE (m:Member {id:row.icpsr, name:row.bioname});
    ''' % data_path

# Create PARTY node
query2 = '''
    LOAD CSV WITH HEADERS FROM '%s' AS row
    WITH row
    CREATE (p:Party {id:row.party_code, name:row.party_name});
    ''' % data_path

# Create STATE node
query3 = '''
    LOAD CSV WITH HEADERS FROM '%s' AS row
    WITH row
    CREATE (s:State {id:row.state_icpsr, abbrev:row.state_abbrev});
    ''' % data_path

# Create CHAMBER node
query4 = '''
    LOAD CSV WITH HEADERS FROM '%s' AS row
    WITH row
    CREATE (c:Chamber {name:row.chamber});
    ''' % data_path

# Create relationships
query5 = '''
    LOAD CSV WITH HEADERS FROM '%s' AS row
    WITH row
    MATCH (m:Member {id:row.icpsr})
    MATCH (p:Party {id:row.party_code})
    MATCH (s:State {id:row.state_icpsr})
    MATCH (c:Chamber {name:row.chamber})
    MERGE (m)-[:IS_MEMBER_OF]->(p)
    MERGE (m)-[:REPRESENTED]->(s)
    MERGE (m)-[:SERVED_IN]->(c);
    ''' % data_path

# Establish database connection and reset it
driver = cfg.getNeo4jConnection()
cfg.clearDatabase(driver)

# Execute queries
print(' ')
print('Creating MEMBER node...')
cfg.quickCypher(driver, query1)
print('Creating PARTY node...')
cfg.quickCypher(driver, query2)
print('Creating STATE node...')
cfg.quickCypher(driver, query3)
print('Creating CHAMBER node...')
cfg.quickCypher(driver, query4)
print('Creating node relationships...')
cfg.quickCypher(driver, query5)
print('Success!')
print(' ')
