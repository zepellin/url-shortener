# URL shortener

This service implements an endpoint for generating shortened links. Following endpoints are supported:

Generate site identifier identifying provided URL:
```bash
$ curl -XPOST "localhost:5001/api/v1/shorten/https://gooogle.com?format=json"
{"status": "OK", "request_url": "https://gooogle.com", "identifier": 1204225829}

```
Retrieving URL from provided identifier:
```bash
$ curl "localhost:5001/api/v1/lookup/1204225829?format=json"
{"status": "OK", "request_url": "https://gooogle.com", "identifier": "1204225829"}

```
Performing HTTP redirect when identifier is supplied in apps base path:
```bash
url "localhost:5001/1204225829" -v
..
< HTTP/1.0 302 FOUND
< Content-Type: text/html; charset=utf-8
< Location: https://gooogle.com
...

```

# Achitectural choices
* Given time constraints, an in memory python dictionary object is used to store mapping of URLs to generated identifiers
* Please refer to comments in main app.py file, it contains more insight into app's functionality

# Build and deploy
The application is intended to run in a docker container. To build:
```bash
docker build --tag url-shortener . 

```
The application is then run exposing an example port 5001 as it's API endpoint:
```bash
docker run --publish 5001:5001 url-shortener
```