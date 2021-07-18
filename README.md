# Movie Rental API

## Description:

Movie Rental is an API where you can see movies which are available for rent, already rented movies. An authenticated user can rent movies for specified days and charged accordingly. An admin can perform CRUD operations on movies and has access to every endpoint.

## Getting Started:

### Prerequisites:

1. Developer should have python3 installed on the local machine along with pip3.
2. Postgresql database should be installed already along with psql.

### Installation

1. Enable virtual environment on local machine -

- run `python3 -m venv env`
- run `source env/bin/activate`

2. Install dependencies with `pip3`

- run `pip3 install -r requirements.txt`

3. Setup database (postgres):

- run `createdb rentalapi`

4. Run the server

- run `source setup.sh` to set environment variables.
- finally run `flask run --reload` to start local server.

## Tests:

To setup tests follow these steps -

- run `dropdb rentalapi_test` to clear the db.
- run `createdb rentalapi_test` to create a fresh db.
- run `source setup.sh` to set configs.
- finally run the tests by `python3 test_app.py`

> NOTE: Repeat above steps everytime you run tests.

# API reference

## Getting Started

### Base URL : `https://movie-rentalapi.herokuapp.com/`

### API keys

The required token are in the `setup.sh` file and are already set in installation steps.

## Error

Errors are handled well and they are sent as JSON objects. Example of an Error response -

```python
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }
```

Every error response includes `"success": false`, error code in `error` key and message in `message` key.

Other error response includes -

- 400: "bad request"
- 405: "method not allowed"
- 422: "unprocessable"

## Request Endpoints

> NOTE: `/` endpoint is only for testing.

### GET `/movies`

- Fetches all the movies from database and returns a list of dictionaries with two key value pairs

- Request arguments: None

- Returns: An JSON object with - `success`: True or False, movies: contains all movies.

- Response Example - (`curl 'https://movie-rentalapi.herokuapp.com/movies'`)

```python
{
  "movies": [
    {
      "id": 4,
      "movie_name": "Intersteller",
      "price": 100
    }
  ],
  "success": true
}
```

### GET `/rented-movies`

- Fetches and returns list of rented movies and their prices.

- Request arguments: None

- Returns: An JSON object with - `success`, `movies`: list of dictionaries of movies.

- Response Example - (`curl 'https://movie-rentalapi.herokuapp.com/rented-movies'`)

```python
{
  "movies": [
    {
      "charges": 2000,
      "id": 4,
      "movie": {
        "id": 4,
        "movie_name": "Avengers Endgame",
        "price": 400
      },
      "movie_id": 4
    },
    {
      "charges": 200,
      "id": 5,
      "movie": {
        "id": 6,
        "movie_name": "Inception",
        "price": 100
      },
      "movie_id": 6
    }
  ],
  "success": true
}
```

### POST `/create-movie`

- Used to post a new movie. It takes JSON object in request body with following properties - `movie_name`, `price`.

- Request Arguments: None

- Returns: An JSON object with keys `success`, `movie`.

- Response Example - (`curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <admin_token>" -d '{"movie_name": "Iron Man", "price": 100' 'https://movie-rentalapi.herokuapp.com/create-movie'`)

```python
{
  "movie": {
    "id": 8,
    "movie_name": "Iron Man",
    "price": 100
  },
  "success": true
}
```

### POST `/rent-movie`

- Rents a movie based on the `movie_id` provided in request body along with `days` to calculate pricing.

- Request Arguments: None

- Returns: An JSON object with - `success` and `rented_movie` keys.

- Response Example - (`curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"movie_id": 1, "days": 5}' 'https://movie-rentalapi.herokuapp.com/rent-movie'`)

```python
{
  "rented_movie": {
    "charges": 500,
    "id": 2,
    "movie": {
        "id": 4,
        "movie_name": "Inception",
        "price": 100
    },
    "movie_id": 4
    },
  "success": true
}
```

### PATCH `/movie/<id>`

- Update a movie based on either `movie_name, price` or both parameters.

- Request arguments: `id` of the movie to be updated.

- Returns: An JSON object with keys `success` and `movie` object.

- Response Example - (`curl -X PATCH -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"movie_name": "Avengers Endgame", "price": 400}' 'https://movie-rentalapi.herokuapp.com/movie/4'`)

```python
{
  "movie": {
    "id": 4,
    "movie_name": "Avengers Endgame",
    "price": 400
  },
  "success": true
}
```

### DELETE `/movie/<id>`

- Delete a movie by id provided in request argument.

- Request argument: `id` The id of the movie.

- Returns: An JSON object with keys `success` and `id` of the movie

- Response Example - (`curl -X DELETE -H "Authorization: Bearer <token>" 'https://movie-rentalapi.herokuapp.com/movie/8'`):

```python
{
  "id": 8,
  "success": true
}
```

## Deployment

This project is deployed on heroku: `https://movie-rentalapi.herokuapp.com/`

## Authors

Abhishek Jain
