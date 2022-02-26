FROM python:3.9-slim
WORKDIR /app
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "stocks_products.wsgi", "-b", "0.0.0.0:8000"]



