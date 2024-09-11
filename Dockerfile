FROM python:3.11
COPY . /main
EXPOSE 4000
WORKDIR /main
RUN python3 -m pip install -r requirements.txt
CMD python main.py
