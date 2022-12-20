FROM python:3.8-slim
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000
ENV NAME revenue
CMD ["python", "app.py"]
