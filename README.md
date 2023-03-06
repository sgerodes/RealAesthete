To connect to raspberry us 
```zsh
ssh pi@raspberrypisdextremeplus
```

# Run
Run the docker image on the raspberry:
```zsh
docker run -e SQLALCHEMY_DATABASE_URI=<db_uri> -e ACTIVATE_SPIDERS=ALL real-aesthete
```
E.g.:
```zsh
docker run -e SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@raspberrypisdextremeplus:5432/postgres -e IMMOWELT_SPIDER_RANDOM_DECLINE_RATE=0.5 -e ACTIVATE_SPIDERS=EbayFlatRentSpider -e POSTGRES_POOL_SIZE=200 -e POSTGRES_MAX_OVERFLOW=20 -it real-aesthete
```

# Dokerize
## Base image
```zsh
docker build -t real-aesthete-base -f Dockerfile-base .
```
```zsh
docker buildx build --platform=linux/arm/v7 -t real-aesthete-base-arm -f Dockerfile-base .
```

## Full image
```zsh
docker build -t real-aesthete .
```
```zsh
docker buildx build --platform=linux/arm/v7 -t real-aesthete-arm .
```

# Copy with
```zsh
docker save -o <path for generated tar file> <image name>
scp real-aesthete-image pi@raspberrypisdextremeplus:real-aesthete-image.tar
docker load -i <path to image tar file>
```
