# Stage 1: Build the Go application
FROM golang:1.23.6-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy the Go application source code
COPY . .

# Build the Go application
RUN go build -o main .

# Stage 2: Create the final image with the Lambda Runtime Interface Adapter
# FROM public.ecr.aws/lambda/provided:al2
FROM alpine:latest


# COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 /lambda-adapter /opt/extensions/lambda-adapter


# Copy the built Go binary from the builder stage
COPY --from=builder /app/main /var/task/main
RUN ls -ltr
# Set the entry point to use the RIE
# ENTRYPOINT ["/usr/local/bin/aws-lambda-rie", "/var/task/main"]
EXPOSE 8080

# Set the CMD to your Lambda handler
CMD ["./main"]