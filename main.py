from datetime import datetime
import time
from colorama import Fore
import requests
import random
from fake_useragent import UserAgent
import asyncio
import json
import gzip
import brotli
import zlib
import chardet
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class monadscore:
    BASE_URL = "https://mscore.onrender.com/"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "origin": "https://monadscore.xyz",
        "referer": "https://monadscore.xyz/",
        "priority": "u=1, i",
        "Content-Type": "application/json",
        "sec-ch-ua": '"Microsoft Edge";v="134", "Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge WebView2";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    def __init__(self):
        self.config = self.load_config()
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.wallet = None
        self.session = self.sessions()
        self._original_requests = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete,
        }
        self.proxy_session = None

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Monad Score Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def sessions(self):
        session = requests.Session()
        retries = Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504, 520]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file. Additionally, if run_account_reff
        in self.config is True, it also loads queries from result_reff.txt.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries combined from query.txt and result_reff.txt if applicable,
                or an empty list if an error occurs.
        """
        self.banner()
        queries = []

        # Load queries from the primary file
        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)
            else:
                self.log(
                    f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN
                )
        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)

        # Jika run_account_reff bernilai True, tambahkan juga query dari file result_reff.txt
        if self.config.get("run_account_reff"):
            try:
                with open("result_reff.txt", "r") as file:
                    result_queries = [line.strip() for line in file if line.strip()]

                if result_queries:
                    queries.extend(result_queries)
                    self.log(
                        f"✅ Loaded {len(result_queries)} queries from result_reff.txt.",
                        Fore.GREEN,
                    )
                else:
                    self.log("⚠️ Warning: result_reff.txt is empty.", Fore.YELLOW)
            except FileNotFoundError:
                self.log("❌ File not found: result_reff.txt", Fore.RED)
            except Exception as e:
                self.log(f"❌ Unexpected error loading result_reff.txt: {e}", Fore.RED)

        return queries

    def decode_response(self, response):
        """
        Mendekode response dari server secara umum.

        Parameter:
            response: objek requests.Response

        Mengembalikan:
            - Jika Content-Type mengandung 'application/json', maka mengembalikan objek Python (dict atau list) hasil parsing JSON.
            - Jika bukan JSON, maka mengembalikan string hasil decode.
        """
        # Ambil header
        content_encoding = response.headers.get("Content-Encoding", "").lower()
        content_type = response.headers.get("Content-Type", "").lower()

        # Tentukan charset dari Content-Type, default ke utf-8
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()

        # Ambil data mentah
        data = response.content

        # Dekompresi jika perlu
        try:
            if content_encoding == "gzip":
                data = gzip.decompress(data)
            elif content_encoding in ["br", "brotli"]:
                data = brotli.decompress(data)
            elif content_encoding in ["deflate", "zlib"]:
                data = zlib.decompress(data)
        except Exception:
            # Jika dekompresi gagal, lanjutkan dengan data asli
            pass

        # Coba decode menggunakan charset yang didapat
        try:
            text = data.decode(charset)
        except Exception:
            # Fallback: deteksi encoding dengan chardet
            detection = chardet.detect(data)
            detected_encoding = detection.get("encoding", "utf-8")
            text = data.decode(detected_encoding, errors="replace")

        # Jika konten berupa JSON, kembalikan hasil parsing JSON
        if "application/json" in content_type:
            try:
                return json.loads(text)
            except Exception:
                # Jika parsing JSON gagal, kembalikan string hasil decode
                return text
        else:
            return text

    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)

        # Validasi index token
        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        # Log informasi login ke wallet dan info running node
        self.log(f"🔑 Login to wallet: {token}", Fore.CYAN)

        # === API BARU: Register User dengan Invite ===
        import json
        import requests

        payload_new = json.dumps({
            "wallet": token,
            "invite": "JioRgBeR"
        })
        user_url = f"{self.BASE_URL}user"        

        try:
            self.log("📡 Sending user registration request...", Fore.CYAN)
            response_new = requests.post(user_url, headers=self.HEADERS, data=payload_new)
            if response_new.status_code == 200:
                data_new = self.decode_response(response_new)
                if data_new.get("success") is True:
                    self.token = data_new.get("token")
                    self.wallet = token
                    self.log("✅ Wallet registration successful!", Fore.GREEN)
                else:
                    self.log("❌ Registration failed: Unsuccessful response", Fore.RED)
                    return
            else:
                self.log(f"❌ Failed to register user. Status code: {response_new.status_code}", Fore.RED)
                return
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error during user registration: {e}", Fore.RED)
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during user registration: {e}", Fore.RED)
            return

        # Info running node (sebagai informasi, bukan eksekusi perintah node)
        self.log("🚀 Running node...", Fore.CYAN)
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # === API LAMA: Update Start Time ===
        import time
        current_time_ms = int(time.time() * 1000)
        payload_old = json.dumps({
            "wallet": self.wallet,
            "startTime": current_time_ms
        })

        update_url = f"{self.BASE_URL}user/update-start-time"
        try:
            response_old = requests.put(update_url, headers=headers, data=payload_old)
            if response_old.status_code == 200:
                self.log("✅ Wallet login and update-start-time successful!", Fore.GREEN)
            else:
                self.log(f"❌ Failed to update start time. Status code: {response_old.status_code}", Fore.RED)
                return
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send update-start-time request: {e}", Fore.RED)
            return
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            return


    def task(self) -> None:
        import json
        import requests

        # Daftar task yang akan diklaim
        tasks = ["task003", "task002", "task001"]

        for task_id in tasks:
            self.log(f"🚀 Claiming task: {task_id}...", Fore.CYAN)

            payload = json.dumps({"wallet": self.wallet, "taskId": task_id})

            claim_url = f"{self.BASE_URL}user/claim-task"
            headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

            try:
                response = requests.post(claim_url, headers=headers, data=payload)
                if response.status_code == 200:
                    self.log(f"✅ Task {task_id} claimed successfully!", Fore.GREEN)
                else:
                    self.log(
                        f"❌ Failed to claim task {task_id}. Status code: {response.status_code}",
                        Fore.RED,
                    )
            except requests.exceptions.RequestException as e:
                self.log(
                    f"❌ Request error while claiming task {task_id}: {e}", Fore.RED
                )
            except Exception as e:
                self.log(
                    f"❌ Unexpected error while claiming task {task_id}: {e}", Fore.RED
                )

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        import random

        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


async def process_account(account, original_index, account_label, monad, config):
    # Menampilkan informasi akun
    display_account = account[:10] + "..." if len(account) > 10 else account
    monad.log(f"👤 Processing {account_label}: {display_account}", Fore.YELLOW)

    # Override proxy jika diaktifkan
    if config.get("proxy", False):
        monad.override_requests()
    else:
        monad.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

    # Login (fungsi blocking, dijalankan di thread terpisah) dengan menggunakan index asli (integer)
    await asyncio.to_thread(monad.login, original_index)

    monad.log("🛠️ Starting task execution...", Fore.CYAN)
    tasks_config = {
        "task": "Automatically solving tasks 🤖",
    }

    for task_key, task_name in tasks_config.items():
        task_status = config.get(task_key, False)
        color = Fore.YELLOW if task_status else Fore.RED
        monad.log(
            f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
            color,
        )
        if task_status:
            monad.log(f"🔄 Executing {task_name}...", Fore.CYAN)
            await asyncio.to_thread(getattr(monad, task_key))

    delay_switch = config.get("delay_account_switch", 10)
    monad.log(
        f"➡️ Finished processing {account_label}. Waiting {Fore.WHITE}{delay_switch}{Fore.CYAN} seconds before next account.",
        Fore.CYAN,
    )
    await asyncio.sleep(delay_switch)


async def worker(worker_id, monad, config, queue):
    """
    Setiap worker akan mengambil satu akun dari antrian dan memprosesnya secara berurutan.
    Worker tidak akan mengambil akun baru sebelum akun sebelumnya selesai diproses.
    """
    while True:
        try:
            original_index, account = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        account_label = f"Worker-{worker_id} Account-{original_index+1}"
        await process_account(account, original_index, account_label, monad, config)
        queue.task_done()
    monad.log(
        f"Worker-{worker_id} finished processing all assigned accounts.", Fore.CYAN
    )


async def main():
    monad = monadscore()  # Inisialisasi instance class monadscore Anda
    config = monad.load_config()
    all_accounts = monad.query_list
    num_threads = config.get("thread", 1)  # Jumlah worker sesuai konfigurasi

    if config.get("proxy", False):
        proxies = monad.load_proxies()

    monad.log(
        "🎉 [LIVEXORDS] === Welcome to Monad Score Automation === [LIVEXORDS]", Fore.YELLOW
    )
    monad.log(f"📂 Loaded {len(all_accounts)} accounts from query list.", Fore.YELLOW)

    while True:
        # Buat queue baru dan masukkan semua akun (dengan index asli)
        queue = asyncio.Queue()
        for idx, account in enumerate(all_accounts):
            queue.put_nowait((idx, account))

        # Buat task worker sesuai dengan jumlah thread yang diinginkan
        workers = [
            asyncio.create_task(worker(i + 1, monad, config, queue))
            for i in range(num_threads)
        ]

        # Tunggu hingga semua akun di queue telah diproses
        await queue.join()

        # Opsional: batalkan task worker (agar tidak terjadi tumpang tindih)
        for w in workers:
            w.cancel()

        monad.log("🔁 All accounts processed. Restarting loop.", Fore.CYAN)
        delay_loop = config.get("delay_loop", 30)
        monad.log(
            f"⏳ Sleeping for {Fore.WHITE}{delay_loop}{Fore.CYAN} seconds before restarting.",
            Fore.CYAN,
        )
        await asyncio.sleep(delay_loop)


if __name__ == "__main__":
    asyncio.run(main())
