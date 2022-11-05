# Python Version
FROM python:3.9

# work path
WORKDIR /code

# It is convenient to use cache loading below
COPY ./requirements.txt /code/requirements.txt

# Download the installation package using the cache
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Use the cache to download the installation package (mirror)
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=1000 --no-cache-dir --upgrade -r /code/requirements.txt

# docker deploy (https://fastapi.tiangolo.com/zh/deployment/docker/)
# .Indicates the same level directory
COPY . /code/

# start command
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# main.py start command
CMD ["python", "main.py"]