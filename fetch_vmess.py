#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import base64
import requests

# ========================
# 配置
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VMESS_FILE = os.path.join(BASE_DIR, "vmess_links.txt")
LOG_FILE = os.path.join(BASE_DIR, "fetch_log.txt")

# 你要抓取的 URL 列表
SOURCE_URLS = [
    "https://example.com/base64.txt",  # 替换为真实 URL
]

MAX_RETRIES = 3      # 自动重试次数
RETRY_INTERVAL = 5   # 秒

# ========================
# 工具函数
# ========================
def log(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    line = f"{timestamp} {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def fetch_url(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log(f"抓取: {url} (尝试 {attempt})")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            log(f"抓取失败: {e}")
            if attempt < MAX_RETRIES:
                log(f"等待 {RETRY_INTERVAL} 秒后重试...")
                time.sleep(RETRY_INTERVAL)
            else:
                log("超过最大重试次数，跳过该 URL")
    return ""

def decode_base64(text):
    try:
        decoded = base64.b64decode(text).decode("utf-8")
        log(f"Base64 解码前500字符预览:\n{decoded[:500]}")
        return decoded
    except Exception as e:
        log(f"Base64 解码失败: {e}")
        return ""

# ========================
# 主逻辑
# ========================
def main():
    all_links = []

    for url in SOURCE_URLS:
        raw_text = fetch_url(url)
        if not raw_text:
            continue

        decoded_text = decode_base64(raw_text)
        if not decoded_text:
            continue

        links = [line.strip() for line in decoded_text.splitlines() if line.strip().startswith("vmess://")]
        log(f"从 {url} 提取 {len(links)} 条 vmess 链接")
        all_links.extend(links)

    all_links = sorted(set(all_links))

    with open(VMESS_FILE, "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link + "\n")

    log(f"总共写入 {len(all_links)} 条 vmess 链接到 {VMESS_FILE}")

if __name__ == "__main__":
    main()
