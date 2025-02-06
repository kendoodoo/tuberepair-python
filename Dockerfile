FROM nginxproxy/nginx-proxy:alpine AS cf-proxy

COPY cloudflare-ips-conf.sh proxy.conf ./
RUN chmod +x cloudflare-ips-conf.sh && ./cloudflare-ips-conf.sh
RUN mv allow-cf.conf proxy.conf /etc/nginx/conf.d/


######################
#     TUBEREPAIR     #
######################

FROM debian:stable
ARG TUBEREPAIR_USER_UID="2000"
ARG TUBEREPAIR_USER_GID="2000"
EXPOSE 80
EXPOSE 443
LABEL NAME="TubeRepair tuberepair.uptimetrackers.com blueprint"
LABEL VERSION="0.1 Beta"

COPY --chown=${TUBEREPAIR_USER_UID}:${TUBEREPAIR_USER_GID} ./requirements.txt /tuberepair-python/

RUN /bin/bash | \
    groupadd -g ${TUBEREPAIR_USER_GID} tuberepair && \
    useradd tuberepair -u ${TUBEREPAIR_USER_UID} -g ${TUBEREPAIR_USER_GID} && \
    apt-get update && \
    apt-get install python3 python3-pip wget --no-install-recommends -y && \
    cd /tuberepair-python && \
    pip3 install -r requirements.txt --break-system-packages && \
    apt-get clean

COPY --chown=${TUBEREPAIR_USER_UID}:${TUBEREPAIR_USER_GID} ./tuberepair /tuberepair-python

WORKDIR /tuberepair-python

USER tuberepair

ENTRYPOINT ["python3", "main.py"]