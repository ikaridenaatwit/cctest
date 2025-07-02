# 1. Base Image: Start from an official, lightweight Python image.
FROM python:3.11-slim

# 2. Working Directory: Set the default directory for all subsequent commands.
WORKDIR /app

# 3. Copy and Install Dependencies:
#    Copy the requirements file first to leverage Docker's layer caching.
#    This way, dependencies are only re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Application Code:
#    Copy the rest of your application's source code into the working directory.
COPY . .

# 5. Expose Port:
#    Inform Docker that the container listens on port 8000.
#    This is for documentation and doesn't actually publish the port.
EXPOSE 8082


# 6. Run Command:
#    Specify the command to run when the container starts.
#    This runs the Uvicorn server, making your app accessible from outside the container.

CMD ["uvicorn", "main:app", "--host", "0.0.0.0" , "--port", "8082"]
