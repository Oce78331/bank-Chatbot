# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the application code into the container
COPY . /code/

# ❗️ Crucial: Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Define the command to run your app.
# We use --host 0.0.0.0 to make it accessible and --port 7860 to match the exposed port.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]