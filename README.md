# A Flask API with GIS Features

## Features

The API currently supports the following endpoints:

1. Target creation
2. Save image to an existing target
3. Search targets by a bounding box


## Get It Running

### Development

1. Clone
    ```sh
    $ git clone https://github.com/dannili/observation-management-api.git
    ```

2. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    (Download [Docker](https://www.docker.com/products/docker-desktop))

3. Create a database using the cli tool:
    ```sh
    $ docker-compose exec web python run.py create_db
    ```

4. Check [http://localhost:5000](http://localhost:5000) to see if server is up running.

### Try via Postman

(Download [Postman](https://www.postman.com/downloads/))

1. Create a new target:
    ```sh
    POST http://localhost:5000/targets
    Body JSON sample:
    {
        "name": "Mont-Tremblant",
        "latitude": 68.1185,
        "longitude": -40.5962,
        "geomerty": "point(-40.5962 68.1185)",
        "elevation": 875.0
    } 
    ```

2. Save image and capture time to an existing target:
    ```sh
    PATCH http://localhost:5000/targets/1
    Body JSON sample:
    {
        "image": "upload.wikimedia.org/wikipedia/commons/6/6b/Mont_Tremblant%2C_Quebec_%286903201864%29.jpg",
        "image_timestamp": "2020-12-02 19:03:30"
	}	 
    ```
3. Search by a bounding box:
    ```sh
    GET http://localhost:5000/targets/search
    Body JSON sample:
    {
        "xmin": -141.00275,
        "ymin": 41.6765556,
        "xmax": -30.3231981,
        "ymax": 83.3362128
    } 
    ```

### Running Tests
