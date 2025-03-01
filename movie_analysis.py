import pandas as pd

# Đọc file dữ liệu
file_path = "tmdb-movies.csv"
df = pd.read_csv(file_path)

# Chuẩn hóa cột ngày phát hành
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Chuyển đổi năm về định dạng phù hợp (năm > 25 là 19XX, năm <= 25 là 20XX)
df['release_date'] = df['release_date'].apply(lambda x: x.replace(year=x.year - 100) if x.year > 2025 else x)

# Loại bỏ dòng trùng lặp
df = df.drop_duplicates()

# Loại bỏ các dòng có giá trị thiếu trong các cột quan trọng
df = df.dropna(subset=['cast', 'director', 'genres'])

# Loại bỏ các bộ phim có doanh thu hoặc ngân sách bằng 0
df = df[(df['revenue'] > 0) & (df['budget'] > 0)]

# 1. Sắp xếp phim theo ngày phát hành giảm dần
df_sorted = df.sort_values(by='release_date', ascending=False)
df_sorted.to_csv("sorted_movies.csv", index=False)
print("Danh sách phim sau khi sắp xếp theo ngày phát hành giảm dần:")
print(df_sorted[['original_title', 'release_date']].head(10))

# 2. Lọc phim có điểm đánh giá trung bình trên 7.5
df_high_rated = df[df['vote_average'] > 7.5]
df_high_rated.to_csv("high_rated_movies.csv", index=False)
print("Danh sách phim có điểm đánh giá trên 7.5:")
print(df_high_rated[['original_title', 'vote_average']].head(10))

# 3. Tìm phim có doanh thu cao nhất và thấp nhất
highest_revenue_movie = df.loc[df['revenue'].idxmax()]
lowest_revenue_movie = df.loc[df['revenue'].idxmin()]
print(f"Phim có doanh thu cao nhất: {highest_revenue_movie['original_title']} - {highest_revenue_movie['revenue']}")
print(f"Phim có doanh thu thấp nhất: {lowest_revenue_movie['original_title']} - {lowest_revenue_movie['revenue']}")

# 4. Tính tổng doanh thu
total_revenue = df['revenue'].sum()
print(f"Tổng doanh thu của tất cả phim: {total_revenue}")

# 5. Top 10 phim có lợi nhuận cao nhất
df['profit'] = df['revenue'] - df['budget']
top_10_profitable = df.nlargest(10, 'profit')
top_10_profitable.to_csv("top_profitable_movies.csv", index=False)
print("Top 10 phim có lợi nhuận cao nhất:")
print(top_10_profitable[['original_title', 'profit']])

# 6. Đạo diễn có nhiều phim nhất và diễn viên đóng nhiều phim nhất
top_director = df['director'].value_counts().idxmax()
top_actor = df['cast'].str.split('|').explode().value_counts().idxmax()
print(f"Đạo diễn có nhiều phim nhất: {top_director}")
print(f"Diễn viên đóng nhiều phim nhất: {top_actor}")

# 7. Thống kê số lượng phim theo thể loại
genre_counts = df['genres'].str.split('|').explode().value_counts()
genre_counts.to_csv("genre_counts.csv")
print("Thống kê số lượng phim theo thể loại:")
print(genre_counts)

# 8. Ý tưởng phân tích bổ sung
# - Phân tích xu hướng phim theo năm
# - Tính điểm trung bình của phim theo thể loại
# - So sánh doanh thu giữa các đạo diễn hàng đầu

# Lưu kết quả
results = {
    "highest_revenue_movie": highest_revenue_movie['original_title'],
    "lowest_revenue_movie": lowest_revenue_movie['original_title'],
    "total_revenue": total_revenue,
    "top_director": top_director,
    "top_actor": top_actor
}

print("Kết quả tổng hợp:")
print(results)
