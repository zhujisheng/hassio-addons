ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install
RUN apt-get update
RUN apt-get install -y libasound2-plugins python3 python3-distutils portaudio19-dev python3-pyaudio wget flac
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN pip3 install requests fuzzywuzzy

# precise-engine
ARG BUILD_ARCH

RUN \
   if [ "$BUILD_ARCH" = "armv7" ]; then wget https://github.com/MycroftAI/mycroft-precise/releases/download/v0.3.0/precise-engine_0.3.0_armv7l.tar.gz && tar xvf precise-engine_0.3.0_armv7l.tar.gz && rm precise-engine_0.3.0_armv7l.tar.gz ; \
   elif [ "$BUILD_ARCH" = "armhf" ]; then wget https://github.com/MycroftAI/mycroft-precise/releases/download/v0.3.0/precise-engine_0.3.0_armv7l.tar.gz && tar xvf precise-engine_0.3.0_armv7l.tar.gz && rm precise-engine_0.3.0_armv7l.tar.gz ; \
   elif [ "$BUILD_ARCH" = "aarch64" ]; then wget https://github.com/MycroftAI/mycroft-precise/releases/download/v0.3.0/precise-engine_0.3.0_aarch64.tar.gz && tar xvf precise-engine_0.3.0_aarch64.tar.gz && rm precise-engine_0.3.0_aarch64.tar.gz ; \
   elif [ "$BUILD_ARCH" = "amd64" ]; then wget https://github.com/MycroftAI/mycroft-precise/releases/download/v0.3.0/precise-engine_0.3.0_x86_64.tar.gz && tar xvf precise-engine_0.3.0_x86_64.tar.gz && rm precise-engine_0.3.0_x86_64.tar.gz ; \
   else echo 'NOT VALID BUILD'; exit 1; \
   fi

# copy
COPY *.pb /
COPY *.pb.params /

RUN mkdir /process_programs
COPY /process_programs/* /process_programs/

COPY runner.py /
COPY run.py /

RUN mkdir /audio
COPY ding.wav /audio/
COPY dong.wav /audio/

# daemon
RUN chmod a+x /run.py

COPY run.sh /
RUN chmod a+x /run.sh
CMD ["/run.sh"]

#CMD ["/run.py"]
