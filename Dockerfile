FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt ./
COPY project /app/project
COPY static /app/static
COPY templates /app/templates
COPY app.py /app
COPY users.json /app
COPY setup.sh ./
COPY ncbi-blast-2.10.0+-x64-linux.tar.gz ./

RUN  python -m venv venv
CMD  ["source venv/bin/activate"]
RUN apt-get install ca-certificates

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN tar zxvpf ncbi-blast-2.10.0+-x64-linux.tar.gz

RUN chmod +x setup.sh
ENV PATH="/app/ncbi-blast-2.10.0+/bin:${PATH}"


ENTRYPOINT ["/bin/bash", "setup.sh"]

EXPOSE 5000
