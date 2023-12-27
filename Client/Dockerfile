#FROM nvidia/cuda:11.2.2-devel-ubuntu20.04
FROM nvidia/cuda:12.2.0-devel-ubuntu20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
# RUN apt-get install libgl1 -y
# RUN apt-get install libglib2.0-0 -y
RUN apt-get install -y git
WORKDIR /data
COPY requirements.txt .
#COPY tensorrt_libs-8.6.1-py2.py3-none-manylinux_2_17_x86_64.whl /data
RUN pip3 install --no-cache-dir -r requirements.txt
# RUN pip3 install pycuda
# RUN pip3 install numpy==1.23.1
# RUN apt install python3-libnvinfer -y
#COPY TensorRT-8.6.1.6 .
#RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:TensorRT-8.6.1.6/lib
#RUN pip3 install TensorRT-8.6.1.6/python/tensorrt-8.6.1-cp38-none-linux_x86_64.whl

#EXPORT LD_LIBRARY_PATH=$LD_LIBRARY_PATH:TensorRT-8.6.1/lib
#RUN pip3 install tensorrt_libs-8.6.1-py2.py3-none-manylinux_2_17_x86_64.whl
#RUN pip3 install tensorrt
#RUN pip3 install pycuda==2021.1
##RUN pip3 install pycuda
CMD [ "/bin/bash" ]
