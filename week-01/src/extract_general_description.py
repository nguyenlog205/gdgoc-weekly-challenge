import pandas as pd
import time

def extract_general_description(df: pd.DataFrame) -> str:
    """
    Module này trích xuất mô tả tổng quan về bộ dữ liệu.
    """
    print('-'*31, 'MÔ TẢ TỔNG QUAN VỀ BỘ DỮ LIỆU','-'*30)

    # Đoạn code dưới đây trích xuất số mẫu và số đặc trưng từ lệnh .shape của DataFrame
    # <dataset>.shape trả về một tuple (số mẫu, số đặc trưng)
    n_samples, n_features = df.shape 
    time.sleep(0.1)
    print(f'Số mẫu: \t {n_samples}')
    print(f'Số đặc trưng: \t {n_features}')

    # Đoạn code dưới đây lần lượt trích xuất các thông tin về tên cột, kiểu dữ liệu, số giá trị null, số giá trị duy nhất
    time.sleep(0.1)
    summary_table = pd.DataFrame({
        'Tên cột': df.columns,
        'Kiểu dữ liệu': df.dtypes,
        'Số giá trị null': df.isnull().sum(),
        'Tỉ lệ giá trị null (%)': round(df.isnull().mean(), 4) * 100,
        'Số giá trị duy nhất': df.nunique()
    })
    print(f'\n{summary_table.to_string(index=False)}')

    # Đoạn code dưới đây trích xuất mô tả thống kê tổng quan của bộ dữ liệu
    print('\n','-'*29, 'THỐNG KÊ TỔNG QUAN VỀ BỘ DỮ LIỆU','-'*28)
    general_statistics = df.describe(include='all').to_string()
    print(f'\n {general_statistics}')

def example():
    import seaborn as sns
    # Tải bộ dữ liệu mẫu từ seaborn
    df = sns.load_dataset('penguins')
    extract_general_description(df)
