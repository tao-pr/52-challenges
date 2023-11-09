import uvicorn
from fastapi import FastAPI
import random

app = FastAPI()

@app.get('/')
def get_root():
    # 15% chance of failing
    if random.rand() < 0.15:
        raise RuntimeError('Simulated failure')
    return {'version': 1.0}

# Run with 
# uvicorn server:app --reload

if __name__ == '__main__':
    print('Starting the server')
    uvicorn.run(app, host='0.0.0.0', port=9191)