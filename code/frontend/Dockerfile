FROM node:21-bookworm-slim as build

USER node

WORKDIR /app

COPY . ./

RUN npm install

RUN npm run build

FROM node:21-bookworm-slim

WORKDIR /app

COPY --from=build /app/dist ./public

RUN npm install -g http-server

EXPOSE 5173

ENTRYPOINT ["http-server", "-p", "5173"]
