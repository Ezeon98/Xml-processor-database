#
FROM python:3.9
LABEL maintainer="Agustin Wisky. <a.wisky@patagon.io>"

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

#install ohmybash
RUN bash -c "$(wget --progress=dot:giga https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh -O -)"

# Install debugpy and jupyterlab
RUN pip3 install --no-cache-dir --upgrade pip==22.1.2 \
        debugpy==1.6.2\
        jupyterlab==3.4.3


ENV PYTHONUNBUFFERED 1
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./database /code/database
RUN mkdir /mnt/downloads
USER root

# Jupyter Lab
EXPOSE 8888
# Debugpy
EXPOSE 3003

COPY bootstrap.sh /etc/bootstrap.sh
RUN chmod a+x /etc/bootstrap.sh
COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py
RUN chmod a+x /usr/local/bin/wait-for-psql.py

CMD ["/etc/bootstrap.sh"]