import csv
import random
import pandas as pd

# Lấy danh sách các thành phố
with open('us_cities.txt', 'r') as city_file:
    cities = [line.strip() for line in city_file]

# Tạo 100 lần ra 100 file khác nhau
files = []
for i in range(100):
    # Mỗi lần gen ra file có định dạng:
    new_csv_filename = f'new_data_{i+1}.csv'

    # Mở file csv đã cleaned để xử lý
    with open('dataset_cleaned.csv', 'r', encoding='utf-8') as original_csv, open(new_csv_filename, 'w', newline='', encoding='utf-8') as new_csv:
        reader = csv.reader(original_csv)
        writer = csv.writer(new_csv)

        # Add thêm profit và city ở đầu
        header = next(reader)
        header.extend(["profit", "city"])
        writer.writerow(header)

        # Đọc từ dòng rồi in ra profit random từ 1->5000 và city chọn ngẫu nhiên từ danh sách
        for row in reader:
            profit = random.randint(1, 5000)
            city = random.choice(cities)

            row = [cell.replace('\ufffd', '') for cell in row]

            row.extend([profit, city])
            writer.writerow(row)
    files.append(new_csv_filename)
    print(f"Created a new file '{new_csv_filename}' with 2 columns: profit and city.")

final_df = pd.read_csv(files[0])

# Đọc các file từ 1 -> 100 rồi hợp nhất lại
for file in files[1:]:
    df = pd.read_csv(file)
    final_df = pd.concat([final_df, df], ignore_index=True)

# Tạo thành file final_merged_file
merged_file = 'final_merged_file.csv'
final_df.to_csv(merged_file, index=False)
print(f"All files merged into {merged_file}")

df = pd.read_csv(merged_file)

# Order theo id giảm dần
sorted_df = df.sort_values(by="id", ascending=True)

# Thay thế id từ 0 đến tăng dần
sorted_df['id'] = range(len(sorted_df))

# Lưu lại thành file final_merged_file_sort.
output_file = "final_merged_file_sort.csv"
sorted_df.to_csv(output_file, index=False)

print(f"File sorted and 'id' column updated. Saved as {output_file}")
