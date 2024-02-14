# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /container_files

# Copy the current directory contents into the container at /app
COPY app ./app
COPY data /data 
COPY main.sh .

# Install Pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Install project dependencies
COPY Pipfile Pipfile.lock /container_files/
RUN pipenv install --deploy --ignore-pipfile

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run Streamlit
CMD ["pipenv", "run", "main.sh"]