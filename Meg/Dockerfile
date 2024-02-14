# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Install project dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --ignore-pipfile

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run Streamlit
CMD ["pipenv", "run", "streamlit", "run", "your_script.py"]