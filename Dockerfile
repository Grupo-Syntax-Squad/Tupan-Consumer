FROM python:3

WORKDIR /usr/ubuntu/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main.py" ]
