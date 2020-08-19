import aiohttp

async def request(url, choice):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
            if choice is None:
                resp = await resp.text()
                return resp
            else:
                resp = await resp.json()
                return resp[f"{choice}"]

async def advrequest(url, choice, number, choice2):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
            if number is None:
                resp = await resp.json()
                return resp[f"{choice}"][f"{choice2}"]
            else:
                resp = await resp.json()
                return resp[f"{choice}"][number][f"{choice2}"]