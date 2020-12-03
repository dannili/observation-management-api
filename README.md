# A Flask API with GIS Features

## Features

Check out [here](https://github.com/GHGSat/tech-challenge/blob/master/webdev/README.md#challenge-3-observation-management).

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


3. Quickly test it out at [http://localhost:5000](http://localhost:5000)

### Try via Postman

(Download [Postman](https://www.postman.com/downloads/))

1. Create a new target:
    ```sh
    POST http://localhost:5000/targets
    Body JSON sample:
    {
        "name": "Mont-Tremblant",
        "latitude": 46.1185,
        "longitude": 74.5962,
        "elevation": 875
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
### Running Tests
