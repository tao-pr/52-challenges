FROM node:12-alpine
COPY app/* /usr/src/app/
RUN npm install app/
ENTRYPOINT node /usr/src/app/main -p 3334
