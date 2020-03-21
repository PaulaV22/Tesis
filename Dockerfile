FROM python:3.7
WORKDIR /app
COPY requirements.txt ./
COPY project /app/project
COPY static /app/static
COPY templates /app/templates
COPY app.py /app
COPY users.json /app
COPY setup.sh ./

RUN  python -m venv venv
CMD  ["source venv/bin/activate"]
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x setup.sh

ENTRYPOINT ["/bin/bash", "setup.sh"]

EXPOSE 5000