
# createDate.py - 合成圖像資料集產生器

## 📄 簡介
此腳本可自動將前景圖片（目標）隨機縮放與貼合到背景圖上，並以 YOLO 格式產生標註檔案，適合用於目標檢測任務的資料集建構。

## 📁 資料夾結構

請依照以下結構準備資料：

```
.
├── createDate.py
├── target_images/       # 放置前景物件圖像（欲辨識的目標）
├── backgrounds/         # 放置背景圖片
└── output_dataset/      # 程式自動產生的合成圖片與標註資料夾
```

## ⚙️ 使用方法

直接執行 `createDate.py` 即可，預設會產生 200 張合成圖像：

```bash
python createDate.py
```

可透過修改程式尾端的 `create_dataset(...)` 呼叫參數來調整生成數量與資料夾位置：

```python
create_dataset("target_images", "backgrounds", "output_dataset", count=200)
```

## 🏷️ 標註格式

每張圖片會產生一個對應的 `.txt` 標註檔案，採用 YOLO 格式：

```
<class_id> <x_center> <y_center> <width> <height>
```

所有數值皆為相對座標（比例），中心點與寬高的值皆介於 0 到 1 之間。

## 🔧 設定項目

可修改腳本頂部的以下變數設定：

```python
label_artist_name = "artist3"  # 圖片與標註檔的前綴名稱
label_class_number = 2         # 對應的 class_id
```

## 📦 套件需求

請先安裝必要的 Python 套件：

```bash
pip install opencv-python
```

## ✅ 執行結果

程式執行完畢後，會於 `output_dataset/images/` 生成合成圖像，
並在 `output_dataset/labels/` 生成對應的 YOLO 標註檔案。



## 🖼️ 合成示意圖

下圖示範了將前景圖貼合至背景後的合成結果：

<p align="center">
  <img src="https://github.com/klo4634321/labelImg-Demo/blob/main/Demonstration_Image/target.jpg" height = "200" width="200"/>
  <strong>+</strong>
  <img src="https://github.com/klo4634321/labelImg-Demo/blob/main/Demonstration_Image/bg.jpg" height = "200" width="200"/>
  <strong>=</strong>
  <img src="https://github.com/klo4634321/labelImg-Demo/blob/main/Demonstration_Image/output.jpg" height = "200" width="200"/>
</p>


