FROM openjdk:8-jdk


ENV GID=5000
ENV UID=5000
ENV UNAME=appuser
ENV PATH=$PATH:/usr/local/lib
ENV SPARK_LOCAL_DIRS=/tmp

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN apt-get update && apt-get install python3-pip wget  cron -y

RUN python3 -m pip install pyspark\
    pandas\
    click\
    mypy\
    pyarrow

RUN mkdir -p /opt/spark_app &&\
    mkdir -p /local/logs &&\
    mkdir -p /tmp/spark-tmp &&\
    mkdir -p /tmp/spark-warehouse

COPY *.py /opt/spark_app/

RUN chown -R  $GID:$UID /local/logs \
    && chown -R  $GID:$UID /tmp \
    && chown -R  $GID:$UID /opt/spark_app


USER $GID:$UID
ENV PATH=$PATH:/usr/local/lib:/home/appuser/.local/bin


WORKDIR /opt/spark_app
RUN python3 -m pip install -e .
RUN export PATH=$PATH:/usr/local/lib:/home/appuser/.local/bin
RUN export SPARK_LOCAL_DIRS=/tmp
WORKDIR /home/appuser
CMD ["spark-app", "run",]

