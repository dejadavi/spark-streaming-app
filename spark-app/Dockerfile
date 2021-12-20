FROM openjdk:8-jdk


ENV GID=5000
ENV UID=5000
ENV UNAME=appuser


RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN apt-get update && apt-get install python3-pip wget  cron -y

RUN python3 -m pip install pyspark\
    pandas\
    click\
    mypy\
    pyarrow

RUN mkdir -p /opt/spark-app
RUN mkdir -p /local/logs

COPY *.py /opt/spark-app/

RUN chown -R  $GID:$UID /local/logs \
    && chown -R  $GID:$UID /tmp \
    && chown -R  $GID:$UID /opt/spark-app

RUN python3 -m pip install -e /opt/spark-app

CMD ['python', '/opt/spark-app/main.py']


