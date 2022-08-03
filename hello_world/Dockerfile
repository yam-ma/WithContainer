FROM continuumio/miniconda3

# COPY app.py requirements.txt ./
COPY app.py requirements.txt MSM_template.grb ./

RUN python3.9 -m pip install -r requirements.txt -t .

SHELL ["/bin/bash", "-c"]

ENV PATH /opt/conda/envs/env/bin:.:$PATH

# install libraries
ADD conda_env.yml /tmp/conda_env.yml
ADD requirements.txt /tmp/requirements.txt
RUN apt update && apt install -y libgl1-mesa-glx && \
    conda config --append channels conda-forge && \
    conda env create -f /tmp/conda_env.yml && \
    echo "source activate storm0" > ~/.bashrc && \
    conda clean -a -y
RUN source activate storm0 && \
    apt install -y build-essential && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/* && apt-get purge -y --auto-remove gcc gfortran build-essential

# install wgrib2 v3.0.2
RUN apt update && apt install build-essential gfortran -y --no-install-recommends && \
    wget -O /tmp/wgrib2.tgz https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v3.0.2 && \
    cd /tmp && tar -zxvf wgrib2.tgz && cd grib2 && \
    sed -i 's/MAKE_SHARED_LIB=0/MAKE_SHARED_LIB=1/' makefile && \
    export CC=gcc && export FC=gfortran && make && make lib && \
    mv wgrib2/wgrib2 /usr/local/bin/ && \
    mv lib/libwgrib2.so /opt/conda/envs/storm0/lib/python3.9/site-packages/ && \
    wget -O /tmp/pywgrib2_s.tgz  "https://ftp.cpc.ncep.noaa.gov/wd51we/pywgrib2_s/pywgrib2_s.tgz" && \
    cd /tmp && tar -zxvf pywgrib2_s.tgz && mv pywgrib2_s/pywgrib2_s.py /opt/conda/envs/storm0/lib/python3.9/site-packages/ && \
    rm -rf /tmp/* && apt-get purge -y --auto-remove gcc gfortran build-essential && \
    apt install -y libgomp1 libgfortran5

ENV PATH /opt/conda/envs/storm0/bin:.:$PATH
RUN /bin/bash -c "source activate storm0"

# add nwcst
ADD . /workdir

# Install the runtime interface client
RUN pip install \
#        --target ${FUNCTION_DIR} \
        awslambdaric


RUN echo ${LAMBDA_TASK_ROOT}
COPY app.py ${LAMBDA_TASK_ROOT}
RUN echo $PATH
RUN which python

ENTRYPOINT [ "conda", "run", "-n", "storm0", "/opt/conda/envs/storm0/bin/python", "-m", "awslambdaric" ]

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
# CMD [".app.lambda_handler"]
