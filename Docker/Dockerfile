FROM Python:3.9

LABEL key="value"
version value="0.1"

RUN apt get update && apt get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    git 

WORKDIR /app
# RUN git clone https://github.com/VCCRI/SyncroPatch-Back-end-Analysis-Code.git

COPY "../requirements.txt" "/app/SyncroPatch-Back-end-Analysis-Code/requirements.txt"

WORKDIR /app/SyncroPatch-Back-end-Analysis-Code/

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]