import httpx
import asyncio 
from typing import Awaitable

from circuit_breaker import CircuitBreaker, api_circuit_breaker


faulty_endpoint = "http://localhost:5000/failure"
success_endpoint = "http://localhost:5000/success"
random_status_endpoint = "http://localhost:5000/random"


@api_circuit_breaker()
async def make_request(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=0.3)
            if response.status_code == httpx.codes.OK:
                print(f"Call to {url} succeed with status code = {response.status_code}")
                return response
        if 500 <= response.status_code < 600:
            print(f"Call to {url} failed with status code = {response.status_code}")

            raise Exception("Server Issue")
    except Exception:
        print(f"call to {url} failed")
        raise


async def main():
    circuit_breakers = CircuitBreaker(make_request, exceptions=(Exception,), threshold=5, delay=10)
    await asyncio.gather(*[circuit_breakers.make_remote_call(faulty_endpoint) for _ in range(5)])

# asyncio.run(make_request(faulty_endpoint))
