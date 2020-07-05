FROM python:3.6.4-jessie
#Create static and app paths. Install requirements and uwsgi package.
RUN mkdir -p /static && \
    mkdir -p /app && \
    pip install uwsgi && \
    apt-get update


# Install Node.js from the Debian-based distributions repository
RUN curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt install -y nodejs
RUN apt-get install -y redis-tools

## YARN INSTALL 
RUN echo "deb https://dl.yarnpkg.com/debian/ rc main" | tee /etc/apt/sources.list.d/yarn.list
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN apt remove -y cmdtest
RUN apt-get update

#Copy docker startup script and copy application code.
RUN pip install --upgrade pip
RUN pip install gevent
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy CODE
COPY . /app

# NOM RUN 
WORKDIR /app/seed/static/
RUN npm install
RUN npm run prod


## Default Workdir 
WORKDIR /app

#Expose application port.
EXPOSE 8001


#Run docker startup script.
CMD ["/app/docker-entrypoint.sh"]