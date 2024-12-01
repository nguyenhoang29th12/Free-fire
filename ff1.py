import asyncio
import aiohttp
import logging
import time

logging.basicConfig(level=logging.INFO)

class APIRequester:
    def __init__(self, base_url, delay=0):  # Added delay parameter
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(10)
        self.delay = delay  # Added delay attribute

    async def send_request(self, endpoint, params):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/{endpoint}", params=params) as response:
                    if response.status == 200:
                        logging.info("Yêu cầu thành công!")
                    else:
                        logging.error(f"Có lỗi xảy ra: {response.status} - {await response.text()}")

    async def send_multiple_requests(self, endpoints, params_list):
        tasks = []
        for endpoint, params in zip(endpoints, params_list):
            tasks.append(asyncio.create_task(self.send_request(endpoint, params)))
        await asyncio.gather(*tasks)

async def main():
    requester = APIRequester("https://free-fire-virusteam.vercel.app", delay=0)  # Set delay

    uid = input("Nhập UID của bạn: ")
    sl = input("Nhập số lượng truy cập (hoặc để trống cho 'info'): ")

    endpoints = ["likes", "visit"]
    params_list = [{"uid": uid}, {"uid": uid, "sl": sl}]

    if sl:
        endpoints.append("info")  # Include "info" endpoint if sl is provided
        params_list.append({"uid": uid})

    while True:
        await requester.send_multiple_requests(endpoints, params_list)
        logging.info(f"Đợi {requester.delay} giây trước khi lặp lại... chỉnh delay trong code")
        await asyncio.sleep(requester.delay)

if __name__ == "__main__":
    asyncio.run(main())