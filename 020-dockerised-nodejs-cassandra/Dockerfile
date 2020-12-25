FROM node:12-alpine
WORKDIR /usr/src/app/
COPY app/* /usr/src/app/
RUN npm install
EXPOSE 3334
ENTRYPOINT node /usr/src/app/main -p 3334
