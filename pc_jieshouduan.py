import os
import socket
import json
import subprocess
from threading import Thread

def get_file_type(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return 'image'
    elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
        return 'video'
    elif ext in ['.mp3', '.wav', '.flac', '.aac']:
        return 'audio'
    elif ext in ['.txt', '.pdf', '.doc', '.docx']:
        return 'text'
    else:
        return 'other'

class SocketServerThread(Thread):
    def __init__(self, port, receive_dir):
        super().__init__()
        self.port = port
        self.running = False
        self.receive_dir = receive_dir

    def run(self):
        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port))
        sock.listen(1)

        print(f"Socket服务器已启动，监听端口 {self.port}")

        while self.running:
            try:
                conn, addr = sock.accept()
                data = conn.recv(1024).decode()
                if data == "RUN_TUPIANZHENGTI":
                    # 执行tupianzhengti.py文件
                    try:
                        subprocess.run(['python', 'tupianzhengti.py'], check=True)
                        print("tupianzhengti.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"tupianzhengti.py执行失败: {e}")

                elif data == "tupianzhengti_jiem":
                    # 执行tupianzhengti_jiem.py文件
                    try:
                        subprocess.run(['python', 'tupianzhengti_jiem.py'], check=True)
                        print("tupianzhengti_jiem.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"tupianzhengti_jiem.py执行失败: {e}")

                elif data == "shuiyin1_jia":
                    # 执行shuiyin1_jia.py文件
                    try:
                        subprocess.run(['python', 'shuiyin1_jia.py'], check=True)
                        print("shuiyin1_jia.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"shuiyin1_jia.py执行失败: {e}")

                elif data == "shuiyin1_jie":
                    # 执行shuiyin1_jie.py文件
                    try:
                        subprocess.run(['python', 'shuiyin1_jie.py'], check=True)
                        print("shuiyin1_jie.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"shuiyin1_jie.py执行失败: {e}")

                elif data == "shipin_jia":
                    # 执行shipin_jia.py文件
                    try:
                        subprocess.run(['python', 'shipin_jia.py'], check=True)
                        print("shipin_jia.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"shipin_jia.py执行失败: {e}")

                elif data == "shipin_jie":
                    # 执行shipin_jie.py文件
                    try:
                        subprocess.run(['python', 'shipin_jie.py'], check=True)
                        print("shipin_jie.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"shipin_jie.py执行失败: {e}")
                
                elif data == "shipinshuiyin_jia":
                    # 执行shipinshuiyin_jia.py文件
                    try:
                        subprocess.run(['python', 'shipinshuiyin_jia.py'], check=True)
                        print("shipinshuiyin_jia.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"shipinshuiyin_jia.py执行失败: {e}")

                elif data == "shipinshuiyin_jie":
                    # 执行shipinshuiyin_jie.py文件
                    try:
                        subprocess.run(['python', 'shipinshuiyin_jie.py'], check=True)
                        print("shipinshuiyin_jie.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"shipinshuiyin_jie.py执行失败: {e}")

                elif data == "RUN_JIA2":
                    # 执行jia2.py文件
                    try:
                        subprocess.run(['python', 'jia2.py'], check=True)
                        print("jia2.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"jia2.py执行失败: {e}")

                elif data == "renlianjiemi":
                    # 执行renlianjiemi.py文件
                    try:
                        subprocess.run(['python', 'renlianjiemi.py'], check=True)
                        print("renlianjiemi.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"renlianjiemi.py执行失败: {e}")

                elif data == "yinpin_jia":
                    # 执行yinpin_jia.py文件
                    try:
                        subprocess.run(['python', 'yinpin_jia.py'], check=True)
                        print("yinpin_jia.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"yinpin_jia.py执行失败: {e}")

                elif data == "yinpin_jie":
                    # 执行yinpin_jie.py文件
                    try:
                        subprocess.run(['python', 'yinpin_jie.py'], check=True)
                        print("yinpin_jie.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"yinpin_jie.py执行失败: {e}")

                elif data == "yinpin_shuiyin_jia":
                    # 执行yinpin_shuiyin_jia.py文件
                    try:
                        subprocess.run(['python', 'yinpin_shuiyin_jia.py'], check=True)
                        print("yinpin_shuiyin_jia.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"yinpin_shuiyin_jia.py执行失败: {e}")

                elif data == "yinpin_shuiyin_jie":
                    # 执行yinpin_shuiyin_jie.py文件
                    try:
                        subprocess.run(['python', 'yinpin_shuiyin_jie.py'], check=True)
                        print("yinpin_shuiyin_jie.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"yinpin_shuiyin_jie.py执行失败: {e}")

                elif data == "wenbenjiami":
                    # 执行wenbenjiami.py文件
                    try:
                        subprocess.run(['python', 'wenbenjiami.py'], check=True)
                        print("wenbenjiami.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"wenbenjiami.py执行失败: {e}")

                elif data == "wenbenjiemi":
                    # 执行wenbenjiemi.py文件
                    try:
                        subprocess.run(['python', 'wenbenjiemi.py'], check=True)
                        print("wenbenjiemi.py执行成功")
                    except subprocess.CalledProcessError as e:
                        print(f"wenbenjiemi.py执行失败: {e}")
                        
                else:
                    self.handle_connection(conn, addr, data)
            except Exception:
                break

        sock.close()

    def stop(self):
        self.running = False
        # 创建一个临时连接来中断accept
        try:
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_sock.connect(('192.168.50.133', self.port))
            temp_sock.close()
        except Exception:
            pass

    def handle_connection(self, conn, addr, data):
        try:
            # 接收文件信息
            file_info = json.loads(data)
            file_name = file_info['file_name']
            file_size = file_info['file_size']
            file_type = file_info['file_type']

            # 根据文件类型设置固定文件名
            if file_type == 'image':
                save_name = 'tupian.png'
            elif file_type == 'video':
                save_name = 'shipin.mp4'
            elif file_type == 'audio':
                save_name = 'yinpin.mp3'
            elif file_type == 'text':
                save_name = 'wenben.txt'
            else:
                save_name = file_name  # 其他类型使用原始文件名

            # 通知发送端已准备好
            conn.send("READY".encode())

            # 准备接收文件
            save_path = os.path.join(self.receive_dir, save_name)
            received_bytes = 0

            with open(save_path, 'wb') as f:
                while received_bytes < file_size:
                    data = conn.recv(4096)
                    if not data:
                        break
                    f.write(data)
                    received_bytes += len(data)

            # 确认接收完成
            conn.send("RECEIVED".encode())
            conn.close()

            print(f"已成功接收文件: {save_path} (类型: {file_type})")
        except Exception as e:
            print(f"Socket接收错误: {str(e)}")

if __name__ == '__main__':
    socket_port = 8001
    receive_dir = "received_files"

    # 创建接收目录
    if not os.path.exists(receive_dir):
        os.makedirs(receive_dir)

    # 启动Socket服务器线程
    socket_thread = SocketServerThread(socket_port, receive_dir)
    socket_thread.start()