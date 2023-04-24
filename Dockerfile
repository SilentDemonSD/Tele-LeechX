FROM codewithweeb/weebzone:stable

RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt-get -qq update --fix-missing && \
    apt-get -qq install -y \
    git \
    wget \
    curl \
    busybox \
    unzip \
    unrar \
    tar \
    python3 \
    python3-pip \
    p7zip-full \
    p7zip-rar \
    pv \
    jq \
    python3-dev \
    mediainfo \
    mkvtoolnix

RUN wget https://rclone.org/install.sh
RUN bash install.sh

RUN mkdir /app/gautam
RUN wget -O /app/gautam/gclone.gz https://git.io/JJMSG
RUN gzip -d /app/gautam/gclone.gz
RUN chmod 0775 /app/gautam/gclone

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash","start.sh"]

EXPOSE 80
