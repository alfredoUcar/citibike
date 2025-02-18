FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

EXPOSE 8000

# run server
CMD ["fastapi", "dev", "main.py"]
