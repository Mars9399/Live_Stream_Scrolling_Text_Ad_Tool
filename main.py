import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                           QVBoxLayout, QHBoxLayout, QPushButton, QSlider, 
                           QFileDialog, QColorDialog, QFontDialog, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon
import os

class LyricLabel(QLabel):
    def __init__(self, parent=None):
        try:
            super(LyricLabel, self).__init__(parent)
            self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 左对齐且垂直居中
            self.font_size = 40
            self.text_color = QColor(Qt.white)
            self.current_font = QFont('Microsoft YaHei', self.font_size)
            self.setFont(self.current_font)
            self.setStyleSheet(f'color: {self.text_color.name()}')
            
            self.speed = 2
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.scroll_text)
            self.timer.start(30)
            
            self.text_lines = []
            self.current_line = 0
            self.offset = 0
            self.last_text_width = 0  # 保存上一行文本的宽度，用于无缝连接
            self.next_label = None  # 辅助标签，用于无缝连接下一轮
            self.cycle_spacing = 50  # 两轮字幕之间的间距（像素）
            self.setWordWrap(False)  # 禁用自动换行
            # 设置标签宽度足够大，确保文字完全显示
            self.setMinimumWidth(10000)  # 设置足够大的最小宽度
            # 使用字体度量获取实际高度，确保文字完全显示
            self.update_height()
        except Exception as e:
            print(f"LyricLabel初始化错误: {str(e)}")
            raise

    def scroll_text(self):
        try:
            if not self.text_lines:
                return
            
            parent_width = self.parent().width()
            
            # 更新主标签位置
            self.offset -= self.speed
            text_width = self.fontMetrics().width(self.text())
            self.update_position()
            
            # 计算文本的右边界位置（最后一个字的位置）
            text_right_edge = self.offset + text_width
            
            # 判断是否是最后一行
            is_last_line = (self.current_line == len(self.text_lines) - 1)
            
            # 当最后一行的右边界（最后一个字）滚动过屏幕最右侧时，创建辅助标签显示第一行
            if is_last_line and text_right_edge < parent_width and self.next_label is None:
                # 保存当前行（最后一行）的文本宽度和结束位置
                current_text_width = text_width
                current_end_position = self.offset + current_text_width
                
                # 创建辅助标签显示第一行，实现无缝连接
                self.next_label = QLabel(self.parent())
                self.next_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.next_label.setFont(self.current_font)
                self.next_label.setStyleSheet(f'color: {self.text_color.name()}')
                self.next_label.setText(self.text_lines[0])
                self.next_label.setWordWrap(False)
                self.next_label.setMinimumWidth(10000)
                self.next_label.setMinimumHeight(self.height())
                self.next_label.resize(self.width(), self.height())
                
                # 辅助标签从最后一行结束的位置开始，添加间距以区分每一轮字幕
                next_label_offset = current_end_position + self.cycle_spacing
                parent_height = self.parent().height()
                label_height = self.next_label.height()
                y_pos = max(0, (parent_height - label_height) // 2)
                self.next_label.move(next_label_offset, y_pos)
                self.next_label.show()
                
                print(f"创建辅助标签，第1行紧接在第{len(self.text_lines)}行后面，间距={self.cycle_spacing}px, offset={next_label_offset:.2f}")
            
            # 更新辅助标签位置（如果存在）
            if self.next_label:
                next_label_offset = self.next_label.x() - self.speed
                self.next_label.move(next_label_offset, self.next_label.y())
                
                # 当主标签完全离开左侧时，将辅助标签设为主标签
                if self.offset <= -text_width:
                    # 切换到第一行
                    self.current_line = 0
                    self.setText(self.text_lines[0])
                    # 主标签从辅助标签的位置开始（已经包含了间距）
                    self.offset = next_label_offset
                    # 删除辅助标签
                    self.next_label.deleteLater()
                    self.next_label = None
                    print(f"辅助标签转换为主标签，开始新一轮循环，offset={self.offset:.2f}")
            
            # 当文本完全滚动出视图左侧时，切换到下一行（中间切换，且没有辅助标签）
            elif self.offset <= -text_width and self.next_label is None:
                next_line_index = (self.current_line + 1) % len(self.text_lines)
                
                # 切换到下一行
                self.current_line = next_line_index
                self.setText(self.text_lines[self.current_line])
                
                # 中间切换：下一行从窗口右侧开始
                self.offset = parent_width
                print(f"切换到第 {self.current_line + 1} 行: {self.text_lines[self.current_line]}, offset={self.offset}")
                
        except Exception as e:
            print(f"滚动文本错误: {str(e)}")

    def update_height(self):
        """根据当前字体更新标签高度，确保文字完全显示"""
        try:
            # 使用fontMetrics获取字体的实际渲染高度
            # height() 返回字体的实际高度（包括上升和下降部分）
            font_height = self.fontMetrics().height()
            # 添加额外的边距以确保文字不被截断（上下各5像素）
            padding = 10
            new_height = font_height + padding
            self.setMinimumHeight(new_height)
            # 确保标签宽度足够大，以便显示完整文字
            # 保持当前宽度，只更新高度
            current_width = max(self.width(), 10000) if self.width() > 0 else 10000
            self.resize(current_width, new_height)
            # 更新垂直位置以确保居中
            self.update_position()
        except Exception as e:
            print(f"更新高度错误: {str(e)}")
    
    def update_position(self):
        """更新标签的垂直位置，确保在容器中居中"""
        try:
            if self.parent():
                parent_height = self.parent().height()
                label_height = self.height()
                y_pos = max(0, (parent_height - label_height) // 2)  # 垂直居中
                # 只更新y坐标，保持x坐标不变
                self.move(self.offset, y_pos)
        except Exception as e:
            print(f"更新位置错误: {str(e)}")
    
    def set_speed(self, speed):
        try:
            self.speed = speed
        except Exception as e:
            print(f"设置速度错误: {str(e)}")

    def set_text_color(self, color):
        try:
            self.text_color = color
            self.setStyleSheet(f'color: {self.text_color.name()}')
            # 如果存在辅助标签，删除它以避免重影，让滚动逻辑重新创建
            if self.next_label:
                self.next_label.deleteLater()
                self.next_label = None
        except Exception as e:
            print(f"设置颜色错误: {str(e)}")

    def set_font(self, font):
        try:
            self.current_font = font
            self.font_size = font.pointSize()
            self.setFont(self.current_font)
            # 使用字体度量更新高度，确保文字完全显示
            self.update_height()
            # 如果存在辅助标签，删除它以避免重影，让滚动逻辑重新创建
            if self.next_label:
                self.next_label.deleteLater()
                self.next_label = None
            if self.parent():
                self.offset = self.parent().width()  # 从父容器（窗口）的右侧开始滚动
                self.update_position()  # 更新位置
        except Exception as e:
            print(f"设置字体错误: {str(e)}")

    def set_font_size(self, size):
        try:
            self.font_size = size
            self.current_font.setPointSize(size)
            self.setFont(self.current_font)
            # 使用字体度量更新高度，确保文字完全显示
            self.update_height()
            # 如果存在辅助标签，删除它以避免重影，让滚动逻辑重新创建
            if self.next_label:
                self.next_label.deleteLater()
                self.next_label = None
            if self.parent():
                self.offset = self.parent().width()  # 从父容器（窗口）的右侧开始滚动
                self.update_position()  # 更新位置
        except Exception as e:
            print(f"设置字体大小错误: {str(e)}")

    def load_text_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取所有行，包括空行
                self.text_lines = [line.strip() for line in file.readlines()]
                if self.text_lines:
                    self.current_line = 0
                    self.setText(self.text_lines[0])
                    if self.parent():
                        self.offset = self.parent().width()  # 从父容器（窗口）的右侧开始滚动
                        self.update_position()  # 更新位置
                    print(f"加载了 {len(self.text_lines)} 行文本")
                    # 打印每行文本内容，用于调试
                    for i, line in enumerate(self.text_lines):
                        print(f"第 {i+1} 行: {line}")
                else:
                    print("文件为空")
        except Exception as e:
            print(f"加载文本文件错误: {str(e)}")
            self.text_lines = []

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(26, 26, 26, 200);
                border-radius: 5px;
                color: white;
            }
            QPushButton {
                background-color: rgba(51, 51, 51, 200);
                border: 1px solid rgba(102, 102, 102, 200);
                padding: 5px;
                border-radius: 3px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(68, 68, 68, 200);
            }
            QSlider::groove:horizontal {
                border: 1px solid rgba(102, 102, 102, 200);
                height: 8px;
                background: rgba(51, 51, 51, 200);
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: rgba(102, 102, 102, 200);
                border: 1px solid rgba(153, 153, 153, 200);
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 速度控制
        speed_layout = QVBoxLayout()
        speed_label = QLabel('速度:', self)
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(2)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        
        # 字体大小控制
        size_layout = QVBoxLayout()
        size_label = QLabel('字体大小:', self)
        self.size_slider = QSlider(Qt.Horizontal, self)
        self.size_slider.setMinimum(20)
        self.size_slider.setMaximum(100)
        self.size_slider.setValue(40)
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_slider)
        
        # 字体选择按钮
        self.font_button = QPushButton('选择字体', self)
        
        # 颜色选择按钮
        self.color_button = QPushButton('选择颜色', self)
        
        # 添加控件到布局
        layout.addLayout(speed_layout)
        layout.addLayout(size_layout)
        layout.addWidget(self.font_button)
        layout.addWidget(self.color_button)

class MainWindow(QMainWindow):
    def __init__(self):
        try:
            super(MainWindow, self).__init__()
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setWindowTitle("直播间滚动字幕广告工具")
            
            # 设置窗口图标
            icon_path = os.path.join(os.path.dirname(__file__), 'logo', 'favicon.ico')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            
            # 添加鼠标跟踪
            self.setMouseTracking(True)
            
            # 用于窗口拖动的变量
            self.dragging = False
            self.offset = None
            
            # 创建主窗口部件
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            
            # 创建布局
            self.layout = QVBoxLayout(self.central_widget)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)
            
            # 创建标签容器
            self.label_container = QWidget()
            self.label_container.setStyleSheet("background-color: transparent;")
            self.label_container.setFixedWidth(2500)  # 设置固定宽度
            # 设置标签容器背景透明
            self.label_container.setAttribute(Qt.WA_TranslucentBackground)
            
            # 创建标签
            self.label = LyricLabel(self.label_container)
            self.label.setParent(self.label_container)  # 设置父容器
            
            # 添加标签容器到主布局
            self.layout.addWidget(self.label_container)
            
            # 创建控制面板
            self.control_panel = ControlPanel(self)
            self.layout.addWidget(self.control_panel)
            
            # 根据初始字体大小设置正确的高度
            font_metrics = self.label.fontMetrics()
            # 使用height()而不是lineSpacing()，确保包含字体的上升和下降部分
            label_height = font_metrics.height() + 10
            control_panel_height = 60
            padding = 20
            self.label_container.setMinimumHeight(label_height)
            self.label_container.setFixedHeight(label_height)
            initial_height = label_height + control_panel_height + padding
            
            # 设置窗口大小
            self.resize(2500, initial_height)  # 使用计算出的高度
            
            # 初始隐藏控制面板
            self.control_panel.hide()
            
            # 安装事件过滤器
            self.label_container.installEventFilter(self)
            self.control_panel.installEventFilter(self)
            self.central_widget.installEventFilter(self)
            
            # 连接信号
            self.control_panel.speed_slider.valueChanged.connect(self.update_speed)
            self.control_panel.size_slider.valueChanged.connect(self.update_font_size)
            self.control_panel.font_button.clicked.connect(self.choose_font)
            self.control_panel.color_button.clicked.connect(self.choose_color)
            
            # 加载文本文件
            self.load_text_file()
            
            # 居中显示
            self.center_window()
            
            # 确保窗口显示在最前面
            self.activateWindow()
            self.raise_()
            
            # 设置窗口样式 - 初始状态透明
            self.setStyleSheet("""
                QMainWindow {
                    background-color: transparent;
                }
            """)
            # 设置窗口背景透明
            self.setAttribute(Qt.WA_TranslucentBackground)
            
            # 初始状态：背景透明
            self.is_mouse_over = False
            # 用于延迟检查鼠标是否离开的定时器
            self.hide_timer = QTimer(self)
            self.hide_timer.setSingleShot(True)
            self.hide_timer.timeout.connect(self.check_and_hide_controls)
            
            # 确保标签显示
            self.label.show()
            self.label_container.show()
        except Exception as e:
            print(f"MainWindow初始化错误: {str(e)}")
            print(traceback.format_exc())
            QMessageBox.critical(None, "错误", f"程序初始化失败: {str(e)}")
            raise

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.dragging = True
                self.offset = event.pos()
        except Exception as e:
            print(f"鼠标按下事件错误: {str(e)}")

    def mouseMoveEvent(self, event):
        try:
            if self.dragging and self.offset:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        except Exception as e:
            print(f"鼠标移动事件错误: {str(e)}")

    def mouseReleaseEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.dragging = False
                self.offset = None
        except Exception as e:
            print(f"鼠标释放事件错误: {str(e)}")

    def center_window(self):
        try:
            screen = QApplication.primaryScreen().geometry()
            size = self.geometry()
            x = (screen.width() - size.width()) // 2
            y = (screen.height() - size.height()) // 2
            self.move(x, y)
        except Exception as e:
            print(f"居中窗口错误: {str(e)}")

    def load_text_file(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, '打开文本文件', '', '文本文件 (*.txt)', options=options)
            if file_path:
                self.label.load_text_from_file(file_path)
        except Exception as e:
            print(f"加载文件错误: {str(e)}")
            self.label.setText("")
            
    def update_speed(self, value):
        try:
            self.label.set_speed(value)
        except Exception as e:
            print(f"更新速度错误: {str(e)}")

    def update_font_size(self, value):
        try:
            # 更新标签字体大小（这会自动更新标签高度）
            self.label.set_font_size(value)
            
            # 使用字体度量获取实际渲染高度
            font_metrics = self.label.fontMetrics()
            # 使用height()确保包含字体的上升和下降部分，避免文字被截断
            label_height = font_metrics.height() + 10  # 实际字体高度加边距
            control_panel_height = 60  # 控制面板固定高度
            padding = 20  # 上下边距
            
            # 设置标签容器的最小高度和固定高度
            self.label_container.setMinimumHeight(label_height)
            self.label_container.setFixedHeight(label_height)
            
            # 设置窗口的最小高度
            min_window_height = label_height + control_panel_height + padding
            self.setMinimumHeight(min_window_height)
            
            # 调整窗口大小
            self.resize(2500, min_window_height)
            
            # 确保标签位置更新（垂直居中）
            self.label.update_position()
            
            # 确保窗口显示在最前面
            self.raise_()
        except Exception as e:
            print(f"更新字体大小错误: {str(e)}")
        
    def choose_color(self):
        try:
            color = QColorDialog.getColor()
            if color.isValid():
                self.label.set_text_color(color)
        except Exception as e:
            print(f"选择颜色错误: {str(e)}")

    def choose_font(self):
        try:
            font, ok = QFontDialog.getFont(self.label.current_font, self)
            if ok:
                self.label.set_font(font)
                # 字体改变后，同步更新容器和窗口高度
                font_metrics = self.label.fontMetrics()
                # 使用height()确保包含字体的上升和下降部分
                label_height = font_metrics.height() + 10
                control_panel_height = 60
                padding = 20
                self.label_container.setMinimumHeight(label_height)
                self.label_container.setFixedHeight(label_height)
                min_window_height = label_height + control_panel_height + padding
                self.setMinimumHeight(min_window_height)
                self.resize(2500, min_window_height)
                # 确保标签位置更新（垂直居中）
                self.label.update_position()
        except Exception as e:
            print(f"选择字体错误: {str(e)}")

    def check_and_hide_controls(self):
        """检查鼠标是否真的离开了窗口，如果是则隐藏控制面板并恢复透明"""
        try:
            if not self.underMouse() and not self.label_container.underMouse() and not self.control_panel.underMouse():
                self.is_mouse_over = False
                self.setStyleSheet("""
                    QMainWindow {
                        background-color: transparent;
                    }
                """)
                self.label_container.setStyleSheet("background-color: transparent;")
                self.control_panel.hide()
        except Exception as e:
            print(f"检查隐藏控制面板错误: {str(e)}")
    
    def eventFilter(self, obj, event):
        try:
            if obj == self.label_container or obj == self.control_panel or obj == self.central_widget:
                if event.type() == event.Enter:
                    # 鼠标进入时取消隐藏定时器，显示背景和控制面板
                    self.hide_timer.stop()
                    self.is_mouse_over = True
                    self.setStyleSheet("""
                        QMainWindow {
                            background-color: rgba(26, 26, 26, 200);
                        }
                    """)
                    self.label_container.setStyleSheet("background-color: rgba(26, 26, 26, 200);")
                    self.control_panel.show()
                elif event.type() == event.Leave:
                    # 延迟检查，确保鼠标真的离开了窗口
                    # 使用定时器延迟100ms检查，避免快速移动时误判
                    self.hide_timer.start(100)
            return super().eventFilter(obj, event)
        except Exception as e:
            print(f"事件过滤错误: {str(e)}")
            return False

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # 设置应用程序图标
        icon_path = os.path.join(os.path.dirname(__file__), 'logo', 'favicon.ico')
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"程序运行错误: {str(e)}")
        print(traceback.format_exc())
        QMessageBox.critical(None, "错误", f"程序运行失败: {str(e)}")
        sys.exit(1)