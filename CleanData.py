import pandas as pd

# Function to clean the dataset
def clean_dataset(dataset_full):
    # Load the dataset
    data = pd.read_csv(dataset_full, encoding='utf-8')

    # Kiểm tra cấu trúc, định dạng dữ liệu
    data.info()
    data.head()

    # Kiểm tra và xóa dòng trùng lặp(nếu có)
    if data.duplicated().sum() > 0:
        data = data.drop_duplicates()
        print("Sum of duplicated rows deleted: ", data.duplicated().sum())#In ra số lượng dòng trùng đã xóa

    # Chuyển 'no_of_ratings' sang interger
    data['no_of_ratings'] = data['no_of_ratings'].str.replace(',', '', regex=True)#bỏ dấu "," thay giá trị không hợp lệ NaN
    data['no_of_ratings'] = pd.to_numeric(data['no_of_ratings'], errors='coerce')

    # Convert 'ratings' column to float, replacing invalid values with NaN
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')

    # Thay giá trị in colum "ratings"sang giá trị TB của cột
    mean_rating = data['ratings'].mean()
    data['ratings'].fillna(mean_rating, inplace=True)

    # Tạo tập con invalid_ratings để lưu các dòng trong cột ratings có giá trị NaN(dòng không thể chuyển qua kiểu float)
    invalid_ratings = data[data['ratings'].isna()]

    # Loại bỏ ký tự đặc biệt và dấu"," ở cột 'actual_price' and 'discount_price' và chuyển sang kiểu float thay giá trị không hợp lệ bằng NaN
    data['actual_price'] = data['actual_price'].str.replace("₹", '').str.replace(",", '')
    data['discount_price'] = data['discount_price'].str.replace("₹", '').str.replace(",", '')
    data['actual_price'] = pd.to_numeric(data['actual_price'], errors='coerce')
    data['discount_price'] = pd.to_numeric(data['discount_price'], errors='coerce')

    # Điền giá trị NaN của 'actual_price' and 'discount_price' bằng giá trị trung bình của cột
    data['actual_price'].fillna(data['actual_price'].mean(), inplace=True)
    data['discount_price'].fillna(data['discount_price'].mean(), inplace=True)

    # Fill NaN values in 'no_of_ratings' bằng giá trị trung bình của cột
    mean_no_of_ratings = data['no_of_ratings'].mean()
    data['no_of_ratings'].fillna(mean_no_of_ratings, inplace=True)

    # Lưu files mới (định dạng: tên file cũ + _cleaned)
    output_file = dataset_full.replace('.csv', '_cleaned.csv')
    data.to_csv(output_file, index=False)
    #in rhông báo dữ liệu đã được lưu ở đâu
    print("Cleaned data saved to:", output_file)
    return data, output_file #trả về dữ liệu đã làm sạch + tên file mới

# Đường dẫn files:
dataset_full = 'D:\\BI\\midterm-dataset\\dataset_full.csv'  # Ensure the path is correct
cleaned_data, new_dataset_file = clean_dataset(dataset_full)
