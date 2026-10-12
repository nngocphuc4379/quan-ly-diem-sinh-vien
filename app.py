import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📚",
    layout="wide"
)

# Tao du lieu
data = {
    "Ho_ten": [
        "Nguyen Van An", "Tran Thi Binh",
        "Le Hoang Nam", "Pham Minh Anh",
        "Vo Quoc Bao", "Dang Thu Ha",
        "Bui Gia Huy", "Hoang Ngoc Lan",
        "Do Minh Quan", "Nguyen Thao Vy"
    ],
    "Chuyen_can": [9.0, 8.0, 7.5, 9.5, 6.0, 8.5, 7.0, 9.0, 4.5, 8.0],
    "Giua_ky":    [8.5, 7.0, 6.5, 9.0, 5.5, 8.0, 7.5, 8.5, 4.0, 7.0],
    "Cuoi_ky":    [9.0, 7.5, 6.0, 9.5, 5.0, 8.5, 7.0, 9.0, 3.5, 7.5]
}

df = pd.DataFrame(data)

# Tinh diem tong ket
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
)

# Xep loai
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Tieu de
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý điểm bằng Python, Pandas và Streamlit.")

# Bang diem
st.subheader("1. Bảng điểm sinh viên")

bang = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang.round(2),
    use_container_width=True,
    hide_index=True
)

# Thong ke
st.subheader("2. Thống kê kết quả")

diem_tb = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_dat = int((df["Tong_ket"] >= 5).sum())

c1, c2, c3, c4 = st.columns(4)

c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{sv_max['Tong_ket']:.2f}")
c3.metric("Điểm thấp nhất", f"{sv_min['Tong_ket']:.2f}")
c4.metric("Sinh viên đạt", f"{so_dat}/10")

st.write("**Sinh viên điểm cao nhất:**", sv_max["Ho_ten"])
st.write("**Sinh viên điểm thấp nhất:**", sv_min["Ho_ten"])

# Selectbox
st.subheader("3. Tra cứu sinh viên")

ten = st.selectbox("Chọn sinh viên:", df["Ho_ten"].tolist())
sv = df[df["Ho_ten"] == ten].iloc[0]

st.write("**Họ tên:**", sv["Ho_ten"])

a, b, c, d, e = st.columns(5)
a.metric("Chuyên cần", f"{sv['Chuyen_can']:.2f}")
b.metric("Giữa kỳ", f"{sv['Giua_ky']:.2f}")
c.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.2f}")
d.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
e.metric("Xếp loại", sv["Xep_loai"])

# Bieu do
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Thong tin nguoi tao
st.divider()
st.caption("Nguyễn Ngọc Phúc | MSSV: [051208008671]")
