# Base image - Python 
FROM python:3.11-slim

# Python environment variables set karo better performance ke liye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Container ke andar ek folder banao
WORKDIR /app

# Pehle requirements copy karo
COPY requirements.txt .

# Packages install karo (--no-cache-dir se image size chota rahega)
RUN pip install --no-cache-dir -r requirements.txt

# Apna saara code copy karo
COPY . .

# Port open karo (bahar se access ke liye)
EXPOSE 8000

# Project start karne ka command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]