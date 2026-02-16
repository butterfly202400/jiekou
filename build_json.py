import json
import os

# ====================================================
# 1. 自动化维护区 (03-08 线路)
# ====================================================
sub_configs = {
    "cns.json": {"name": "03_菜妮丝", "url": "https://tv.xn--yhqu5zs87a.top"},
    "fty.json": {"name": "04_饭太硬", "url": "http://www.饭太硬.com/tv"},
    "wex.json": {"name": "05_王二小", "url": "https://9280.kstore.vip/newwex.json"},
    "ok01.json": {"name": "06_OK线路", "url": "https://10352.kstore.vip/tv"},
    "ok02.json": {"name": "07_OK备用", "url": "http://ok521.top/tv"},
    "ok03.json": {"name": "08_OK备用2", "url": "http://ok213.top/ok"}
}

def generate_all():
    # --- 第一步：生成独立的子 JSON 文件 ---
    for filename, content in sub_configs.items():
        data = {"urls": [{"name": content["name"], "url": content["url"]}]}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 更新子接口: {filename}")

    # --- 第二步：构建完整主接口 out.json (移除时间戳参数) ---
    main_data = {
        "urls": [
            {
                "name": "01_特制净化",
                "url": "https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/tzjh.json"
            },
            {
                "name": "02_王二小净化",
                "url": "https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/wexjh.json"
            }
        ]
    }

    # --- 第三步：循环追加 03-08 线路 ---
    for filename, content in sub_configs.items():
        # 链接回归简洁形式
        url = f"https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/{filename}"
        main_data["urls"].append({
            "name": content["name"],
            "url": url
        })

    # 写入并覆盖主接口 out.json
    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print("\n🚀 同步完成！URL 已恢复简洁模式（无时间戳）。")

if __name__ == "__main__":
    generate_all()
