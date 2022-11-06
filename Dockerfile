FROM 412314/mltb:heroku

RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt -qq update --fix-missing && \
    apt -qq install -y \
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
    mediainfo

RUN wget https://rclone.org/install.sh
RUN bash install.sh

RUN mkdir /app/gautam
RUN wget -O /app/gautam/gclone.gz https://git.io/JJMSG
RUN gzip -d /app/gautam/gclone.gz
RUN chmod 0775 /app/gautam/gclone

RUN pip install -U pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash","start.sh"]
