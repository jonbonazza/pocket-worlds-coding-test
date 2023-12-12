# URL Shortener Take-Home Project
Welcome to the Pocket Worlds URL Shortener Take-Home Project! In this repository, we'd like you to demonstrate your
engineering skills by creating a small Python project that implements a URL Shortener web service.

This project will serve as the primary jumping off point for our technical interviews.

## Project Description
Using the provided Python project template, your task is to implement a URL Shortener web service that exposes
the following API endpoints:

* POST `/url/shorten`: accepts a URL to shorten (e.g. https://www.google.com) and returns a short URL that 
  can be resolved at a later time (e.g. http://localhost:8000/r/abc)
* GET `r/<short_url>`: resolve the given short URL (e.g. http://localhost:8000/r/abc) to its original URL
  (e.g. https://www.google.com). If the short URL is unknown, an HTTP 404 response is returned.

Your solution must support running the URL shortener service with multiple workers.

For example, it should be possible  to start two instances of the service, make a request to shorten a URL
to one instance, and be able to resolve that shortened URL by sending subsequent request to the second instance. 

## Getting Started

To begin the project, clone this repository to your local machine:

```commandline
git clone https://github.com/pocketzworld/url-shortener-tech-test.git
```

This repository contains a URL Shortener web service written in Python 3.11
using the [FastAPI](https://fastapi.tiangolo.com/) framework.

The API endpoints can be found in `server.py`.

A Makefile, Dockerfile, and docker-compose file are also included for your convenience to run and test the web service.

### Running the service

To run the web service in interactive mode, use the following command:
```commandline
make run
```

This command will build a new Docker image (`pw/url-shortener:latest`) and start the following:

1. a Mongodb instance
2. two instances of the URL shortening service.

By default, one web service instance will run on port 8000, while the other web service instance will run on port 8020.

### Testing

Swagger UI is available as part of the FastAPI framework that can be used to inspect and test
the API endpoints of the URL shortener. To access instance 1, go to http://localhost:8000/docs

from there you can generate a short URL and enter the URL that comes back in the response into your browser to be redirected to your target site.

You can also change the port in the resulting URL to `8020` and redirect to the same site from the other web service instance. For instance, if the
response from your URL shorten request comes back as `http://localhost:8080/1foobar`, then you can enter either that URL or  `http://localhost:8020/1foobar`
into your browser and be redirected to the same site.

## Additional Information
I've added several comments throughout the codebase regarding how I would change improve things if this were a production service, both from a code stand point, as well as an architecture stand point.
