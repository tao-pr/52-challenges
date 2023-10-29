# Background task

from enum import Enum, IntEnum
import redis
import asyncio
import aiofiles
import os

TEST_UNAUTH = 'unauth'


class Status(Enum):
    UNAUTH = -1
    UNKNOWN_URI = 0
    PENDING = 1
    READY = 200


class Purpose(IntEnum):
    STREAM_PREP_LOCK = 0
    STREAM_CHUNK = 1


TTL_LOCK = 10  # seconds
TTL_CHUNK = 30
CHUNK_SIZE = 15360  # 15 KB

rlock = redis.Redis(host='localhost', port=6555,
                    password='testpwd', db=Purpose.STREAM_PREP_LOCK.value)
rchunk = redis.Redis(host='localhost', port=6555,
                     password='testpwd', db=Purpose.STREAM_CHUNK.value)


async def gen_chunks(uri):
    print(f'[async] Generating chunks of : {uri}')
    with open(os.path.join('./data', uri), 'rb') as f:
        offset = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if chunk:
                print(f'[async] Reading chunk #{offset+1} of {uri} ({len(chunk)/1024} KB)')
                rchunk.mset({chunk_key(uri, offset): chunk})
                rchunk.expire(uri, TTL_CHUNK)
                offset += 1
            else:
                break


async def spawn(uri):
    # spawn coroutine generating chunks for uri
    global rlock
    global rchunk
    rlock.mset({uri: 1})
    rlock.expire(uri, TTL_LOCK)

    # regenerate content if chunks not available in cache
    if rchunk.mget(chunk_key(uri, 0))[0] is None:
        asyncio.create_task(gen_chunks(uri))  # fire and forget
    else:
        print(f'[async] Re-lock, content for {uri} already exists')


def chunk_key(uri, offset) -> str:
    return f'{uri}---{offset}'


async def check_progress(uid, uri, offset) -> Status:
    if uid == TEST_UNAUTH:
        return Status.UNAUTH

    global rlock
    global rchunk

    print(f'Checking progress of {uid} -> {uri}:{offset}')

    # If resource not available
    if not os.path.isfile(os.path.join('./data', uri)):
        return Status.UNKNOWN_URI

    lock = rlock.mget(uri)[0]  # lock is based on whole content alone

    # If no lock and no content, re-generate it
    if lock is None:
        # Place a new order
        print(
            f'No lock found for {uri}, Spawning stream task and return pending status')
        await spawn(uri)
        return Status.PENDING

    elif lock == 1:
        # Lock is on, meaning resource is being prepared
        print(f'Lock for {uri}:{offset} is on, return pending status')
        return Status.PENDING

    else:
        # Lock is off, meaning streaming chunk should already be ready
        chunk = rchunk.mget(chunk_key(uri, offset))[0]
        if chunk is None:
            # Chunk not available, generate it again
            print(
                f'Lock for {uri}:{offset} off, but content not available. Respawn stream task and return pending.')
            await spawn(uri)
            return Status.PENDING

        else:
            # Chunk available
            print(
                f'Lock for {uri}:{offset} off, and content is available. Return ready')
            return Status.READY
