FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get -y install busybox-static
COPY crontab /var/spool/cron/crontabs/root
RUN chmod +x ./HORSE_called_making_data_for_dango.sh ./HORSE_making_all_data_for_dango.sh
CMD ["busybox", "crond", "-l", "8", "-L", "/var/log/crond.log", "-f"]