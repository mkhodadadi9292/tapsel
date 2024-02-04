# Project Name

A brief description of your project.

## Endpoints

### /predict

Description of the `/predict` endpoint.

#### Request

- **Method**: GET
- **Path**: `/predict`
- **Query Parameters**:
  - `ids` (List of Integers): List of primary keys.

#### Response

Describe the expected response from the `/predict` endpoint.

### /stat

Description of the `/stat` endpoint.

#### Request

- **Method**: GET
- **Path**: `/stat`
- **Query Parameters**: (if any)

#### Response

Describe the expected response from the `/stat` endpoint.

## MongoDB Collections

- **CTR**: Collection for the `/predict` endpoint.
- **prediction_stats**: Collection for the `/stat` endpoint.

## `seed_data.py`

The `seed_data.py` script is responsible for populating MongoDB with initial data. It reads data from a CSV file (`task-23-dataset.csv`) and inserts it into the specified collections.

/predict Endpoint Caching
The /predict endpoint utilizes a caching mechanism to improve performance. The cachetools library is used to cache responses based on the input parameters.

### Caching Strategy
Cache Key Generation: The cache key is dynamically generated based on the hash of the tuple of ids (list of primary keys).
Cache TTL (Time-to-Live): The cache is configured with a TTL of 60 seconds.
Usage
When a request is made to the /predict endpoint with the same set of ids within the cache TTL, the cached response is returned. If the ids are not found in the cache, the prediction logic is executed, and the result is stored in the cache for future requests.

### MongoDB Connection

The script connects to MongoDB using the provided `mongo_uri` and inserts data into the specified collections (`CTR` and `prediction_stats`).

### Usage
Running the Services

run `docker-compose up -d`


