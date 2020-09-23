ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
ARG BUILD_ARCH

RUN \
   if [ "$BUILD_ARCH" = "armv7" ]; then wget https://github.com/fatedier/frp/releases/download/v0.32.1/frp_0.32.1_linux_arm.tar.gz && tar xvf frp_0.32.1_linux_arm.tar.gz && mv frp_0.32.1_linux_arm/frpc / && rm -rf frp_0.32.1_linux_arm.tar.gz frp_0.32.1_linux_arm ; \
   elif [ "$BUILD_ARCH" = "armhf" ]; then wget https://github.com/fatedier/frp/releases/download/v0.32.1/frp_0.32.1_linux_arm.tar.gz && tar xvf frp_0.32.1_linux_arm.tar.gz && mv frp_0.32.1_linux_arm/frpc / && rm -rf frp_0.32.1_linux_arm.tar.gz frp_0.32.1_linux_arm ; \
   elif [ "$BUILD_ARCH" = "aarch64" ]; then wget https://github.com/fatedier/frp/releases/download/v0.32.1/frp_0.32.1_linux_arm64.tar.gz && tar xvf frp_0.32.1_linux_arm64.tar.gz && mv frp_0.32.1_linux_arm64/frpc / && rm -rf frp_0.32.1_linux_arm64.tar.gz frp_0.32.1_linux_arm64 ; \
   elif [ "$BUILD_ARCH" = "amd64" ]; then wget https://github.com/fatedier/frp/releases/download/v0.32.1/frp_0.32.1_linux_amd64.tar.gz && tar xvf frp_0.32.1_linux_amd64.tar.gz && mv frp_0.32.1_linux_amd64/frpc / && rm -rf frp_0.32.1_linux_amd64.tar.gz frp_0.32.1_linux_amd64 ; \
   elif [ "$BUILD_ARCH" = "i386" ]; then wget https://github.com/fatedier/frp/releases/download/v0.32.1/frp_0.32.1_linux_386.tar.gz && tar xvf frp_0.32.1_linux_386.tar.gz && mv frp_0.32.1_linux_386/frpc / && rm -rf frp_0.32.1_linux_386.tar.gz frp_0.32.1_linux_386 ; \
   else echo 'NOT VALID BUILD'; exit 1; \
   fi

COPY run.sh /
RUN chmod a+x /run.sh

CMD ["/run.sh"]