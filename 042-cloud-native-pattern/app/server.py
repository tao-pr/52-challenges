import uvicorn
from fastapi import FastAPI
import random
import os

app = FastAPI()

@app.get('/')
def get_root():
    # 15% chance of failing
    if random.random() < 0.15:
        raise RuntimeError('Simulated failure')
    return {'version': os.environ.get('TAG') or 'default'}

# Run with 
# python -m uvicorn server:app

if __name__ == '__main__':
    print('Starting the server')
    uvicorn.run(app, host='0.0.0.0', port=9191)