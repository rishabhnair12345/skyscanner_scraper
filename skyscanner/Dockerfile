FROM python:3.11-slim

# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Set environment variables
COPY .env .env
# Copy the rest of the application code into the container
COPY . .
# Expose the port the app runs on
EXPOSE 4000
# Set environment variable to enable production behavior
ENV PYTHONUNBUFFERED=1
# Run the app
CMD [ "python", "skyscanner/app/webapp.py" ]