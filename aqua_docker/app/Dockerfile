FROM python:3.6-onbuild

# Install essential packages
RUN pip install --upgrade pip && \
    pip3 install sanic

#RUN pip3 install /usr/src/app/aqua

# Install PyTorch for Stanza
#RUN pip3 install https://download.pytorch.org/whl/cpu/torch-1.7.0%2Bcpu-cp36-cp36m-linux_x86_64.whl

#RUN pip3 install stanza && \
#    mv /usr/src/app/resources/stanza_resources /root

# Install NLIMED
#RUN pip3 install /usr/src/app/nlimed && \
#    NLIMED --config --apikey "fc5d5241-1e8e-4b44-b401-310ca39573f6" --corenlp-home "/usr/src/app/resources/stanford"

# Install nltk
#RUN python3 -m nltk.downloader averaged_perceptron_tagger && \
#    rm  /root/nltk_data/taggers/*zip && \
#    python3 -m nltk.downloader wordnet && \
#    rm  /root/nltk_data/corpora/*zip && \
#    rm -r /root/.cache
#    # --no-cache-dir --compile --global-option=build_ext <-- use this on pip for final version

# Install Java
#RUN apt-get update
#RUN apt-get install -y apt-utils build-essential gcc

#ENV JAVA_FOLDER java-se-8u41-ri

#ENV JVM_ROOT /usr/lib/jvm

#ENV JAVA_PKG_NAME openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz
#ENV JAVA_TAR_GZ_URL https://download.java.net/openjdk/jdk8u41/ri/$JAVA_PKG_NAME

#RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*    && \
#    apt-get clean                                                               && \
#    apt-get autoremove                                                          && \
#    echo Downloading $JAVA_TAR_GZ_URL                                           && \
#    wget -q $JAVA_TAR_GZ_URL                                                    && \
#    tar -xvf $JAVA_PKG_NAME                                                     && \
#    rm $JAVA_PKG_NAME                                                           && \
#    mkdir -p /usr/lib/jvm                                                       && \
#    mv ./$JAVA_FOLDER $JVM_ROOT                                                 && \
#    update-alternatives --install /usr/bin/java java $JVM_ROOT/$JAVA_FOLDER/bin/java 1        && \
#    update-alternatives --install /usr/bin/javac javac $JVM_ROOT/$JAVA_FOLDER/bin/javac 1     && \
#    java -version
