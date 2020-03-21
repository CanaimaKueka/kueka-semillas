FROM dockershelf/debian:sid
LABEL maintainer "Luis Alejandro Martínez Faneyth <luis@collagelabs.org>"

RUN apt-get update && \
    apt-get install net-tools netcat-openbsd gnupg aptitude

RUN route -n | awk '/^0.0.0.0/ {print $2}' > /tmp/host_ip.txt
RUN echo "HEAD /" | nc `cat /tmp/host_ip.txt` 8000 | grep squid-deb-proxy \
    && (echo "Acquire::http::Proxy \"http://$(cat /tmp/host_ip.txt):8000\";" > /etc/apt/apt.conf.d/30proxy) \
    || echo "No squid-deb-proxy detected on docker host"

RUN apt-get update && \
    apt-get install python3 \
                    bash \
                    git-core \
                    gettext \
                    debhelper \
                    devscripts \
                    dpkg-dev \
                    git-buildpackage \
                    lintian \
                    gnupg \
                    coreutils \
                    tar \
                    devscripts \
                    python3-sphinx \
                    imagemagick \
                    python3-docutils \
                    gettext \
                    icoutils \
                    libmagickcore-extra \
                    librsvg2-bin