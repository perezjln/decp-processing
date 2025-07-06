FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Rust and Cargo
RUN apt-get update && apt-get install -y curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Install any needed packages specified in pyproject.toml
RUN pip install .

# Copy the current directory contents into the container at /app
COPY . /app

# Run main.py when the container launches
CMD ["python", "src/flows_oneshot.py"]
