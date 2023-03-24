FROM python:3.9.16

WORKDIR /app
# RUN git clone https://github.com/VCCRI/SyncroPatch-Back-end-Analysis-Code.git

COPY ./requirements.txt /app/SyncroPatch-Back-end-Analysis-Code/requirements.txt

WORKDIR /app/SyncroPatch-Back-end-Analysis-Code/

RUN pip install -r requirements.txt --no-cache-dir

# CMD ["python", "main.py"]