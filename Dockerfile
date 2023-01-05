FROM python:3.7.12-slim

# Copy as early as possible so we can cache ...
COPY requirements_cloud.txt .

# Install common libraries
RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    stunnel \
 && apt-get autoremove -y

RUN apt-get -y install libzbar-dev

# Install all required build libraries
RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    build-essential
    
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\ 
    'libsm6'\ 
    'libxext6' -y

# For the "failed call to cuInit" error
ENV CUDA_VISIBLE_DEVICES 0

# Make sure we have the latest pip version
RUN pip install -U pip
RUN apt install git -y

# Install dependencies
RUN pip install --no-cache-dir -r requirements_cloud.txt
RUN apt install -y sqlite3

COPY . /

RUN chmod a+x /start

EXPOSE 9092
EXPOSE 8501
EXPOSE 3000

CMD ["sh","./start"]
