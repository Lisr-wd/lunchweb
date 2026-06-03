# 🎙️ 语音备忘录 Android APK

将 `voice-memo.html` 封装为原生 Android WebView 应用。

## 功能特性

- ✅ 录音（调用麦克风权限）
- ✅ 实时语音转写（Chrome WebView 支持 Web Speech API）
- ✅ AI 精转（Whisper API，需配置密钥）
- ✅ 闹钟播报（定时播放录音）
- ✅ 本地存储（IndexedDB/localStorage）
- ✅ 全屏沉浸式体验

---

## 方法一：本地构建（推荐）

### 前置要求

1. 下载并安装 [Android Studio](https://developer.android.com/studio)（自带 JDK 和 Android SDK）

### 步骤

```bash
# 1. 在 Android Studio 中打开此文件夹
File → Open → 选择 voice-memo-android 文件夹

# 2. 等待 Gradle 同步完成（首次需要下载依赖，约 5-10 分钟）

# 3. 生成图标（可选，需要 Python + Pillow）
python generate_icons.py

# 4. 构建 Release APK
Build → Generate Signed Bundle/APK → APK → debug

# 或使用命令行（在 Android Studio Terminal 中）
./gradlew assembleRelease

# 5. APK 路径
app/build/outputs/apk/release/app-release.apk
```

---

## 方法二：GitHub Actions 云端构建（无需本地环境）

### 步骤

1. 在 GitHub 创建一个新仓库（可私有）

2. 将此文件夹推送到仓库：
   ```bash
   git init
   git add .
   git commit -m "init: voice memo android app"
   git remote add origin https://github.com/你的用户名/仓库名.git
   git push -u origin main
   ```

3. 等待 GitHub Actions 自动构建（约 5-8 分钟）

4. 在仓库的 **Actions** 标签页 → 点击最新的 workflow run → 下载 **voice-memo-release** artifact

5. 解压后得到 `.apk` 文件，发送到手机安装

---

## 安装 APK 到手机

1. **Android 手机** → 设置 → 安全 → 开启**允许未知来源安装**
2. 将 APK 文件传输到手机（USB、微信、邮件均可）
3. 点击 APK 文件安装

---

## 注意事项

- **Web Speech API**：Android Chrome WebView 支持（需联网），录音实时转写可用
- **离线使用**：录音、播放、闹钟均可完全离线使用；实时转写需要联网
- **存储**：数据保存在应用 WebView localStorage 中，卸载应用数据会清空
- **权限**：首次启动会弹出麦克风权限申请，请允许

---

## 文件结构

```
voice-memo-android/
├── app/
│   ├── src/main/
│   │   ├── assets/index.html         ← 语音备忘录主页面
│   │   ├── java/.../MainActivity.java ← WebView 容器
│   │   ├── AndroidManifest.xml        ← 权限声明
│   │   └── res/                       ← 图标、布局、样式
│   └── build.gradle
├── .github/workflows/build.yml        ← 云端自动构建
├── build.gradle
├── settings.gradle
├── gradlew / gradlew.bat
└── generate_icons.py                  ← 图标生成脚本
```
