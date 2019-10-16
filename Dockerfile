FROM continuumio/miniconda3

LABEL maintainer="Anton Korosov <anton.korosov@nersc.no>"
LABEL purpose="Python libs for developing and running Nansat"

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/src

RUN apt-get update \
&&  apt-get install -y --no-install-recommends \
    build-essential \
    gcc

RUN conda config --add channels conda-forge  \
&&  conda install -y \
    ipython \
    ipdb \
    gdal=2.4.2 \
    matplotlib \
    mock \
    netcdf4 \
    nose \
    numpy \
    pillow \
    python-dateutil \
    scipy \
    urllib3 \
&&  conda remove qt pyqt --force \
&&  conda clean -a -y \
&&  rm /opt/conda/pkgs/* -rf \
&&  pip install pythesint \
&&  python -c 'import pythesint; pythesint.update_all_vocabularies()'

RUN wget -nc -P /usr/share/MOD44W ftp://ftp.nersc.no/nansat/test_data/MOD44W.tgz \
&&  tar -xzf /usr/share/MOD44W/MOD44W.tgz -C /usr/share/MOD44W/ \
&&  rm /usr/share/MOD44W/MOD44W.tgz

#RUN pip install coverage

#ENV MOD44WPATH=/usr/share/MOD44W/

#COPY utilities /tmp/utilities
#COPY nansat /tmp/nansat
#COPY setup.py /tmp/
#WORKDIR /tmp
#RUN python setup.py install

#WORKDIR /src

