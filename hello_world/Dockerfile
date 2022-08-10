FROM public.ecr.aws/lambda/python:3.9

COPY app.py requirements.txt MSM_template.grb my_grib2table ./

SHELL ["/bin/bash", "-c"]

# Install the runtime interface client
RUN python3.9 -m pip install awslambdaric
RUN python3.9 -m venv storm

RUN ls /tmp

# install libraries
RUN yum makecache && yum -y install mesa-libGL-devel mesa-libGLU-devel libpng-devel 
RUN source storm/bin/activate && \
    yum -y groupinstall "Development Tools" && yum install kernel-devel kernel-headers && \
    pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt 

# install wgrib2 v3.0.2
RUN yum makecache && yum -y groupinstall 'Development Tools' && yum -y install gcc-gfortran libgfortran && \
    yum -y install wget && \
    wget -O /tmp/wgrib2.tgz https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v3.0.2 && \
    cd /tmp && tar -zxvf wgrib2.tgz && cd grib2 && \
    sed -i 's/MAKE_SHARED_LIB=0/MAKE_SHARED_LIB=1/' makefile && \
    export CC=gcc && export FC=gfortran && make && make lib && \
    mv wgrib2/wgrib2 /usr/local/bin/ && \
    # mv lib/libwgrib2.so ${LAMBDA_TASK_ROOT}/storm/lib/python3.9/site-packages/ && \
    mv lib/libwgrib2.so ${LAMBDA_TASK_ROOT}/ && \
    wget -O /tmp/pywgrib2_s.tgz  "https://ftp.cpc.ncep.noaa.gov/wd51we/pywgrib2_s/pywgrib2_s.tgz" && \
    # cd /tmp && tar -zxvf pywgrib2_s.tgz && mv pywgrib2_s/pywgrib2_s.py ${LAMBDA_TASK_ROOT}/storm/lib/python3.9/site-packages/ && \
    cd /tmp && tar -zxvf pywgrib2_s.tgz && mv pywgrib2_s/pywgrib2_s.py ${LAMBDA_TASK_ROOT} && \
    yum -y remove install gcc-gfortran libgfortran wget kernel-devel kernel-headers && \
    yum -y groupremove "Development Tools" && \
    rm -fr /tmp/* && yum -y install libgomp libgfortran

RUN python3.9 -m pip install -r requirements.txt -t ${LAMBDA_TASK_ROOT}

# ENTRYPOINT [ "python3.9", "-m", "awslambdaric" ]
# RUN ["/bin/bash", "-c", "source /var/task/storm/bin/activate"]
# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
