FROM python:3.12
# Set the working directory in the container
WORKDIR /usr/local/app
# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the source code into the container
COPY . .
# Expose the port your app runs on
EXPOSE 5000
# Run the application
CMD ["flask", "run", "--host", "0.0.0.0", "--debug"]