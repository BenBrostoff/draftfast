FROM python:3.6

RUN apt-get update && apt-get install -y --no-install-recommends vim

#RUN wget https://github.com/google/or-tools/releases/download/v4.3/or-tools.python.examples_4.3.3805.tar.gz && \
#  tar -xzf or-tools.python.examples_4.3.3805.tar.gz && \
#  cd ortools_examples && \
#  python setup.py install --user && \
#  cd .. && \
#  rm -R ortools_examples && \
#  rm or-tools.python.examples_4.3.3805.tar.gz

RUN mkdir /dk
COPY . /dk
RUN cd dk && ls && pip install -r requirements.txt
WORKDIR /dk

CMD ["/bin/bash"]
