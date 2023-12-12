from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from encoder import ShortURLEncoder
from repo import URLRepository, DBInfo
from pymongo.errors import OperationFailure
import os

encoder = ShortURLEncoder()
db_info = DBInfo(os.getenv("DB_NAME"), os.getenv("DB_HOST"), int(os.getenv("DB_PORT")))
repo = URLRepository(encoder, db_info)
app = FastAPI(debug=True)
base_url: str = os.getenv("BASE_URL")


class ShortenRequest(BaseModel):
    url: str


@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be later resolved to the originally
    specified URL.
    """
    short_url : str
    try:
        short_url = repo.register(request.url)
    except OperationFailure as e:
        return HTTPException(status_code=500, detail=e.details)

    return {"short_url": f"{base_url}/r/{short_url}"}

class ResolveRequest(BaseModel):
    short_url: str


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    
    In swagger, this route doesnt work. It seems swagger doesnt understand
    how to handle 307 redirect responses. It might be something with our
    swagger config, but it seems that's being auto generated, so I'm not
    entirely certain how to go about modifying that. If this were a
    production system, I would spend some time investigating this, but
    for this demo, if you paste the whole URL into a browser, it works fine.
    """
    url = repo.retrieve(short_url)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found.")

    return RedirectResponse(url)


@app.get("/")
async def index():
    return "Your URL Shortener is running!"
