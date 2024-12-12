# Gunakan image Python sebagai base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080

# Salin file aplikasi ke dalam container
WORKDIR /app
COPY . /app

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Ekspose port 8080 untuk Cloud Run
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "app.py"]
