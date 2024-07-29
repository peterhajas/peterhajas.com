# Use the official Node.js image from the Docker Hub
# FROM node:14
FROM alpine:3.14

RUN apk add npm \
    && npm install -g tiddlywiki \
    && apk add python3 \
    && apk add jq \
    && apk add bash

# Create a directory for the TiddlyWiki
RUN mkdir -p /usr/local/tiddlywiki

# Set the working directory
WORKDIR /usr/local/tiddlywiki

# Copy over entrypoint script
COPY entrypoint.bash /
# Copy over tiddlywiki_strip_public_tag
COPY tiddlywiki_strip_public_tag /

# Make executables have +x
RUN chmod +x /entrypoint.bash
RUN chmod +x /tiddlywiki_strip_public_tag

# Install TiddlyWiki globally using npm
RUN npm install -g tiddlywiki

# Expose the default port for TiddlyWiki
EXPOSE 8080

# Start entrypoint
ENTRYPOINT ["/entrypoint.bash"]
