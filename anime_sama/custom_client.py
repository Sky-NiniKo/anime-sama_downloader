from hashlib import blake2b

import hishel
import httpcore
from hishel._utils import normalized_url


def generate_key(request: httpcore.Request) -> str:
    encoded_url = normalized_url(request.url).encode("ascii")

    key_parts = [
        request.method,
        encoded_url,
        request.stream._stream,
    ]

    key = blake2b(digest_size=16)
    for part in key_parts:
        key.update(part)
    return key.hexdigest()


class CustomAsyncClient(hishel.AsyncCacheClient):
    def __init__(self, *args, **kwargs):
        customs = {
            "timeout": 30.0,
            "storage": hishel.AsyncFileStorage(ttl=3600),
            "controller": hishel.Controller(key_generator=generate_key),
        }
        customs.update(kwargs)

        super().__init__(*args, **customs)

    async def request(self, *args, **kwargs):
        if kwargs.get("extensions") is None:
            kwargs["extensions"] = {"force_cache": True}

        return await super().request(*args, **kwargs)
