FROM python:2.7.12-slim

ENV SERVER_DIR /opt/ceds/
ENV SRC_DIR miniredis/

COPY requirements.txt ./

# intalling all dependencies required
RUN pip install -r requirements.txt

# create folder for the code
RUN mkdir -p $SERVER_DIR
WORKDIR $SERVER_DIR
COPY $SRC_DIR $SERVER_DIR/$SRC_DIR
WORKDIR $SERVER_DIR/$SRC_DIR
# start server
ENTRYPOINT python server.py