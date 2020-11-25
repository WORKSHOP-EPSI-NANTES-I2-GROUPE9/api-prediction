<h1 align="center">Welcome to api-prediction 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
</p>

> predicts whether a sentence is negative or not

## Prerequisites

- Add a model file (.h5) into /src/
- Add a tokenizer file into /src/

## Run

```sh
python ./server.py
```

try something like this to test api
```sh
curl -i -X POST -H "Content-Type: application/json" -d "{\"message\":\"hello bob, how are you?\"}" http://localhost:5000/api/v1/analyses
```

## Docker

Build image
```sh
docker build -t api-prediction .
```

Run image
```sh
docker run -i --rm -p 5000:5000 api-prediction
```

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_