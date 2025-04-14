FROM python:3.12-bookworm

# Создаем директорию для приложения
WORKDIR /app

# Настройка OpenMPI
COPY openmpi-4.0.0 /app/openmpi-4.0.0
RUN ln -s /app/openmpi-4.0.0 /app/openmpi

ENV PATH="/app/openmpi/bin:${PATH}"
ENV LD_LIBRARY_PATH="/app/openmpi/lib"
ENV OPAL_PREFIX="/app/openmpi"

# Настройка HPS_ST3D
COPY HPS_ST3D /app/HPS_ST3D
ENV PATH="/app/HPS_ST3D/bin:${PATH}"

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . /app/code
WORKDIR /app/code

# Устанавливаем переменные окружения
ENV DEBUG=0
ENV FDSN_BASE="http://84.237.52.214:8000"
ENV HPS_ST3D_EXEC="/app/HPS_ST3D/bin/HPS_ST3D"
ENV DB_LOGIN=""
ENV DB_PASSWORD=""
ENV PYTHONPATH=/app/code/src

# Запуск FastAPI с помощью Uvicorn
CMD ["uvicorn", "src.geo.main:application", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]

