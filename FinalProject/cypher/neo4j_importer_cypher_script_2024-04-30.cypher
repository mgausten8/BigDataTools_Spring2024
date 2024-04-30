:param {
  // Define the file path root and the individual file names required for loading.
  // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
  file_path_root: 'file:///', // Change this to the folder your script can access the files at.
  file_0: 'HSall_custom.csv'
};

// CONSTRAINT creation
// -------------------
//
// Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
//
// NOTE: The following constraint creation syntax is generated based on the current connected database version 5.19-aura.
CREATE CONSTRAINT `icpsr_Member_uniq` IF NOT EXISTS
FOR (n: `Member`)
REQUIRE (n.`icpsr`) IS UNIQUE;
CREATE CONSTRAINT `state_icpsr_State_uniq` IF NOT EXISTS
FOR (n: `State`)
REQUIRE (n.`state_icpsr`) IS UNIQUE;
CREATE CONSTRAINT `party_code_Party_uniq` IF NOT EXISTS
FOR (n: `Party`)
REQUIRE (n.`party_code`) IS UNIQUE;
CREATE CONSTRAINT `congress_Congress_uniq` IF NOT EXISTS
FOR (n: `Congress`)
REQUIRE (n.`congress`) IS UNIQUE;
CREATE CONSTRAINT `chamber_Chamber_uniq` IF NOT EXISTS
FOR (n: `Chamber`)
REQUIRE (n.`chamber`) IS UNIQUE;

:param {
  idsToSkip: []
};

// NODE load
// ---------
//
// Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
//
// NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`icpsr` IN $idsToSkip AND NOT toInteger(trim(row.`icpsr`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Member` { `icpsr`: toInteger(trim(row.`icpsr`)) })
  SET n.`icpsr` = toInteger(trim(row.`icpsr`))
  SET n.`congress` = toInteger(trim(row.`congress`))
  SET n.`chamber` = row.`chamber`
  SET n.`state_icpsr` = toInteger(trim(row.`state_icpsr`))
  SET n.`party_code` = toInteger(trim(row.`party_code`))
  SET n.`bioname` = row.`bioname`
  SET n.`nominate_dim1` = toFloat(trim(row.`nominate_dim1`))
  SET n.`nominate_dim2` = toFloat(trim(row.`nominate_dim2`))
  SET n.`prob_nom` = toFloat(trim(row.`prob_nom`))
  SET n.`n_prob_nom` = toFloat(trim(row.`n_prob_nom`))
  SET n.`district_code` = toFloat(trim(row.`district_code`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`state_icpsr` IN $idsToSkip AND NOT toInteger(trim(row.`state_icpsr`)) IS NULL
CALL {
  WITH row
  MERGE (n: `State` { `state_icpsr`: toInteger(trim(row.`state_icpsr`)) })
  SET n.`state_icpsr` = toInteger(trim(row.`state_icpsr`))
  SET n.`state_abbrev` = row.`state_abbrev`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`party_code` IN $idsToSkip AND NOT toInteger(trim(row.`party_code`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Party` { `party_code`: toInteger(trim(row.`party_code`)) })
  SET n.`party_code` = toInteger(trim(row.`party_code`))
  SET n.`party_name` = row.`party_name`
  SET n.`n_members` = toInteger(trim(row.`n_members`))
  SET n.`nominate_dim1_median` = toFloat(trim(row.`nominate_dim1_median`))
  SET n.`nominate_dim2_median` = toFloat(trim(row.`nominate_dim2_median`))
  SET n.`nominate_dim1_mean` = toFloat(trim(row.`nominate_dim1_mean`))
  SET n.`nominate_dim2_mean` = toFloat(trim(row.`nominate_dim2_mean`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`congress` IN $idsToSkip AND NOT toInteger(trim(row.`congress`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Congress` { `congress`: toInteger(trim(row.`congress`)) })
  SET n.`congress` = toInteger(trim(row.`congress`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`chamber` IN $idsToSkip AND NOT row.`chamber` IS NULL
CALL {
  WITH row
  MERGE (n: `Chamber` { `chamber`: row.`chamber` })
  SET n.`chamber` = row.`chamber`
} IN TRANSACTIONS OF 10000 ROWS;


// RELATIONSHIP load
// -----------------
//
// Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Member` { `icpsr`: toInteger(trim(row.`icpsr`)) })
  MATCH (target: `Party` { `party_code`: toInteger(trim(row.`party_code`)) })
  MERGE (source)-[r: `MEMBER_OF`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Member` { `icpsr`: toInteger(trim(row.`icpsr`)) })
  MATCH (target: `Chamber` { `chamber`: row.`chamber` })
  MERGE (source)-[r: `SERVED_IN`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Member` { `icpsr`: toInteger(trim(row.`icpsr`)) })
  MATCH (target: `State` { `state_icpsr`: toInteger(trim(row.`state_icpsr`)) })
  MERGE (source)-[r: `REPRESENTS`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Member` { `icpsr`: toInteger(trim(row.`icpsr`)) })
  MATCH (target: `Congress` { `congress`: toInteger(trim(row.`congress`)) })
  MERGE (source)-[r: `SERVED_DURING`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;
