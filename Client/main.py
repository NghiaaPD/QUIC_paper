import cv2
import socket
import struct
import pickle

server_ip = ''
server_port =

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

video_path = "Traffic.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Hoàn thành gửi video.")
        break

    data = pickle.dumps(frame)

    message = struct.pack("Q", len(data)) + data

    client_socket.sendall(message)

cap.release()
client_socket.close()
