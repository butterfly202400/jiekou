import json
import os

# 定义文件配置：文件名、线路名、目标原始网址
configs = {
    "fty.json": {"name": "03_饭太硬", "url": "http://www.饭太硬.com/tv"},
    "wex.json": {"name": "04_王二小", "url": "https://9280.kstore.vip/newwex.json"},
    "ok01.json": {"name": "05_OK线路", "url": "https://10352.kstore.vip/tv"},
    "ok02.json": {"name": "06_OK备用", "url": "http://ok521.top/tv"},
    "ok03.json": {"name": "07_OK备用2", "url": "http://ok213.top/ok"},
    "cns.json": {"name": "08_菜妮丝", "url": "https://tv.xn--yhqu5zs87a.top"}
}

def generate_files():
    for filename, content in configs.items():
        data = {
            "urls": [
                {
                    "name": content["name"],
                    "url": content["url"]
                }
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    generate_files()

