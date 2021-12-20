FROM python:latest

ENV GID=5000
ENV UID=5000
ENV UNAME=appuser

USER root

RUN apt-get update && apt-get install awscli cron  wget -y

RUN mkdir -p /opt/scripts && mkdir -p /etc/cron.d
RUN mkdir -p /local/logs

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

COPY copy_logs.sh /opt/scripts/copy_logs.sh
COPY cronjob  /etc/cron.d/cronjob

RUN chown -R $GID:$UID /opt/scripts/copy_logs.sh &&\
    chown -R  $GID:$UID /local/logs &&\
    chmod +x /opt/scripts/copy_logs.sh &&\
    chmod 0644 /etc/cron.d/cronjob

# Apply cron job
RUN crontab /etc/cron.d/cronjob

CMD cron