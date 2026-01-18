# 直播间滚动字幕广告工具

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

一个基于 PyQt5 的直播间滚动字幕广告工具，支持无缝循环滚动、透明背景、字体和颜色自定义等功能，专为直播场景设计，实现类似音乐播放软件的字幕效果。

**GitHub**: [https://github.com/Mars9399/Live_Stream_Scrolling_Text_Ad_Tool](https://github.com/Mars9399/Live_Stream_Scrolling_Text_Ad_Tool)

## 功能特性

### 核心功能
- ✅ **无缝循环滚动**：支持多行文本无缝循环滚动，头尾无缝连接
- ✅ **透明背景**：鼠标移开后背景自动透明，只显示文字
- ✅ **字体自定义**：支持自定义字体、字体大小和颜色
- ✅ **速度调节**：可调节滚动速度（1-10级）
- ✅ **文本文件加载**：支持从文本文件加载字幕内容

### 界面特性
- 🎨 **音乐播放器风格**：鼠标悬停时显示半透明背景和控制面板
- 🎨 **自动隐藏控制面板**：鼠标移开后自动隐藏，保持界面简洁
- 🎨 **轮次区分**：每轮字幕之间自动添加间距，便于区分

## 安装要求

### 系统要求
- Windows 10/11
- Python 3.6+

### 依赖库
```bash
pip install PyQt5
```

## 使用方法

### 1. 运行程序
```bash
python main.py
```

### 2. 加载广告文本文件
- 程序启动后会自动弹出文件选择对话框
- 选择包含广告内容的文本文件（.txt格式）
- 每行文本将作为一条广告字幕滚动显示

### 3. 控制选项
鼠标悬停在窗口上时，会显示控制面板：

- **速度滑块**：调节滚动速度（1-10级）
- **字体大小滑块**：调节字体大小（20-100）
- **选择字体按钮**：打开字体选择对话框
- **选择颜色按钮**：打开颜色选择对话框

### 4. 窗口操作
- **拖动窗口**：点击窗口任意位置并拖动，可放置在直播画面任意位置
- **自动透明**：鼠标移开后窗口背景自动透明，不影响直播画面
- **置顶显示**：窗口始终显示在最前面，确保广告内容始终可见

## 文件结构

```
Live_Stream_Scrolling_Text_Ad_Tool/
├── main.py              # 主程序文件
├── logo/                # 图标目录
│   ├── favicon.ico      # 窗口图标
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   ├── apple-touch-icon.png
│   └── site.webmanifest
├── README.md            # 说明文档
├── LICENSE              # Apache-2.0 许可证
└── .gitignore          # Git 忽略文件配置
```

## 技术实现

### 核心类说明

#### LyricLabel
滚动字幕标签类，负责文本的滚动显示：
- `scroll_text()`: 实现文本滚动逻辑
- `set_font_size()`: 设置字体大小
- `set_text_color()`: 设置文字颜色
- `load_text_from_file()`: 从文件加载文本

#### MainWindow
主窗口类，负责界面和交互：
- `update_font_size()`: 更新字体大小并调整窗口高度
- `choose_font()`: 字体选择对话框
- `choose_color()`: 颜色选择对话框
- `eventFilter()`: 鼠标事件处理，实现透明背景切换

### 关键技术点

1. **无缝循环实现**
   - 使用辅助标签（next_label）实现头尾无缝连接
   - 当最后一行的右边界离开窗口右侧时，创建辅助标签显示第一行
   - 主标签完全离开后，辅助标签转换为主标签

2. **透明背景实现**
   - 使用 `setAttribute(Qt.WA_TranslucentBackground)` 实现窗口透明
   - 通过事件过滤器监听鼠标进入/离开事件
   - 使用 QTimer 延迟检查，避免快速移动时的误判

3. **字体高度自适应**
   - 使用 `fontMetrics().height()` 获取字体实际渲染高度
   - 动态调整标签、容器和窗口高度，确保文字不被截断

## 使用示例

### 创建广告文本文件
创建一个 `ads.txt` 文件，每行一条广告内容：
```
欢迎关注直播间，点赞加关注不迷路
进群领取专属福利，优惠券等你来拿
新品上架限时特价，错过再等一年
```

### 运行程序
1. 双击运行 `main.py` 或使用命令行：`python main.py`
2. 选择广告文本文件
3. 广告字幕开始滚动显示
4. 鼠标悬停可调节字体、颜色、速度等参数
5. 将窗口放置在直播画面合适位置，开始直播

## 常见问题

### Q: 如何调整两轮字幕之间的间距？
A: 在代码中修改 `LyricLabel` 类的 `cycle_spacing` 属性（默认50像素）。

### Q: 支持哪些文本格式？
A: 目前支持 UTF-8 编码的 .txt 文本文件，每行一条广告内容。

### Q: 适合哪些直播平台？
A: 适用于所有支持窗口捕获的直播软件（如 OBS、XSplit 等），通过窗口捕获功能将字幕窗口添加到直播画面中。

### Q: 如何与直播软件配合使用？
A: 
1. 运行本程序并加载广告文本
2. 在 OBS 等直播软件中添加"窗口捕获"源
3. 选择本程序的窗口
4. 调整窗口位置和大小到合适位置
5. 开始直播，广告字幕会自动滚动显示

## 更新日志

### v1.0.0 (2026)
- ✅ 实现基本滚动字幕功能
- ✅ 支持字体、颜色、速度自定义
- ✅ 实现透明背景和自动隐藏控制面板
- ✅ 实现无缝循环滚动
- ✅ 添加窗口图标
- ✅ 支持多行文本无缝连接
- ✅ 字体大小自适应，确保文字完整显示

## 许可证

本项目采用 [Apache-2.0](LICENSE) 许可证。

## 作者
Mars Xu

Created with ❤️ using PyQt5

## 贡献

欢迎提交 Issue 和 Pull Request！

### 如何贡献
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 致谢

感谢使用本工具！如果对你有帮助，欢迎给个 ⭐ Star！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 [Issue](https://github.com/Mars9399/Live_Stream_Scrolling_Text_Ad_Tool/issues)
- 发送 Pull Request
