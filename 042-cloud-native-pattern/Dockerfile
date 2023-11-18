FROM python:3.9-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY ./app /app
EXPOSE 9191
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9191"]
