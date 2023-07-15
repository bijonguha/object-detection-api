FROM nvidia/cuda:11.7.1-base-ubuntu20.04

RUN apt-get -y update \
    && apt-get install -y software-properties-common \
    && apt-get -y update \
    && add-apt-repository universe \
    && apt-get -y update \
    && apt-get -y install python3.8-dev python3.8-distutils python3.8-venv \
    && apt-get -y install python3-pip

# RUN apt install python3.8-venv
RUN python3 -m venv /home/venv
RUN pip install -U pip
ENV PATH="/home/venv/bin:$PATH"

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt install -y sqlite3

COPY . /app
WORKDIR /app

RUN chmod a+x ./start

EXPOSE 9092
EXPOSE 8501
EXPOSE 3000

CMD ["sh","./start"]
