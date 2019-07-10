FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y build-essential \
                    python3 \
                    python3-dev \
                    python3-pip
COPY ./ /opt/app
WORKDIR /opt/app

RUN pip3 install -r /opt/app/requirements.txt
EXPOSE 8443
CMD ["python3", "/opt/app/bot.py"]
