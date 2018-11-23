FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-wheel python3-six python3-pip

RUN mkdir /dk
COPY . /dk
WORKDIR /dk
RUN python3 -m pip install -r requirements.txt

CMD ["/bin/bash"]
