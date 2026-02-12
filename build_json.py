import json
import os
import time

# ====================================================
# 1. 自动化维护区 (03-08 线路)
# 这里的顺序决定了 App 里的显示顺序，只需在这修改线路名
# ====================================================
sub_configs = {
    # 菜妮丝已移动到第 3 位，后续序号顺延
    "cns.json": {"name": "03_菜妮丝", "url": "https://tv.xn--yhqu5zs87a.top"},
    "fty.json": {"name": "04_饭太硬", "url": "http://www.饭太硬.com/tv"},
    "wex.json": {"name": "05_王二小", "url": "https://9280.kstore.vip/newwex.json"},
    "ok01.json": {"name": "06_OK线路", "url": "https://10352.kstore.vip/tv"},
    "ok02.json": {"name": "07_OK备用", "url": "http://ok521.top/tv"},
    "ok03.json": {"name": "08_OK备用2", "url": "http://ok213.top/ok"}
}

def generate_all():
    # 生成当前时间戳，用于强刷 CDN 和 App 缓存
    # 每次运行脚本，这个数字都会变，URL 也会随之更新
    timestamp = int(time.time())
    
    # --- 第一步：生成独立的子 JSON 文件 ---
    for filename, content in sub_configs.items():
        # 子文件内容同样建议保持最新
        data = {"urls": [{"name": content["name"], "url": content["url"]}]}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 更新子接口: {filename} -> {content['name']}")

    # --- 第二步：构建包含 01-08 的完整主接口 out.json ---
    main_data = {
        "urls": [
            {
                "name": "01_特制净化",
                "url": f"https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/tzjh.json?v={timestamp}"
            },
            {
                "name": "02_王二小净化",
                "url": f"https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/wexjh.json?v={timestamp}"
            }
        ]
    }

    # --- 第三步：循环追加 03-08 线路并注入防缓存参数 ---
    for filename, content in sub_configs.items():
        # 通过在 URL 后面拼接 ?v=时间戳，诱导 App 认为这是新文件
        raw_base_url = f"https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/{filename}"
        main_data["urls"].append({
            "name": content["name"],
            "url": f"{raw_base_url}?v={timestamp}"
        })

    # 写入并覆盖主接口 out.json
    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🚀 同步完成！当前版本 v={timestamp}")
    print("OK影视 App 现已强制刷新缓存。")

if __name__ == "__main__":
    generate_all()
