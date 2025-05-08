import os
import cv2
import random
from pathlib import Path


## 將目標資料夾改名成 "target_images"然後放在這個檔案同一層資料夾內
## 準備一個"backgrounds"資料夾，裡面放入背景圖片
##

# 設定標籤名稱
# 這裡的標籤名稱會影響到生成的 txt 檔案名稱
label_artist_name = "artist3"
label_class_number = 2

def random_paste(target_img, bg_img):
    th, tw = target_img.shape[:2]
    bh, bw = bg_img.shape[:2]

    # 初始隨機縮放比例
    scale = random.uniform(0.2, 0.6)
    new_w = int(tw * scale)
    new_h = int(th * scale)

    # 若縮放後仍大於背景，進一步壓縮
    if new_w > bw or new_h > bh:
        scale = min(bw / tw, bh / th) * 0.9  # 再保守一點
        new_w = int(tw * scale)
        new_h = int(th * scale)

        # 還是不合格就直接放棄（可選）
        if new_w <= 0 or new_h <= 0:
            raise ValueError("Target image is too small after resizing.")

    target_resized = cv2.resize(target_img, (new_w, new_h))

    x = random.randint(0, bw - new_w)
    y = random.randint(0, bh - new_h)

    # 將目標圖貼上背景
    bg_img_copy = bg_img.copy()
    bg_img_copy[y:y+new_h, x:x+new_w] = target_resized

    # 計算 YOLO 格式的 bounding box (中心點 + 寬高比例)
    x_center = (x + new_w / 2) / bw
    y_center = (y + new_h / 2) / bh
    w_norm = new_w / bw
    h_norm = new_h / bh

    return bg_img_copy, (label_class_number, x_center, y_center, w_norm, h_norm)  # class_id=0

def create_dataset(target_dir, background_dir, output_dir, count=100):
    Path(output_dir, "images").mkdir(parents=True, exist_ok=True)
    Path(output_dir, "labels").mkdir(parents=True, exist_ok=True)

    target_files = list(Path(target_dir).glob("*"))
    bg_files = list(Path(background_dir).glob("*"))

    for i in range(count):
        bg_path = random.choice(bg_files)
        target_path = random.choice(target_files)

        bg = cv2.imread(str(bg_path))
        target = cv2.imread(str(target_path))

        if bg is None or target is None:
            continue

        composed, yolo_box = random_paste(target, bg)
        img_name = f"{label_artist_name}_{i:04d}.jpg"
        label_name = f"{label_artist_name}_{i:04d}.txt"

        cv2.imwrite(str(Path(output_dir, "images", img_name)), composed)
        with open(Path(output_dir, "labels", label_name), "w") as f:
            f.write(" ".join(map(str, yolo_box)) + "\n")

    print(f"✅ 完成 {count} 張合成資料")

# 使用方式
create_dataset("target_images", "backgrounds", "output_dataset", count=200)
