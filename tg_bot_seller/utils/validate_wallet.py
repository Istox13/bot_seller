from http import HTTPStatus

import aiohttp


async def validate_wallet(address: hash) -> bool:
    async with aiohttp.ClientSession() as client:
        resp = await client.get(f'https://blockchain.info/address/{address}?format=json')
        return resp.status == HTTPStatus.OK
