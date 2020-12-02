# A Flask API with GIS Features

## Features

Check out [here](https://github.com/GHGSat/tech-challenge/blob/master/webdev/README.md#challenge-3-observation-management).

## Get It Running

### Development

1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    (Download [Docker](https://www.docker.com/products/docker-desktop))


2. Test it out at [http://localhost:5000](http://localhost:5000)

### Running Tests

### Test via Postman

(Download [Postman](https://www.postman.com/downloads/))

1. Create a new target:
    ```sh
    POST http://localhost:5000/new-target
    Body JSON sample:
    {
    	"name": "Mont-Tremblant",
    	"latitude": 68.1185,
    	"longitude": -40.5962,
    	"elevation": -220.23
	}	 
    ```