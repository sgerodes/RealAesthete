FROM real-aesthete-base:latest
# FROM real-aesthete-base-arm:latest

# use with:
# docker run -e SQLALCHEMY_DATABASE_URI=<db_uri> -e ACTIVATE_SPIDERS=ALL real-aesthete
# docker run -e SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@raspberrypisdextremeplus:5432/postgres -e IMMOWELT_SPIDER_RANDOM_DECLINE_RATE=0.5 -e ACTIVATE_SPIDERS=EbayFlatRentSpider -e POSTGRES_POOL_SIZE=200 -e POSTGRES_MAX_OVERFLOW=20 -it real-aesthete

# dockerize with:
# > docker build -t real-aesthete .
# > docker buildx build --platform=linux/arm/v7 -t real-aesthete-arm .

# copy with:
# docker save -o <path for generated tar file> <image name>
# scp real-aesthete-image pi@raspberrypisdextremeplus:real-aesthete-image.tar
# docker load -i <path to image tar file>

RUN mkdir -p /app
WORKDIR /app
COPY ./src/ ./src/
COPY ./configuration/ ./configuration/
COPY ./main.py ./main.py
CMD python3 main.py

# ENTRYPOINT python main.py