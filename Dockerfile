FROM ubuntu:16.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get upgrade -y -q
RUN apt-get install -y nano \
  wget \
  curl \
  python \
  python-dev \
  python-pip

RUN wget https://github.com/google/or-tools/releases/download/v4.3/or-tools.python.examples_4.3.3805.tar.gz && \
  tar -xzf or-tools.python.examples_4.3.3805.tar.gz && \
  cd ortools_examples && \
  python setup.py install --user && \
  cd .. && \
  rm -R ortools_examples && \
  rm or-tools.python.examples_4.3.3805.tar.gz

RUN mkdir /draft-kings-fun
COPY . /draft-kings-fun
RUN cd draft-kings-fun && ls && pip install -r requirements.txt
WORKDIR /draft-kings-fun

CMD ["/bin/bash"]