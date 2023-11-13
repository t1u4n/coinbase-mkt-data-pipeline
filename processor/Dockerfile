FROM bitnami/spark:3.5

# Setup work directory
WORKDIR /usr/src/app

# Copy requirements file
COPY requirements.txt ./

# Install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the programs
COPY data_processor.py .
COPY --chmod=755 start.sh .

# Run data ingestor
CMD ["./start.sh"]
