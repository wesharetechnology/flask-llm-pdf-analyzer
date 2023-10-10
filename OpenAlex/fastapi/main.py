from fastapi import FastAPI
import requests
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
def search_id(author_id: str):
    """search for the author name in OpenAlex, such as url = "https://api.openalex.org/works?filter=author.id:A5043842990"""

    url = "https://api.openalex.org/works?filter=author.id:" + author_id
    # find connections by concept
    # find connections by work
    # find connections by author
    # find connections by institution
    results = requests.get(url).json()["results"]
    for result in results:
        print(result["authorships"])
