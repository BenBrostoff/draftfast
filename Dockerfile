FROM ubuntu

RUN apt-get clean
RUN apt-get -y update
RUN apt-get install -y apt-transport-https && apt-get install -y vim python3 python3-pip python3-wheel python3-six python3-pip

RUN mkdir /dk
COPY . /dk
WORKDIR /dk
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install autopep8

CMD ["/bin/bash"]
