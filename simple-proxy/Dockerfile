ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add python3 iptables

# Copy data for add-on
COPY tcp_proxy_encoded.py /
RUN chmod a+x /tcp_proxy_encoded.py

CMD ["/tcp_proxy_encoded.py"]