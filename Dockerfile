FROM python
ADD sources.list /etc/apt/
ADD . /app/
WORKDIR /app/
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install itchat -i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install redis -i https://mirrors.aliyun.com/pypi/simple/
ENTRYPOINT ["python","./main.py"]