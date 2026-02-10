import json

# ====================================================
# 1. 自动化维护区 (03-08 线路)
# 以后你修改这里的线路名或网址，App 就会自动更新
# ====================================================
sub_configs = {
    "fty.json": {"name": "03_饭太硬", "url": "http://www.饭太硬.com/tv"},
    "wex.json": {"name": "04_王二小", "url": "https://9280.kstore.vip/newwex.json"},
    "ok01.json": {"name": "05_OK线路", "url": "https://10352.kstore.vip/tv"},
    "ok02.json": {"name": "06_OK备用", "url": "http://ok521.top/tv"},
    "ok03.json": {"name": "07_OK备用2", "url": "http://ok213.top/ok"},
    "cns.json": {"name": "08_菜妮丝", "url": "https://tv.xn--yhqu5zs87a.top"}
}

def generate_all():
    # --- 第一步：仅为 03-08 生成独立的子 JSON 文件 ---
    for filename, content in sub_configs.items():
        data = {"urls": [{"name": content["name"], "url": content["url"]}]}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 自动更新子接口: {filename}")

    # --- 第二步：构建包含 01-08 的完整主接口 out.json ---
    # 这里手动锁死 01 和 02 的指向，保护你的复杂代码不被覆盖
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

    # 自动把 03-08 的最新路径追加进去
    for filename, content in sub_configs.items():
        main_data["urls"].append({
            "name": content["name"],
            "url": f"https://ghfast.top/https://raw.githubusercontent.com/butterfly202400/jiekou/main/{filename}"
        })

    # 写入并覆盖主接口 out.json
    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print("🚀 架构同步完成！01-02 已受保护，03-08 已自动化。")

if __name__ == "__main__":
    generate_all()
