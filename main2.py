import sys
import os
import time
import cv2
import numpy as np
import requests
import socket
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QMessageBox, QStackedWidget
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
from PyQt5.QtGui import QPixmap, QImage,QPalette, QBrush
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QGridLayout
from PyQt5 import QtCore


# 常量定义
UPLOADS_DIR = 'uploads'
# ENCRYPT_SCRIPT = 'main_encrypt.py'
# ENCRYPTED_IMAGE = 'encrypted_wensheng.png'
# DECRYPTED_IMAGE = 'jiemi.png'
RECEIVER_IP = '192.168.50.133'  # 接收端IP地址
RECEIVER_SOCKET_PORT = 8001

uploads_dir = 'uploads'
receiver_ip = '192.168.50.29'  # 后端服务器IP
receiver_socket_port = 5001    # 后端socket端口
receiver_http_port = 5000      # 后端HTTP端口
backend_url = f'http://{receiver_ip}:{receiver_http_port}/upload'

class EncryptionDecryptionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_file = None
        self.last_displayed_file = None  # 记录上次显示的文件路径
        
        # 设置定时器检查后端文件
        self.check_timer = QTimer(self)
        
        self.check_timer.timeout.connect(self.check_for_received_file)
        self.check_timer.start(40000)  # 每秒检查一次

    def check_for_received_file(self):
        """检查后端是否有新文件，只显示最新的文件"""
        try:
            if os.path.exists(uploads_dir):
                # 获取目录下所有文件，按修改时间排序
                files = [os.path.join(uploads_dir, f) 
                         for f in os.listdir(uploads_dir) 
                         if os.path.isfile(os.path.join(uploads_dir, f))]
                
                if files:
                    # 找到最新的文1件
                    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                    latest_file = files[0]
                    self.display_received_file(latest_file)
                    
                    # 如果是新文件且与上次显示的不同
                    # if latest_file != self.last_displayed_file:
                    #     self.last_displayed_file = latest_file
                    #     self.display_received_file(latest_file)
                        
                        # 清理旧文件（可选）
                    for old_file in files[1:]:
                        try:
                            os.remove(old_file)
                            print(f"已清理旧文件: {old_file}")
                        except Exception as e:
                            print(f"清理文件失败: {e}")
        except Exception as e:
            print(f"检查接收文件时出错: {e}")

    def submit_initial_values(self):
        x = self.input_edit["x:"].text()  # Note: Changed to use "x:" to match the key in input_edit
        y = self.input_edit["y:"].text()
        z = self.input_edit["z:"].text()
        w = self.input_edit["w:"].text()
        print(f"提交的初始值：x={x}, y={y}, z={z}, w={w}")
        # 可在这里编写将这些值用于加密流程的逻辑，比如传给加密函数作为参数
    
        # Show success message
        QMessageBox.information(self, "成功", "密钥已上传", QMessageBox.Ok)
    
        # Clear input fields
        for edit in self.input_edit.values():
            edit.clear()

    def initUI(self):
        # 创建主布局
        main_layout = QHBoxLayout(self)  # 修改为主水平布局
        
        # 设置窗口大小为图片尺寸
        self.resize(1920, 1080)
    
        # 设置背景图片
        self.setAutoFillBackground(True)
        palette = self.palette()
    
        # 加载背景图片
        background_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aaa.png')
        if os.path.exists(background_path):
            background = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            print("未找到背景图片 beijing.png")
            # 如果没有背景图片，设置为白色背景
            self.setStyleSheet("background-color: white;")
        
        # 创建左侧按钮区域
        button_area = QWidget(self)
        button_area.setStyleSheet("background-color: rgba(40, 40, 40, 200); border-radius: 10px;")
        button_layout = QVBoxLayout(button_area)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(15, 30, 15, 30)
        

         # 标题
        init_value_label = QLabel("初始值", button_area)
        init_value_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        init_value_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(init_value_label)

        # 输入框布局
        input_layout = QGridLayout()
        input_labels = ["x:", "y:", "z:", "w:"]
        self.input_edit = {}
        for idx, label_text in enumerate(input_labels):
            label = QLabel(label_text, button_area)
            label.setStyleSheet("color: white; font-size: 18px;")
            edit = QLineEdit(button_area)
            edit.setStyleSheet("background-color: white; color: #333; border-radius: 5px; padding: 5px;")
            input_layout.addWidget(label, idx, 0)
            input_layout.addWidget(edit, idx, 1)
            self.input_edit[label_text] = edit

        button_layout.addLayout(input_layout)

        # 提交按钮
        # submit_layout = QHBoxLayout()
        submit_button = QPushButton("提交", button_area)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 18px;
                border: none;
                min-width: 100px;
                max-width: 150px; 
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1a252f;
            }
        """)
        # submit_button.clicked.connect(self.submit_initial_values)  # 绑定提交逻辑
        # button_layout.addWidget(submit_button)
        submit_button.clicked.connect(self.submit_initial_values)  # Connect the button click
        button_layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        button_area.layout().addWidget(submit_button, alignment=Qt.AlignCenter) 

        # 创建按钮分组
        button_names = [
            "加密/加水印", 
            "图像整体加密", 
            "图像局部加密", 
            "图像添加水印", 
            "视频局部加密", 
            "视频添加水印",
            "音频加密",
            "音频添加水印",
            "文本加密",

            "解密/去水印", 
            "图像整体解密", 
            "图像局部解密", 
            "图像去除水印", 
            "视频局部解密", 
            "视频去除水印",
            "音频解密",
            "音频去除水印",
            "文本解密",
        ]
        
        # 定义加密和解密按钮组
        self.encryption_buttons = [
            "图像整体加密", 
            "图像局部加密", 
            "图像添加水印", 
            "视频局部加密", 
            "视频添加水印",
            "音频加密",
            "音频添加水印",
            "文本加密"
        ]
        
        self.decryption_buttons = [
            "图像整体解密",
            "图像局部解密", 
            "图像去除水印", 
            "视频局部解密", 
            "视频去除水印",
            "音频解密",
            "音频去除水印",
            "文本解密"
        ]
        
        # 使用字典存储按钮和对应的处理函数
        self.buttons = {}
        for name in button_names:
            button = QPushButton(name, button_area)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: white;
                    padding: 45px 40px;
                    border-radius: 8px;
                    font-size: 30px;
                    text-align: left;
                    border: none;
                    margin: 5px 0;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
                QPushButton:pressed {
                    background-color: #1a252f;
                }
                QPushButton:checked {
                    background-color: #3498db;
                }
            """)
            button.setFixedHeight(50)
            button.setCheckable(True)  # 设置为可选中状态
            
            # 初始隐藏加密和解密子按钮
            if name in self.encryption_buttons + self.decryption_buttons:
                button.setVisible(False)
            
            button_layout.addWidget(button)
            self.buttons[name] = button
            
            # 为每个按钮连接到通用处理函数
            button.clicked.connect(lambda checked, btn_name=name: self.button_clicked(btn_name))
        
        # 添加拉伸项，使按钮居上
        button_layout.addStretch()
        
        # 创建右侧内容区域
        content_area = QWidget(self)
        content_area.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 10px;")
        content_layout = QVBoxLayout(content_area)

        # 创建显示区域布局
        display_layout = QHBoxLayout()

        # 创建第一个显示框，用于显示原始内容
        self.display1 = QLabel(content_area)
        self.display1.setFixedSize(520, 520)
        self.display1.setStyleSheet("background-color: #f5f5f5; border-radius: 5px;")
        self.display1.setAlignment(Qt.AlignCenter)
        self.display1.setText("请选择文件...")
        display_layout.addWidget(self.display1)

        # 创建第二个显示框，用于显示处理后的内容
        self.display2 = QLabel(content_area)
        self.display2.setFixedSize(520, 520)
        self.display2.setStyleSheet("background-color: #f5f5f5; border-radius: 5px;")
        self.display2.setAlignment(Qt.AlignCenter)
        self.display2.setText("处理结果将显示在这里")
        display_layout.addWidget(self.display2)

        # 将显示区域添加到内容布局
        content_layout.addLayout(display_layout)

        # 创建文件选择按钮 (现在在显示框下方)
        self.file_button = QPushButton("添加文件", content_area)
        self.file_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 20px 30px;
                border-radius: 5px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.file_button.clicked.connect(self.add_file)
        content_layout.addWidget(self.file_button)

        # 添加一些边距
        content_layout.setContentsMargins(20, 20, 20, 20)

        # 将按钮区域和内容区域添加到主布局
        main_layout.addWidget(button_area, 1)  # 按钮区域占1份
        main_layout.addWidget(content_area, 4)  # 内容区域占4份    
        
        # 设置窗口标题和大小
        self.setWindowTitle('加密解密界面')
        self.resize(1300, 650)  # 调整窗口宽度以适应左侧按钮
        
        # 确保上传目录存在
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        
        # 模拟发送文件并显示
        # self.send_and_display_file()  # 注释掉，避免启动时自动发送文件

    def button_clicked(self, button_name):
        # 重置所有按钮状态
        for name, btn in self.buttons.items():
            btn.setChecked(name == button_name)
        
        # 根据点击的按钮执行相应操作
        print(f'执行操作: {button_name}')
        
        # 处理主按钮点击
        if button_name == "加密/加水印":
            # 切换加密子按钮的显示状态
            show = not self.buttons[self.encryption_buttons[0]].isVisible()
            for btn_name in self.encryption_buttons:
                self.buttons[btn_name].setVisible(show)
            # 隐藏解密子按钮
            for btn_name in self.decryption_buttons:
                self.buttons[btn_name].setVisible(False)
        
        elif button_name == "解密/去水印":
            # 切换解密子按钮的显示状态
            show = not self.buttons[self.decryption_buttons[0]].isVisible()
            for btn_name in self.decryption_buttons:
                self.buttons[btn_name].setVisible(show)
            # 隐藏加密子按钮
            for btn_name in self.encryption_buttons:
                self.buttons[btn_name].setVisible(False)
        
        # 根据按钮名称执行不同的处理逻辑
        if button_name == "加密/加水印":
            self.perform_general_encryption()
        elif button_name == "图像整体加密":
            self.perform_image_full_encryption()
        elif button_name == "图像局部加密":
            self.perform_image_partial_encryption()
        elif button_name == "图像添加水印":
            self.perform_image_watermark()
        elif button_name == "视频局部加密":
            self.perform_video_partial_encryption()
        elif button_name == "视频添加水印":
            self.perform_video_watermark()
        elif button_name == "音频加密":
            self.yinpinjiami()
        elif button_name == "音频添加水印":
            self.yinpinshuiyinjiami()
        elif button_name == "文本加密":
            self.wenbenjiami()

        elif button_name == "解密/去水印":
            self.perform_general_decryption()
        elif button_name == "图像整体解密":
            self.perform_image_full_decryption()
        elif button_name == "图像局部解密":
            self.perform_image_partial_decryption()
        elif button_name == "图像去除水印":
            self.perform_image_remove_watermark()
        elif button_name == "视频局部解密":
            self.perform_video_partial_decryption()
        elif button_name == "视频去除水印":
            self.perform_video_remove_watermark()
        elif button_name == "音频解密":
            self.yinpin_jie()
        elif button_name == "音频去除水印":
            self.yinpinshuiyinjiemi()
        elif button_name == "文本解密":
            self.wenbenjiemi()

    def add_file(self):
        """添加文件并显示在display1中"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", 
            "所有文件 (*);;图像文件 (*.jpg *.jpeg *.png *.bmp *.gif);;视频文件 (*.mp4 *.avi *.mov *.mkv);;音频文件 (*.mp3 *.wav *.flac *.aac);;文本文件 (*.txt *.pdf *.docx)"
        )
        
        if not file_path:
            return
            
        self.current_file = file_path
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 根据文件类型处理
        if self.is_image(file_ext):
            self.display_image(file_path)
        elif self.is_video(file_ext):
            self.display_video(file_path)
        elif self.is_audio(file_ext):
            self.display_audio(file_path)
        elif self.is_text(file_ext):
            self.display_text(file_path)
        else:
            self.display1.setText(f"不支持的文件类型: {file_ext}")
        
        # 发送文件到接收端
        self.send_file_to_receiver(file_path)

    def send_file_to_receiver(self, file_path):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))

            # 发送文件信息
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_type = self.get_file_type(file_name)
            file_info = {
                'file_name': file_name,
                'file_size': file_size,
                'file_type': file_type
            }
            sock.send(json.dumps(file_info).encode())

            # 等待接收端准备好
            response = sock.recv(1024).decode()
            if response == "READY":
                # 发送文件内容
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        sock.send(data)

                # 等待接收端确认
                response = sock.recv(1024).decode()
                if response == "RECEIVED":
                    print("文件发送成功")
            sock.close()
        except Exception as e:
            print(f"文件发送失败: {e}")
    
    def is_image(self, ext):
        return ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    def is_video(self, ext):
        return ext in ['.mp4', '.avi', '.mov', '.mkv']
    
    def is_audio(self, ext):
        return ext in ['.mp3', '.wav', '.flac', '.aac']
    
    def is_text(self, ext):
        return ext in ['.txt', '.pdf', '.docx']
    
    def display_image(self, file_path):
        """显示图像文件"""
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.display1.setText("无法加载图像")
            return
            
        self.display1.setPixmap(pixmap.scaled(
            self.display1.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))
    
    def display_video(self, file_path):
        """显示视频文件"""
        # 如果已经有视频播放器，先释放资源
        if hasattr(self, 'video_player'):
            self.video_player.stop()
            self.video_player.deleteLater()
        
        # 创建视频播放器和视频显示部件
        self.video_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self.display1)
        self.video_widget.setGeometry(0, 0, 520, 520)
        self.video_widget.show()
        
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.video_player.play()
    
    def display_audio(self, file_path):
        """显示音频文件"""
        # 如果已经有音频播放器，先释放资源
        if hasattr(self, 'audio_player'):
            self.audio_player.stop()
            self.audio_player.deleteLater()
        
        # 创建音频播放器
        self.audio_player = QMediaPlayer(None)
        self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.audio_player.play()
        
        # 显示音频文件信息
        file_name = os.path.basename(file_path)
        self.display1.setText(f"正在播放音频: {file_name}")
    
    def display_text(self, file_path):
        """显示文本文件，支持自动换行"""
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            
                # 设置文本并开启自动换行（适用于QLabel）
                self.display1.setText(text)
                self.display1.setWordWrap(True)  # 开启自动换行
                self.display1.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # 允许文本选择

            else:
                self.display1.setText(f"暂不支持预览此类文本文件: {os.path.splitext(file_path)[1]}")
        except Exception as e:
            self.display1.setText(f"无法读取文件: {str(e)}")

    def display_received_file(self, file_path):
        """在display2中显示接收到的文件"""
        # 先清空显示
        self.clear_display2()
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if self.is_image(file_ext):
                self.display_image_in_display2(file_path)
            elif self.is_video(file_ext):
                self.display_video_in_display2(file_path)
            elif self.is_audio(file_ext):
                self.display_audio_in_display2(file_path)
            elif self.is_text(file_ext):
                self.display_text_in_display2(file_path)
            else:
                self.display2.setText(f"不支持的文件类型: {file_ext}")
        except Exception as e:
            self.display2.setText(f"显示文件出错: {str(e)}")

    def clear_display2(self):
        """清空第二个显示框"""
        
        # 如果有视频播放器，先停止
        if hasattr(self, 'video_player2'):
            self.video_player2.stop()
            self.video_player2.deleteLater()
            del self.video_player2
        
        # 如果有音频播放器，先停止
        if hasattr(self, 'audio_player2'):
            self.audio_player2.stop()
            self.audio_player2.deleteLater()
            del self.audio_player2
        
        # 清除图像或文本
        self.display2.clear()
        self.display2.setText("处理结果将显示在这里")
    
    def display_image_in_display2(self, file_path):
        """在display2中显示图像文件"""
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.display2.setText("无法加载图像")
            return
            
        self.display2.setPixmap(pixmap.scaled(
            self.display2.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))
    
    def display_video_in_display2(self, file_path):
        """在display2中显示视频文件"""
        # 如果已经有视频播放器，先释放资源
        if hasattr(self, 'video_player2'):
            self.video_player2.stop()
            self.video_player2.deleteLater()
            
        
        # 创建视频播放器和视频显示部件
        self.video_player2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget2 = QVideoWidget(self.display2)
        self.video_widget2.setGeometry(0, 0, 520, 520)
        self.video_widget2.show()
        
        self.video_player2.setVideoOutput(self.video_widget2)
        self.video_player2.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.video_player2.play()
    
    def display_audio_in_display2(self, file_path):
        # 如果已经有音频播放器，先释放资源
        if hasattr(self, 'audio_player2'):
            self.audio_player2.stop()
            self.audio_player2.deleteLater()
        
        # 创建音频播放器
        self.audio_player2 = QMediaPlayer(None)
        self.audio_player2.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.audio_player2.play()
        
        # 显示音频文件信息
        file_name = os.path.basename(file_path)
        self.display2.setText(f"正在播放接收到的音频: {file_name}")
    
    # def display_text_in_display2(self, file_path):
    #     """在display2中显示文本文件"""
    #     try:
    #         if file_path.endswith('.txt'):
    #             with open(file_path, 'r', encoding='utf-8') as f:
    #                 text = f.read(5000)  # 限制读取的字符数，避免过大
    #                 if len(text) == 5000:
    #                     text += "\n\n... 文件内容过长，已省略部分内容 ..."
    #             self.display2.setText(text)
    #         else:
    #             self.display2.setText(f"暂不支持预览此类文本文件: {os.path.splitext(file_path)[1]}")
    #     except Exception as e:
    #         self.display2.setText(f"无法读取文件: {str(e)}")

    def display_text_in_display2(self, file_path):
        """在display2中显示文本文件"""
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            
                # 设置文本并开启自动换行（适用于QLabel）
                self.display2.setText(text)
                self.display2.setWordWrap(True)  # 开启自动换行
                self.display2.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # 允许文本选择

            else:
                self.display2.setText(f"暂不支持预览此类文本文件: {os.path.splitext(file_path)[1]}")
        except Exception as e:
            self.display2.setText(f"无法读取文件: {str(e)}")

    # 以下是原有的各个功能的处理函数，保持不变
    def perform_general_encryption(self):
        print("执行加密/加水印操作")
        # 实际处理代码...

    def perform_image_full_encryption(self):
        print("执行图像整体加密操作")
        # 通知接收端执行tupianzhengti.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("RUN_TUPIANZHENGTI".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行tupianzhengti.py失败: {e}")

    def perform_image_partial_encryption(self):
        print("执行图像局部加密操作")
        # 通知接收端执行jia2.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("RUN_JIA2".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行jia2.py失败: {e}")

    def perform_image_watermark(self):
        print("执行图像添加水印操作")
        # 通知接收端执行shuiyin1_jia.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("shuiyin1_jia".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行shuiyin1_jia.py失败: {e}")

    def perform_video_partial_encryption(self):
        print("执行视频局部加密操作")
        # 通知接收端执行shipin_jia.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("shipin_jia".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行shipin_jia.py失败: {e}")

    def perform_video_watermark(self):
        print("执行视频添加水印操作")
        # 通知接收端执行shipinshuiyin_jia.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("shipinshuiyin_jia".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行shipinshuiyin_jia.py失败: {e}")

    def yinpinjiami(self):
        print("执行音频加密操作")
        # 通知接收端执行yinpin_jia.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("yinpin_jia".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行yinpin_jia.py失败: {e}")

    def yinpinshuiyinjiami(self):
        print("执行音频添加水印操作")
        # 通知接收端执行yinpin_shuiyin_jia.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("yinpin_shuiyin_jia".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行yinpin_shuiyin_jia.py失败: {e}")

    def wenbenjiami(self):
        print("执行文本加密操作")
        # 通知接收端执行wenbenjiami.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("wenbenjiami".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行wenbenjiami.py失败: {e}")

    def perform_general_decryption(self):
        print("执行解密/去水印操作")
        # 实际处理代码...

    def perform_image_full_decryption(self):
        print("执行图像整体解密操作")
        # 通知接收端执行tupianzhengti_jiem.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("tupianzhengti_jiem".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行tupianzhengti_jiem.py失败: {e}")

    def perform_image_partial_decryption(self):
        print("执行图像局部解密操作")
        # 通知接收端执行renlianjiemi.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("renlianjiemi".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行renlianjiemi.py失败: {e}")

    def perform_image_remove_watermark(self):
        print("执行图像去除水印操作")
        # 通知接收端执行shuiyin1_jie.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("shuiyin1_jie".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行shuiyin1_jie.py失败: {e}")

    def perform_video_partial_decryption(self):
        print("执行视频局部解密操作")
        # 通知接收端执行shipin_jie.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("shipin_jie".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行shipin_jie.py失败: {e}")

    def perform_video_remove_watermark(self):
        print("执行视频去除水印操作")
        # 通知接收端执行shipinshuiyin_jie.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("shipinshuiyin_jie".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行shipinshuiyin_jie.py失败: {e}")

    def yinpin_jie(self):
        print("执行音频解密操作")
        # 通知接收端执行yinpin_jie.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("yinpin_jie".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行yinpin_jie.py失败: {e}")

    def yinpinshuiyinjiemi(self):
        print("执行音频去除水印操作")
        # 通知接收端执行yinpin_shuiyin_jie.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("yinpin_shuiyin_jie".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行yinpin_shuiyin_jie.py失败: {e}")

    def wenbenjiemi(self):
        print("执行w文本解密操作")
        # 通知接收端执行wenbenjiemi.py文件
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((RECEIVER_IP, RECEIVER_SOCKET_PORT))
            sock.send("wenbenjiemi".encode())
            sock.close()
        except Exception as e:
            print(f"通知接收端执行wenbenjiemi.py失败: {e}")

    # 以下是原有的辅助函数，保持不变
    def is_image_supported(self, file_path=None):
        # 简单判断是否为支持的图像格式，可根据需要扩展
        if file_path is None:
            file_path = 'your_local_file_path'  # 这里替换为实际要发送的文件路径
            
        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            return file_extension in ['.jpg', '.jpeg', '.png', '.bmp']
        return False

    def get_file_type(self, file_name):
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

class LoginWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录界面')
    
     # 设置窗口大小为图片尺寸
        self.resize(1920, 1080)
    
        # 设置背景图片
        self.setAutoFillBackground(True)
        palette = self.palette()
    
        # 加载背景图片
        background_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aaa.png')
        if os.path.exists(background_path):
            background = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            print("未找到背景图片 beijing.png")
            # 如果没有背景图片，设置为白色背景
            self.setStyleSheet("background-color: white;")
        
        # 创建一个半透明的容器，用于放置登录控件
        container = QWidget(self)
        container.setFixedSize(440, 300)
        # 设置半透明白色背景
        container.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 10px;")

        main_layout = QVBoxLayout(container)

        welcome_label = QLabel('请输入您的信息：')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(welcome_label)

        account_layout = QHBoxLayout()
        account_label = QLabel('账号')
        account_label.setStyleSheet("font-size: 14px;")
        self.account_input = QLineEdit()
        self.account_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_input)
        main_layout.addLayout(account_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel('密码')
        password_label.setStyleSheet("font-size: 14px;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        # 新增“注册账号”和“忘记密码”按钮布局
        button_layout = QHBoxLayout()
        register_button = QPushButton('注册账号')
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #f4f4f4;
                color: #333;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        register_button.clicked.connect(self.register_account)  # 连接槽函数
        button_layout.addWidget(register_button)

        forget_password_button = QPushButton('忘记密码')
        forget_password_button.setStyleSheet("""
            QPushButton {
                background-color: #f4f4f4;
                color: #333;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        forget_password_button.clicked.connect(self.forget_password)  # 连接槽函数
        button_layout.addWidget(forget_password_button)
        main_layout.addLayout(button_layout)

        # 添加一些间距
        main_layout.addSpacing(15)

        login_button = QPushButton('登录')
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #4286f4;
                color: white;
                padding: 7px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3a78d9;
            }
            QPushButton:pressed {
                background-color: #3266b8;
            }
        """)
        login_button.clicked.connect(self.login_check)
        main_layout.addWidget(login_button)

        # 新增人脸登录按钮
        face_login_button = QPushButton('人脸登录')
        face_login_button.setStyleSheet("""
            QPushButton {
                background-color: #4286f4;
                color: white;
                padding: 7px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3a78d9;
            }
            QPushButton:pressed {
                background-color: #3266b8;
            }
        """)
        face_login_button.clicked.connect(self.open_face_recognition)
        main_layout.addWidget(face_login_button)

        # 设置布局间距
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 将容器居中显示在主窗口中
        central_layout = QVBoxLayout(self)
        central_layout.addStretch(1)
        central_layout.addWidget(container, alignment=Qt.AlignCenter)
        central_layout.addStretch(1)
        
        # 设置窗口大小
        self.resize(800, 600)

    def login_check(self):
        input_account = self.account_input.text()
        input_password = self.password_input.text()
        if input_account == '123' and input_password == '123':
            print('登录成功')
            self.stacked_widget.setCurrentIndex(1)  # 切换到加密解密界面
        else:
            self.show_error_message()

    def show_error_message(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("密码错误")
        msg_box.setWindowTitle("错误")
        msg_box.exec_()

    def open_face_recognition(self):
        self.stacked_widget.setCurrentIndex(2)  # 切换到人脸识别界面

    def register_account(self):
        print("注册账号功能待实现")

    def forget_password(self):
        print("忘记密码功能待实现")

class FaceRecognitionWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # # 加载已知人脸图像
        # try:
        #     known_image = cv2.imread('face.jpg')
        #     if known_image is None:
        #         raise FileNotFoundError("未找到 face.jpg 文件，请检查文件是否存在。")
        #     known_gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)
        #     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #     known_faces = face_cascade.detectMultiScale(known_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        #     if len(known_faces) == 0:
        #         raise ValueError("在已知人脸图像中未检测到人脸，请更换图像。")
        #     (x, y, w, h) = known_faces[0]
        #     known_face = known_gray[y:y + h, x:x + w]
        #     self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        #     self.recognizer.train([known_face], np.array([0]))
        # except (FileNotFoundError, ValueError) as e:
        #     print(e)
                # 加载已知人脸图像
        try:
            known_image = cv2.imread('face.jpg')
            if known_image is None:
                raise FileNotFoundError("未找到 face.jpg 文件，请检查文件是否存在。")
            known_gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            known_faces = face_cascade.detectMultiScale(known_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(known_faces) == 0:
                raise ValueError("在已知人脸图像中未检测到人脸，请更换图像。")
            (x, y, w, h) = known_faces[0]
            known_face = known_gray[y:y + h, x:x + w]
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.train([known_face], np.array([0]))
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def perform_face_recognition(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            id_, confidence = self.recognizer.predict(face)
            
            # 关键修改：添加相似度阈值判断
            if confidence < 60:  # 阈值可调整，值越小表示要求越严格
                QMessageBox.information(self, "认证结果", "认证成功")
                self.stacked_widget.setCurrentIndex(1)  # 切换到加密解密界面
            else:
                # 人脸不匹配时抛出错误
                QMessageBox.critical(self, "认证失败", "检测到的人脸与模板不匹配！")
                result = QMessageBox.question(self, "提示", "是否使用账号密码登录？", QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    self.stacked_widget.setCurrentIndex(0)  # 切换到登录界面
                break  # 找到一张人脸后就退出循环，避免多重弹窗
        else:
            # 没有检测到人脸的情况
            QMessageBox.warning(self, "警告", "未检测到人脸，请调整位置")

    def initUI(self):
        # 设置窗口大小
        self.resize(1920, 1080)

        # 设置背景图片
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aaa.png')
        if os.path.exists(background_path):
            background = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            print("未找到背景图片 aaa.png")
            self.setStyleSheet("background-color: white;")

        # 主垂直布局
        main_layout = QVBoxLayout()
        # 添加伸缩项，用于让中间内容上下居中
        main_layout.addStretch()

        # 标题水平布局（用于放置“人脸登录界面”标题）
        title_layout = QHBoxLayout()
        self.title_label = QLabel("人脸登录界面")
        # 可设置标题字体大小等样式，这里简单示例
        self.title_label.setStyleSheet("""
            font-size: 60px; 
            color: red; 
            font-weight: bold; 
            background-color: rgba(0, 0, 0, 0);  /* 半透明黑色背景，可选 */
            padding: 15px;  /* 上下左右内边距，让标题不贴着边缘 */
        """)
        title_layout.addStretch()
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)

        # 摄像头显示区域水平布局，用于让摄像头框水平居中
        video_layout = QHBoxLayout()
        video_layout.addStretch()
        self.video_label = QLabel(self)
        # 可设置摄像头显示区域的固定大小等，根据实际需求调整
        self.video_label.setFixedSize(QSize(640, 480))  
        video_layout.addWidget(self.video_label)
        video_layout.addStretch()
        main_layout.addLayout(video_layout)
    
        # 按钮水平布局，用于让按钮水平居中
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.recognize_button = QPushButton('进行人脸认证')
        self.recognize_button.setStyleSheet("""
            QPushButton {
                background-color: #4286f4;
                color: white;
                padding: 12px 24px;  /* 增加内边距让按钮更大 */
                border-radius: 5px;
                font-size: 16px;     /* 增加字体大小 */
                min-width: 700px;    /* 设置最小宽度 */
            }
            QPushButton:hover {
                background-color: #3a78d9;
            }
            QPushButton:pressed {
                background-color: #3266b8;
            }
        """)

        self.recognize_button.clicked.connect(self.perform_face_recognition)
        button_layout.addWidget(self.recognize_button)
        button_layout.addStretch()

        # 创建一个容器widget来设置按钮的外边距
        button_container = QWidget()
        button_container.setLayout(button_layout)
        button_container.setContentsMargins(0, 10, 0, 0)  # 上边距10px，实现下移

        main_layout.addWidget(button_container)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)

            # 检测人脸并绘制蓝色框
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # 绘制蓝色框 (BGR格式)

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_img).scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.video_label.setPixmap(pixmap)

    def perform_face_recognition(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                id_, confidence = self.recognizer.predict(face)
                if confidence < 100:
                    QMessageBox.information(self, "认证结果", "认证成功")
                    self.stacked_widget.setCurrentIndex(1)  # 切换到加密解密界面
                else:
                    QMessageBox.critical(self, "认证结果", "认证失败，请重新认证")
                    result = QMessageBox.question(self, "提示", "是否使用账号密码登录？", QMessageBox.Yes | QMessageBox.No)
                    if result == QMessageBox.Yes:
                        self.stacked_widget.setCurrentIndex(0)  # 切换到登录界面

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('可移动加密')
        
        # 创建堆叠窗口部件
        self.stacked_widget = QStackedWidget()

        # 添加登录界面，将stacked_widget传递给LoginWidget
        login_widget = LoginWidget(self.stacked_widget)
        self.stacked_widget.addWidget(login_widget)

        # 添加加密解密界面
        viewer = EncryptionDecryptionWidget()
        self.stacked_widget.addWidget(viewer)

        # 添加人脸识别界面，将stacked_widget传递给FaceRecognitionWidget
        face_recognition_widget = FaceRecognitionWidget(self.stacked_widget)
        self.stacked_widget.addWidget(face_recognition_widget)
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 创建主窗口和堆叠窗口部件
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())
