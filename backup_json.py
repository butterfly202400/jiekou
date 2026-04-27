import os
import shutil
from datetime import datetime, timedelta, timezone

# ===== 1. 环境配置 =====
beijing_tz = timezone(timedelta(hours=8))
now = datetime.now(beijing_tz)

# 时间戳格式：2026-04-27_01-00（精确到分钟）
timestamp = now.strftime("%Y-%m-%d_%H-%M")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_ROOT = os.path.join(ROOT_DIR, "backup")
LOG_FILE = os.path.join(BACKUP_ROOT, "backup_log.txt")

if not os.path.exists(BACKUP_ROOT):
    os.makedirs(BACKUP_ROOT)

# ===== 2. 执行备份 =====
# 仅备份根目录下的 .json 文件
json_files = [f for f in os.listdir(ROOT_DIR) if f.endswith('.json')]
backup_dir = os.path.join(BACKUP_ROOT, timestamp)

copy_count = 0
if json_files:
    # 同一分钟内多次运行会共用同一目录（exist_ok=True）
    os.makedirs(backup_dir, exist_ok=True)
    for f in json_files:
        shutil.copy2(os.path.join(ROOT_DIR, f), os.path.join(backup_dir, f))
        copy_count += 1

# ===== 3. 自动修剪：保留最近 20 次备份 =====
all_backups = sorted([
    d for d in os.listdir(BACKUP_ROOT)
    if os.path.isdir(os.path.join(BACKUP_ROOT, d))
])

deleted_count = 0
if len(all_backups) > 20:
    to_delete = all_backups[:-20]
    for folder in to_delete:
        shutil.rmtree(os.path.join(BACKUP_ROOT, folder))
        deleted_count += 1

# ===== 4. 写入操作日志 =====
current_total = len([d for d in os.listdir(BACKUP_ROOT) if os.path.isdir(os.path.join(BACKUP_ROOT, d))])
log_msg = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 备份:{copy_count} | 清理:{deleted_count} | 总数:{current_total}\n"

with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(log_msg)

print(log_msg.strip())
