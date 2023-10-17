"""
I have a json file in a following format:
```
{
    "publication": [
		{
	    	"doi": "doi of the publication",
		    "titles": "titles of the publication",
		    "coauthors":[
                {
                    "id": "id of the coauthor",
                    "display_name": "name of the coauthor",
                    "orcid": "orcid of the coauthor"
                }
            ]
		}
	]
}
```
I want to construct a Neo4j graph that has a structure
```
Author{"id": "id of the coauthor","display_name": "name of the coauthor", "orcid": "orcid of the coauthor"} -[:HAS_PUBLICATION]->Author{"id": "id of the coauthor","display_name": "name of the coauthor","orcid": "orcid of the coauthor"}
```
please write a python code to construct the Neo4j graph
"""
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import json


def construct_graph(data):

    # Connect to the Neo4j database
    uri = "neo4j+s://e9358041.databases.neo4j.io"
    username = "neo4j"  # Update with your Neo4j username
    load_dotenv()
    # Update with your Neo4j password
    password = os.getenv("NEO4J_PASSWORD")
    print(password)
    db_driver = GraphDatabase.driver(uri, auth=(username, password))

    # Create a Neo4j session
    with db_driver.session() as session:
        # Iterate over the publications in the JSON data
        for publication in data:
            # Create the publication node
            query = """
            MERGE (p:Publication {titles: $titles, paper_id: $paper_id})
            """
            try:
                session.run(query,
                            titles=publication['title'],
                            paper_id=publication['paper_id'])
            except:
                pass

            # Iterate over the coauthors of the publication
            if publication['coauthors'] is not None:
                for coauthor in publication['coauthors']:
                    # Create the coauthor node
                    query = """
                    MERGE (a:Author {id: $id, display_name: $display_name})
                    """
                    session.run(
                        query, id=coauthor['id'], display_name=coauthor['display_name'])

                    # Create the relationship between the coauthor and the publication
                    query = """
                    MATCH (a:Author {id: $id}), (p:Publication {paper_id: $paper_id})
                    MERGE (a)-[:HAS_PUBLICATION]->(p)
                    """
                    session.run(query, id=coauthor['id'],
                                paper_id=publication['paper_id'])
