FROM Python:3.9

LABEL module.name="SyncroPatch-Back-end-Analysis-Code"
LABEL module.description="SyncroPatch-Back-end-Analysis-Code"
LABEL module.version="v0.0.1"

RUN apt get update && apt get install -y --no-install-recommends \
    git 

WORKDIR /app
# RUN git clone https://github.com/VCCRI/SyncroPatch-Back-end-Analysis-Code.git

COPY "../requirements.txt" "/app/SyncroPatch-Back-end-Analysis-Code/requirements.txt"

WORKDIR /app/SyncroPatch-Back-end-Analysis-Code/

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]