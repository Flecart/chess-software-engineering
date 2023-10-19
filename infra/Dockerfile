# run with something like
# docker run -p 4000:4000 -v ./build.sh:/app/build.sh -d webhook-listener -e "SECRET=your_secret_value"

# Use an official Node.js runtime as a base image
FROM node:20

# Set a working directory within the container
WORKDIR /app

# Copy your script and any other necessary files into the container
COPY ./webhook_listener.js /app/

# Install any required dependencies
RUN npm install express

# Expose the port your listener will run on
EXPOSE 4000

# Define a build argument for your secret
ENV SECRET="your_secret_value"

# Use the build argument in your CMD
CMD ["node", "webhook-listener.js", "$SECRET"]
