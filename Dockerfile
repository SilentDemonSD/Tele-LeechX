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

# Install RClone
RUN wget https://rclone.org/install.sh
RUN bash install.sh

# Install GClone-1.6.2 < https://github.com/l3v11/gclone >
#RUN wget -O /app/gautam/gclone.gz https://git.io/JJMSG
RUN wget -O /app/gclone/gclone.zip https://github.com/l3v11/gclone/releases/download/v1.62.2-purple/gclone-v1.62.2-purple-linux-amd64.zip
RUN cd gclone && unzip gclone.zip
RUN chmod 0775 /app/gclone

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash","start.sh"]
