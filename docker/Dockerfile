FROM python:3

RUN mkdir /src
WORKDIR /src

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

RUN useradd -m -d /home/iron_bank -b /bin/bash iron_bank 
USER iron_bank 

CMD ["python3", "/src/server.py"]

