from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_categorical_univariate(column, column_name):
    """
    Phân tích đơn biến cho các đặc trưng phân loại (categorical features).
    """

    print(f'\n- Phân tích đơn biến cho đặc trưng phân loại {column_name}')
    
    # =========================================
    # Đếm tần số của mỗi giá trị trong cột
    print(column.value_counts(dropna=False))


    # =========================================
    # Trực quan hóa phân phối của đặc trưng phân loại
    column_to_plot = column.fillna('Giá trị thiếu') # Thêm vào nhãn giá trị thiếu để plot, tạo thành một cột khác
    plt.figure(figsize=(10, 5))

    ax = sns.countplot(x=column_to_plot, palette='viridis', hue=column_to_plot, legend=False)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 5),
                    textcoords='offset points')
    
    plt.title(f'Phân phối của đặc trưng phân loại: {column_name}')
    plt.xlabel(f'Cột {column_name}')
    plt.ylabel('Tần số')
    plt.show()


def analyze_numerical_univariate(
    column, 
    column_name, 
    number_of_bins=30
):
    """
    Phân tích đơn biến cho các đặc trưng số (numerical features).
    Bao gồm thống kê mô tả và trực quan hóa (Histogram & Boxplot).
    """
    
    print(f'\n- Phân tích đơn biến cho đặc trưng số {column_name}')
    
    # =========================================
    # Mô tả thống kê và số giá trị thiếu (missing values)
    print(column.describe().round(2))

    missing_count = column.isnull().sum()
    print(f"\nSố lượng giá trị thiếu (NaN): {missing_count}")
    print(f'Tỉ lệ missing value: {missing_count / len(column) * 100:.2f}%')
    
    # =========================================
    # Trực quan hóa phân phối của đặc trưng phân loại (Histogram + KDE và Boxplot)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    sns.histplot(x=column, kde=True, ax=axes[0], bins=number_of_bins)
    axes[0].set_title(f'Phân phối (Histogram & KDE) của {column_name}', fontsize=14)
    axes[0].set_xlabel(column_name)
    axes[0].set_ylabel('Mật độ (Density)')
    
    sns.boxplot(x=column, ax=axes[1], color='lightblue')
    axes[1].set_title(f'Ngoại lai (Box Plot) của {column_name}', fontsize=14)
    axes[1].set_xlabel(column_name)
    
    plt.tight_layout()
    plt.show()




# ===============================================================
# HÀM DEBUG / TEST
# ===============================================================
def categorical_example():
    import seaborn as sns
    # Tải bộ dữ liệu mẫu từ seaborn
    df = sns.load_dataset('penguins')
    analyze_categorical_univariate(df['species'], 'species')

def numerical_example():
    import seaborn as sns
    # Tải bộ dữ liệu mẫu từ seaborn
    df = sns.load_dataset('penguins')
    analyze_numerical_univariate(df['bill_length_mm'], 'bill_length_mm', 30)

# categorical_example()
# numerical_example()