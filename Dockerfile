FROM node:20

#TODO: python
# Install dependencies for building Python from source
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    curl \
    liblzma-dev \
    tk-dev \
    libgdbm-dev \
    libnss3-dev \
    libdb5.3-dev \
    libgdbm-compat-dev \
    libexpat1-dev

# Download and install Python 3.12.2
RUN wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz \
    && tar -xf Python-3.12.2.tgz \
    && cd Python-3.12.2 \
    && ./configure --enable-optimizations \
    && make -j $(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.12.2 \
    && rm Python-3.12.2.tgz

# Set Python 3.12.2 as the default python3 and pip3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3.12 1

RUN pip3 install scikit-learn==1.3.2

##TODO:

# copy from local project to Docker Container File System(DCFS) inside of the top-leve /tmp
ADD package.json /tmp/package.json

ADD package-lock.json /tmp/package-lock.json

# it runs in /src (whereas you can cd within docker by specifing the top-level folder like /tmp)
# the cd is specific for the current RUN
RUN cd /tmp && npm i

# will neglect ignored file and folders
ADD ./ /src 

RUN cp -a /tmp/node_modules /src/

# all subsequent commands will be running inside of /src, like the CMD ones
WORKDIR /src

# wouldn't start a shell session 
CMD ["node", "./index.js"]