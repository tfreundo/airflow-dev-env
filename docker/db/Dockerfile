FROM mongo:latest
WORKDIR /home
RUN  apt-get update \
  && apt-get install -y wget
# Download the sample dataset
RUN wget http://media.mongodb.org/zips.json
