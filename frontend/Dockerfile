# frontend/Dockerfile
FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
ENV VITE_DOCKER_API_URL=http://localhost:8080/api/v1
# Build the application
RUN npm run build

# Utilise un serveur statique (serve par exemple)
RUN npm install -g serve

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
