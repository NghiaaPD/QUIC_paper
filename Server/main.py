import socket
import struct
import pickle
import cv2

server_ip = ''
server_port =

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

print("Đang chờ kết nối từ máy khách...")

client_socket, client_address = server_socket.accept()
print(f"Kết nối từ: {client_address}")

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)

    cv2.imshow("Nhận từ máy khách", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Đóng kết nối
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
