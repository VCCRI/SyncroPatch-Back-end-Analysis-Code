
FROM python:3.8.10-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python-tk \
    && rm -rf /var/lib/apt/lists/*

# WORKDIR /SyncroPatch-Back-end-Analysis-Code
# RUN git clone https://github.com/VCCRI/SyncroPatch-Back-end-Analysis-Code.git


COPY ./requirements.txt /pip/requirements.txt

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r /pip/requirements.txt --no-cache-dir

RUN pip install numpy==1.21.2 --no-cache-dir

WORKDIR /SyncroPatch-Back-end-Analysis-Code
# ENTRYPOINT [ "python3" ] 