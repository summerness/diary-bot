# 自动生成日记项目

## 项目背景
我一直很喜欢看别人写的博客，觉得很有趣，但每次动手写时总是懒得动笔。于是我决定开发这个项目，让图片替我讲述一天的故事。只需每天上传几张图片，我的博客就能自动更新，省去了亲自动手写的麻烦。


## 技术栈
- **阿里云百炼**：用于图像分析和自然语言生成。
- **Halo 建站平台(https://www.halo.run/)**：用于托管和展示生成的博客内容。
- **Lsky 图床(https://github.com/lsky-org/lsky-pro)**：用于上传和存储图片。

## 安装与使用
1. 克隆本项目代码：
    ```bash
    git clone https://github.com/your-repo/diary-bot.git
    cd diary-bot
    ```

2. 安装依赖：
    ```bash
    pip install .
    ```

3. 配置相关服务：
    - 在 `.env` 中配置阿里云百炼、Lsky 图床及 Halo 平台的配置信息。

4. 运行项目：
    ```bash
    python main.py
    ```

## 示例

你可以在这里查看我的自动生成日记博客：[http://www.summerness.cc/](http://www.summerness.cc/)


