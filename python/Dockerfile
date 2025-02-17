# Use a minimal Python image
FROM python:3.12-slim

# Add AWS Lambda Web Adapter as an extension
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 /lambda-adapter /opt/extensions/lambda-adapter

# Set the working directory inside the container
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask & Lambda
ENV FLASK_APP=app.py
ENV PORT=8080  

# Expose the correct port
EXPOSE 8080

# Start the Flask app using Gunicorn with dynamic port
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
