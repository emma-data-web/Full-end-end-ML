#   base image
FROM python:3.10-slim

#  working directory 
WORKDIR /app

# 3. Copy dependency file 
COPY requirements.txt .

#  Installing  dependencies
RUN pip install --no-cache-dir -r requirements.txt

#  Copy all files
COPY . .

#   run the app
CMD ["python", "app.py"]
