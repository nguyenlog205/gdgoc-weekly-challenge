import pandas as pd
import numpy as np
import scipy.stats as ss

# -----------------------------------------------------------------
# 1. CRAMÉR'S V (Chữ vs Chữ) - Trả về (V, p-value)
# -----------------------------------------------------------------
def cramers_v(cat_col_1, cat_col_2):
    """
    Tính Cramér's V và P-value (dựa trên Chi-squared test).
    """
    # Xóa các dòng có NaN ở cả 2 cột để tránh lỗi
    data = pd.DataFrame({'c1': cat_col_1, 'c2': cat_col_2}).dropna()
    
    if data.empty: return 0.0, 1.0

    # Tạo bảng tần suất chéo
    contingency_table = pd.crosstab(data['c1'], data['c2'])
    
    # Nếu bảng quá nhỏ (ví dụ chỉ có 1 giá trị duy nhất), không tính được
    if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
        return 0.0, 1.0

    # Tính Chi-squared
    chi2_stat, p_value, dof, expected = ss.chi2_contingency(contingency_table)
    
    n = contingency_table.sum().sum()
    r, k = contingency_table.shape
    
    # Tính V
    min_dim = min(r - 1, k - 1)
    if min_dim == 0:
        v = 0.0
    else:
        v = np.sqrt((chi2_stat / n) / min_dim)
        
    return v, p_value

# -----------------------------------------------------------------
# 2. ETA-SQUARED (Chữ vs Số) - Trả về (Eta, p-value)
# -----------------------------------------------------------------
def eta_squared(categorical_col, numerical_col):
    """
    Tính Eta-squared và P-value (dựa trên ANOVA one-way).
    """
    # Gom dữ liệu và xóa NaN
    data = pd.DataFrame({'cat': categorical_col, 'val': numerical_col}).dropna()
    
    if data.empty: return 0.0, 1.0

    # --- Tính Eta Squared (Độ mạnh) ---
    overall_mean = data['val'].mean()
    
    # Tổng bình phương toàn bộ (SST)
    ss_total = ((data['val'] - overall_mean) ** 2).sum()
    
    # Nhóm dữ liệu theo category
    grouped = data.groupby('cat')['val']
    
    # Tổng bình phương giữa các nhóm (SSB)
    ss_between = 0
    groups_for_anova = [] # Chuẩn bị dữ liệu cho ANOVA
    
    for name, group in grouped:
        n_i = len(group)
        mean_i = group.mean()
        ss_between += n_i * ((mean_i - overall_mean) ** 2)
        groups_for_anova.append(group.values)
        
    if ss_total == 0:
        eta_sq = 0.0
    else:
        eta_sq = ss_between / ss_total

    # --- Tính P-value (bằng kiểm định ANOVA) ---
    # Cần ít nhất 2 nhóm để chạy ANOVA
    if len(groups_for_anova) < 2:
        p_value = 1.0
    else:
        # f_oneway trả về (F-statistic, p-value)
        _, p_value = ss.f_oneway(*groups_for_anova)

    # Căn bậc 2 của eta_sq để đưa về thang đo 0-1 tương tự như r (tùy chọn, thường dùng eta gốc)
    # Ở đây giữ nguyên Eta^2 vì nó là chuẩn đo lường mức độ ảnh hưởng
    return eta_sq, p_value

# -----------------------------------------------------------------
# 3. PEARSON (Số vs Số) - Trả về (r, p-value)
# -----------------------------------------------------------------
def pearson_w_p(num_col_1, num_col_2):
    """
    Wrapper cho hàm pearsonr của scipy để xử lý NaN trước.
    """
    data = pd.DataFrame({'n1': num_col_1, 'n2': num_col_2}).dropna()
    
    if len(data) < 2: return 0.0, 1.0
    
    r, p_value = ss.pearsonr(data['n1'], data['n2'])
    return r, p_value

# -----------------------------------------------------------------
# HÀM CHÍNH
# -----------------------------------------------------------------
def calculate_correlation_matrix(df):
    """
    Trả về 2 ma trận:
    1. Ma trận tương quan (Correlation Matrix)
    2. Ma trận P-value (P-value Matrix)
    """
    
    cols = df.columns
    corr_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
    pval_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
    
    # Phân loại cột
    numerical_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns

    for col1 in cols:
        for col2 in cols:
            # Đường chéo chính
            if col1 == col2:
                corr_matrix.loc[col1, col2] = 1.0
                pval_matrix.loc[col1, col2] = 0.0
                continue
            
            # Để tránh tính lặp lại (A vs B giống B vs A), ta có thể chỉ tính tam giác trên,
            # nhưng với Eta-squared (Chữ -> Số), A vs B khác B vs A về vai trò input/target.
            # Nên code này sẽ chạy full matrix để an toàn.
            
            val = 0.0
            p = 1.0
            
            # CASE 1: Số - Số (Pearson)
            if col1 in numerical_cols and col2 in numerical_cols:
                val, p = pearson_w_p(df[col1], df[col2])
                
            # CASE 2: Chữ - Chữ (Cramér's V)
            elif col1 in categorical_cols and col2 in categorical_cols:
                val, p = cramers_v(df[col1], df[col2])
                
            # CASE 3: Chữ (col1) - Số (col2) (Eta)
            elif col1 in categorical_cols and col2 in numerical_cols:
                val, p = eta_squared(df[col1], df[col2])
                
            # CASE 4: Số (col1) - Chữ (col2) (Eta ngược)
            elif col1 in numerical_cols and col2 in categorical_cols:
                val, p = eta_squared(df[col2], df[col1])

            corr_matrix.loc[col1, col2] = val
            pval_matrix.loc[col1, col2] = p
            
    return corr_matrix, pval_matrix