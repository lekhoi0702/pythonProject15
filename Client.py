import socket
import tkinter as tk
from tkinter import messagebox

def send_data():
    # Lấy địa chỉ multicast group, cổng và dữ liệu từ giao diện người dùng
    group = group_entry.get()
    port = port_entry.get()
    data = data_entry.get()

    try:
        # Kiểm tra địa chỉ multicast group và cổng
        socket.inet_pton(socket.AF_INET, group)
        port = int(port)
    except (socket.error, ValueError):
        messagebox.showerror("Lỗi", "Địa chỉ multicast group hoặc cổng không hợp lệ!")
        return

    # Tạo socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Gửi dữ liệu đến multicast group
    sock.sendto(data.encode(), (group, port))

    # Đóng socket
    sock.close()

    # Xóa nội dung nhập trong ô dữ liệu
    data_entry.delete(0, tk.END)

# Tạo giao diện đồ họa
root = tk.Tk()
root.title("Multicast Client")

group_label = tk.Label(root, text="Địa chỉ multicast group:")
group_label.pack()
group_entry = tk.Entry(root)
group_entry.pack()

port_label = tk.Label(root, text="Cổng:")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()

data_label = tk.Label(root, text="Dữ liệu:")
data_label.pack()
data_entry = tk.Entry(root)
data_entry.pack()

send_button = tk.Button(root, text="Gửi", command=send_data)
send_button.pack()

root.mainloop()
