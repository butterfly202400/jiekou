import os
import shutil
from datetime import datetime, timedelta, timezone

# ===== 配置与时间 =====
beijing_tz = timezone(timedelta(hours=8))
now = datetime.now(beijing_tz)
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_ROOT = os.path.join(ROOT_DIR, "backup")
BACKUP_DIR = os.path.join(BACKUP_ROOT, timestamp)
LOG_FILE = os.path.join(BACKUP_ROOT, "backup_log.txt")

# 确保备份根目录存在
os.makedirs(BACKUP_ROOT, exist_ok=True)

# ===== 备份 JSON 文件 =====
backup_count = 0
# 仅在备份文件夹不存在时创建，避免重复运行冲突
os.makedirs(BACKUP_DIR, exist_ok=True)

for filename in os.listdir(ROOT_DIR):
    filepath = os.path.join(ROOT_DIR, filename)
    
    # 核心改进：确保只处理文件，且排除备份目录本身
    if os.path.isfile(filepath) and filename.endswith(".json"):
        dest_path = os.path.join(BACKUP_DIR, filename)
        shutil.copy2(filepath, dest_path)
        backup_count += 1

# 如果本次没有备份任何文件，则删除空的备份文件夹
if backup_count == 0:
    os.rmdir(BACKUP_DIR)

# ===== 清理30天前备份 =====
deleted_count = 0
cutoff_time = now - timedelta(days=30)

for folder in os.listdir(BACKUP_ROOT):
    folder_path = os.path.join(BACKUP_ROOT, folder)
    
    if os.path.isdir(folder_path):
        try:
            # 仅解析符合时间格式的文件夹
            folder_time = datetime.strptime(folder, "%Y-%m-%d_%H-%M-%S")
            folder_time = folder_time.replace(tzinfo=beijing_tz)

            if folder_time < cutoff_time:
                shutil.rmtree(folder_path)
                deleted_count += 1
        except ValueError:
            # 跳过名称不符合日期格式的文件夹（如 log 文件夹或临时文件夹）
            continue

# ===== 写入日志 =====
log_entry = (
    f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
    f"成功备份: {backup_count} | 清理旧目录: {deleted_count}\n"
)

with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(log_entry)

print(f"任务执行完毕: {log_entry.strip()}")
