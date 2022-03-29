FROM ubuntu:18.04
MAINTAINER Shuai Liang "sliang@indocresearch.org"

RUN sed 's/main$/main universe/' -i /etc/apt/sources.list 
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential 
RUN pip3 install --upgrade pip
#libpg-dev, python-openssl required by psycopg2, secrets, respectively
RUN apt-get install -y libpq-dev 
RUN apt-get install libsasl2-dev libldap2-dev libssl-dev

# if build in the current folder
COPY ./ /app
# the path is different if using docker-compose in the parent folder
#COPY ./flask_app /app
WORKDIR /app
# have to install/upgrade pyopenssl separately
RUN pip install -U pyopenssl 
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
CMD ["run_server.sh"]


#  docker run -d -p 5000:5000 -v /home/sliang/hdp/tokenizer:/app --add-host=psql_server:10.3.10.100 sliang/tokenizer:v0.1 
