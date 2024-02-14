# Use an official Python runtime as a parent image
FROM docker.io/python:3.12 AS builder

# Set the working directory in the container
RUN mkdir usr/src/meg
WORKDIR /usr/src/meg

COPY Pipfile .
COPY Pipfile.lock .

ENV PIPENV_VENV_IN_PROJECT=1

RUN pip install --upgrade pip
RUN pip install pipenv

RUN pipenv install 

# Create Runtime
FROM docker.io/python:3.12 AS runtime

RUN mkdir usr/src/meg

RUN mkdir /usr/src/meg/.venv
COPY /app /usr/src/meg/app/
COPY /data /usr/src/meg/data/

COPY --from=builder /usr/src/meg/.venv/ /usr/src/meg/.venv/

# Make port 8501 available to the world outside this container
EXPOSE 8501

WORKDIR /usr/src/meg

# Run Streamlit
CMD ["/usr/src/meg/.venv/bin/python", "-m", "streamlit", "run", "/usr/src/meg/app/interface.py", "--server.port=8501", "--server.address=0.0.0.0"]