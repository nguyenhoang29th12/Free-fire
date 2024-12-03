import asyncio
import aiohttp
import logging
from colorama import Fore, Style, init

# Khởi tạo colorama
init(autoreset=True)

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Danh sách key hợp lệ
VALID_KEYS = ["key123", "admin2024", "buoitao"]

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
                        data = await response.json()
                        if endpoint == "info":
                            self.print_info(data)
                        else:
                            logging.info(Fore.BLUE + f"[SUCCESS] Yêu cầu thành công: {endpoint}")
                    else:
                        logging.error(Fore.RED + f"[ERROR] Có lỗi xảy ra: {response.status} - {await response.text()}")

    def print_info(self, data):
        """In thông tin từ endpoint 'info' một cách gọn gàng."""
        account_basic_info = data.get("account_basic_info", {})
        account_activity = data.get("account_activity", {})
        account_overview = data.get("account_overview", {})
        pet_details = data.get("pet_details", {})
        guild_info = data.get("guild_info", {})
        admin_info = data.get("Info Admin - Group", {})

        # In các thông tin cơ bản
        print(Fore.GREEN + "[INFO] Thông tin tài khoản:")
        print(f"  UID: {account_basic_info.get('uid', 'N/A')}")
        print(f"  Tên: {account_basic_info.get('name', 'N/A')}")
        print(f"  Cấp: {account_basic_info.get('level', 'N/A')} - Khu vực: {account_basic_info.get('region', 'N/A')}")
        print(f"  Lượt thích: {account_basic_info.get('likes', 'N/A')} - Điểm danh dự: {account_basic_info.get('honor_score', 'N/A')}")
        print()

        # In hoạt động tài khoản
        print(Fore.YELLOW + "[INFO] Hoạt động tài khoản:")
        print(f"  Rank BR: {account_activity.get('br_rank', 'N/A')}")
        print(f"  Rank CS: {account_activity.get('cs_rank', 'N/A')}")
        print(f"  Lần đăng nhập cuối: {account_activity.get('last_login', 'N/A')}")
        print(f"  Tạo tài khoản: {account_activity.get('created_at', 'N/A')}")
        print()

        # In chi tiết trang bị
        print(Fore.CYAN + "[INFO] Chi tiết trang bị:")
        print(f"  Nhân vật: {account_overview.get('equipped_character', 'N/A')}")
        print(f"  Kỹ năng: {', '.join(account_overview.get('equipped_skills', []))}")
        print()

        # In chi tiết pet
        print(Fore.MAGENTA + "[INFO] Thông tin Pet:")
        print(f"  Pet được trang bị: {pet_details.get('equipped', 'N/A')}")
        print(f"  Pet ID: {pet_details.get('pet_id', 'N/A')} - Cấp độ: {pet_details.get('pet_level', 'N/A')}")
        print()

        # In thông tin guild
        print(Fore.BLUE + "[INFO] Thông tin Guild:")
        print(f"  Tên Guild: {guild_info.get('guild_name', 'N/A')}")
        print(f"  Trạng thái: {guild_info.get('status', 'N/A')}")
        print()

        # In thông tin admin
        print(Fore.RED + "[INFO] Thông tin Admin:")
        print(f"  Admin: NguyenHoangdev")
        print(f"  Api: {admin_info.get('Admin', 'N/A')}")
        print(f"  Telegram: update")
        print(f"  Group Zalo: none")
        print("-" * 40)

    async def send_multiple_requests(self, endpoints, params_list):
        tasks = []
        for endpoint, params in zip(endpoints, params_list):
            tasks.append(asyncio.create_task(self.send_request(endpoint, params)))
        await asyncio.gather(*tasks)

def check_key():
    """Kiểm tra key người dùng nhập."""
    print(Fore.YELLOW + "Vui lòng nhập key để sử dụng:")
    for _ in range(3):  # Người dùng có 3 lần thử
        key = input(Fore.MAGENTA + "Nhập key: ")
        if key in VALID_KEYS:
            print(Fore.GREEN + "Key hợp lệ! Tiếp tục...")
            return True
        else:
            print(Fore.RED + "Key không hợp lệ! Thử lại.")
    print(Fore.RED + "Bạn đã nhập sai key quá nhiều lần. Thoát chương trình.")
    return False

async def main():
    # Banner
    print(Fore.CYAN + """
███████╗███████╗███████╗    ███████╗██╗██████╗ ████████╗
██╔════╝██╔════╝██╔════╝    ██╔════╝██║██╔══██╗╚══██╔══╝
█████╗  █████╗  █████╗      █████╗  ██║██████╔╝   ██║   
██╔══╝  ██╔══╝  ██╔══╝      ██╔══╝  ██║██╔═══╝    ██║   
██║     ███████╗██║         ██║     ██║██║        ██║   
╚═╝     ╚══════╝╚═╝         ╚═╝     ╚═╝╚═╝        ╚═╝   
    """)
    print(Fore.YELLOW + "API Requester Tool - Powered by asyncio and aiohttp\n")

    # Kiểm tra key
    if not check_key():
        return  # Thoát nếu key không hợp lệ

    requester = APIRequester("https://free-fire-virusteam.vercel.app", delay=5)  # Set delay

    uid = input(Fore.MAGENTA + "Nhập UID của bạn: ")
    sl = input(Fore.MAGENTA + "Nhập số lượng truy cập (100-1000): ")

    endpoints = ["likes", "visit"]
    params_list = [{"uid": uid}, {"uid": uid, "sl": sl}]

    if sl:
        endpoints.append("info")  # Include "info" endpoint if sl is provided
        params_list.append({"uid": uid})

    while True:
        await requester.send_multiple_requests(endpoints, params_list)
        logging.info(Fore.CYAN + f"Đợi {requester.delay} giây trước khi lặp lại... chỉnh delay trong code")
        await asyncio.sleep(requester.delay)

if __name__ == "__main__":
    asyncio.run(main())
