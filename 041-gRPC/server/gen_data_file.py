"""
Generate artificial data file for streaming
"""

import os
from task.background import CHUNK_SIZE

NUM_CHUNKS = 25


def gen_bytes(offset: int) -> bytes:
    return bytes([50+offset*4 for _ in range(CHUNK_SIZE)])


if __name__ == '__main__':
    with open(os.path.join('./data/test-file'), 'wb') as f:
        for offset in range(NUM_CHUNKS):
            buf = gen_bytes(offset)
            print(f'Writing chunk {offset+1} of {NUM_CHUNKS}')
            f.write(buf)
    print(f'Total {NUM_CHUNKS * CHUNK_SIZE / 1024} KB written')
