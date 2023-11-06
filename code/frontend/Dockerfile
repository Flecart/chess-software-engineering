FROM node:21-bookworm-slim as build

WORKDIR /app

COPY . ./

ENV VITE_BACKEND_URL=http://app.t1-check-mates.mooo.com:8000
ENV VITE_FRONTEND_URL=http://app.t1-check-mates.mooo.com:80

RUN npm install

RUN npm run build

FROM node:21-bookworm-slim

WORKDIR /app

COPY --from=build /app/dist ./public

# so http-server always returns index.html, for SPA
RUN mv ./public/index.html ./public/404.html

RUN npm install -g http-server

EXPOSE 5173

ENTRYPOINT ["http-server", "-p", "5173"]
