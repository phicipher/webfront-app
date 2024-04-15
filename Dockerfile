# Use Nginx image from Docker Hub
FROM nginx:alpine

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Remove the default server definition
RUN rm /etc/nginx/conf.d/default.conf

# Copy the static site files
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx and keep it running
CMD ["nginx", "-g", "daemon off;"]
