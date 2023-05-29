import socket
import struct
import threading
from tkinter import messagebox

import tkinter as tk

group_test = "224.1.1.1"
port_test = 3000
def check_input(group, port):
    # Kiểm tra xem địa chỉ multicast group có hợp lệ hay không
    try:
        socket.inet_pton(socket.AF_INET, group)
    except socket.error:
        messagebox.showerror("Lỗi", "Địa chỉ multicast group không hợp lệ!")
        return False

    # Kiểm tra xem port có hợp lệ hay không
    try:
        port = int(port)
        if not (1024 <= port <= 65535):
            raise ValueError
    except (ValueError, TypeError):
        messagebox.showerror("Lỗi", "Port không hợp lệ!")
        return False

    return True

def send_data():
    group = group_entry.get()
    port = port_entry.get()
    data = data_entry.get()
    if not check_input(group, port):
        return

    if not data:
        messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu gửi!")
        return

    # Tạo socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    # Gửi dữ liệu qua multicast
    sock.sendto(data.encode(), (group, int(port)))

def receive_data():
    group = group_entry.get()
    port = port_entry.get()
    if not check_input(group,port):
        return

    messagebox.showinfo("Thông báo", "Bắt đầu nhận dữ liệu!!")

    # Tạo socket và thiết lập các giá trị cần thiết
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', int(port)))
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Nhận dữ liệu từ multicast group

    while receiving:
        # Check if the window is closed
        if not root.winfo_exists():
            break

        try:
            data, addr = sock.recvfrom(1024)
            message_text.config(state=tk.NORMAL)
            print(f"Nhận từ {addr[0]}: {data.decode()}")
            message_text.insert(tk.END, "Nhận từ {}: {}\n".format(addr[0], data.decode()))
            message_text.config(state=tk.DISABLED)
        except socket.error:
            break


    sock.close()
#tạ thread chạy vòng lặp
def start_receiving():
    global receiving
    receiving = True
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.daemon = True
    receive_thread.start()


def stop_receiving():
    global receiving
    receiving = False
    messagebox.showinfo("Thông báo", "Đã ngừng nhận dữ liệu!!")

def reset_table():
    message_text.delete('1.0', tk.END)




# Tạo giao diện đồ họa
root = tk.Tk()
root.title("Multicast App")


group_label = tk.Label(root, text="Địa chỉ multicast group:")
group_label.pack()
group_entry = tk.Entry(root)
group_entry.pack()

port_label = tk.Label(root, text="Port:")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()

data_label = tk.Label(root, text="Nội dung dữ liệu:")
data_label.pack()
data_entry = tk.Entry(root, font=('Arial', 12), width=40)
data_entry.pack()


send_button = tk.Button(root, text="Gửi", command=send_data)
send_button.pack()

start_button = tk.Button(root, text="Bắt đầu nhận", command=start_receiving)
start_button.pack()

reset_button = tk.Button(root, text="Reset bảng", command=reset_table)
reset_button.pack()

message_label = tk.Label(root, text="Dữ liệu nhận được:")
message_label.pack()
message_text = tk.Text(root)
message_text.pack()
message_text.config(state=tk.DISABLED)

stop_button = tk.Button(root, text="Ngừng nhận", command=stop_receiving)
stop_button.pack()

root.mainloop()