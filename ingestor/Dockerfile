FROM python:3.11

# Setup work directory
WORKDIR /usr/src/app

# Copy requirements file
COPY requirements.txt ./

# Install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the program
COPY . .

# Run data ingestor
CMD [ "python", "./data_ingestor.py" ]
