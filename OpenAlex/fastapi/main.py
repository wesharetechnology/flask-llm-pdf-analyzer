from fastapi import FastAPI
import requests
from construct_graph import construct_graph
from download_doi import GetDownloadUrl, DownloadFileByUrl
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# make an api call to OpenAlex


@app.get("/author/{author_name}")
def search_author(author_name: str):
    """search for the author name in OpenAlex, such as https://api.openalex.org/authors?filter=display_name.search:john%20smith"""

    url = "https://api.openalex.org/authors?filter=display_name.search:"+author_name

    return requests.get(url).json()

# how to spot a specific person based on the institution and name?


@app.get("/id/{author_id}")
def search_id(author_id: str, n: int = 2):
    """search for the author name in OpenAlex, such as url = "https://api.openalex.org/works?filter=author.id:A5043842990"""
    if n == 0:
        return
    else:
        url = "https://api.openalex.org/works?filter=author.id:" + author_id
        # find connections by concept
        # find connections by work
        # find connections by author
        # find connections by institution
        # construct a graph that shows the connections between the author and their co-authors
        relations = []
        doi_list = []
        results = requests.get(url).json()["results"]
        for result in results:

            publication = {
                "paper_id": result["id"],
                "doi": result["doi"],
                "title": result["title"],
                "coauthors": []
            }
            for authorship in result["authorships"]:
                publication["coauthors"].append(authorship["author"])
            relations.append(publication)
        # print(relations)
        # construct_graph(relations)
        for relation in relations:
            for coauthor in relation["coauthors"]:
                next_relations = search_id(coauthor["id"], n-1)
                if next_relations:
                    relations.extend(next_relations)
                # print(search_id(coauthor["id"], n-1))

    return relations


@app.get("/publication/{publication_id}")
def search_doi(author_id: str, n: int = 2):
    """search for publication ID, download its PDF using sci-hub"""
    relations = search_id(author_id, n)
    print(relations)
    # doi_EnglishPaper = 'https://doi.org/10.1038/nature07970'
    # paperDownloadUrl = GetDownloadUrl(doi_EnglishPaper)  # doi
    # DownloadFileByUrl(paperDownloadUrl)
    for relation in relations:
        try:
            paperDownloadUrl = GetDownloadUrl(relation["doi"])  # doi
            DownloadFileByUrl(paperDownloadUrl)
        except:
            print("Download failed:" + relation["doi"])
