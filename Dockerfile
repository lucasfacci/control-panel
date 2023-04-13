FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip \
&& pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]