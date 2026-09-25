<p align="center">
  <img src="logo.png" alt="Meta Automation Logo" width="140" style="border-radius: 28px; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);" />
</p>

<h1 align="center">⚡ Meta Automation - Auto Meta on Meta.ai</h1>

<p align="center">
  <strong>Scale your creative workflow with automated batch prompts, image & video generation, and hands-free media downloads on Meta.ai.</strong>
</p>

<p align="center">
  <a href="https://github.com/abidalidevv"><img src="https://img.shields.io/badge/Version-2.2.3-6366f1?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Version 2.2.3" /></a>
  <a href="https://developer.chrome.com/docs/extensions/mv3/intro/"><img src="https://img.shields.io/badge/Manifest-V3-10b981?style=for-the-badge&logo=webcomponents&logoColor=white" alt="Manifest V3" /></a>
  <a href="https://abidalidev.com"><img src="https://img.shields.io/badge/Author-Abid%20Ali%20Dev-8b5cf6?style=for-the-badge&logo=codeforces&logoColor=white" alt="Author Abid Ali Dev" /></a>
  <a href="https://ko-fi.com/abidalidev"><img src="https://img.shields.io/badge/Support-Ko--fi-ff5e5b?style=for-the-badge&logo=kofi&logoColor=white" alt="Support on Ko-fi" /></a>
  <img src="https://img.shields.io/badge/Platform-Chrome%20%7C%20Edge%20%7C%20Brave-3b82f6?style=for-the-badge" alt="Platform Support" />
</p>

---

## 🌟 Overview

**Meta Automation** is a high-performance, developer-friendly Chrome Extension designed for creators, marketers, AI artists, and power users who generate AI media at scale on [Meta.ai](https://www.meta.ai). 

Instead of manually entering prompts one by one and waiting for each generation to complete, **Meta Automation** runs autonomously in your browser's native **Chrome Side Panel**—allowing you to queue dozens of prompts, generate videos and images in parallel, and automatically download the results directly to organized local folders.

---

## ✨ Key Features

- 🚀 **Batch Prompt Processing**: Queue multiple prompts simultaneously using custom delimiter or spreadsheet/CSV imports.
- 🎬 **Multi-Modal Generation**:
  - **Text to Video**: Bulk generate smooth 5s AI video clips with prompt delays.
  - **Image to Video**: Automatically feed seed images to animate them into video sequences.
  - **Text to Image & Image to Image**: Generate high-fidelity stills with aspect ratio controls.
- 💾 **Smart Auto-Download & Renaming**:
  - Automatically captures output files (`.mp4`, `.png`, `.jpg`, `.webp`).
  - Organizes downloads into custom designated subfolders (`meta-folder-1/`).
  - Automatically prefixes or indexes downloaded media based on prompt numbers.
- 🛡️ **Zero-Downtime Offline Resilience**:
  - Equipped with built-in fail-safe DOM selectors—works independently without relying on external config servers.
- 🌐 **Multi-Language Support**:
  - Native localization for English, Spanish (Español), Vietnamese (Tiếng Việt), Chinese (中文), Japanese (日本語), and Korean (한국어).
- 🎨 **Futuristic & Elegant UI**:
  - Integrated directly inside the modern Chrome Side Panel with a sleek **Electric Indigo** dark theme, real-time progress indicators, and actionable status logs.

---

## 📥 Quick Installation Guide

No build steps required! You can run the extension directly in any Chromium-based browser (Google Chrome, Microsoft Edge, Brave, Opera).

### Step 1: Download or Clone Repository
```bash
git clone https://github.com/abidalidevv/Meta-Automation-Auto-Meta-on-Meta.ai.git
```
*(Or click **Code > Download ZIP** and extract the folder to your computer).*

### Step 2: Load into Chrome
1. Open Google Chrome and navigate to:
   ```text
   chrome://extensions
   ```
2. Enable **Developer mode** using the toggle in the top-right corner.
3. Click the **Load unpacked** button in the top-left corner.
4. Select the downloaded/extracted project folder (`meta automation`).
5. The extension icon will now appear in your browser extensions toolbar! 🎉

---

## 🕹️ How to Use

1. **Log in to Meta AI**:
   Navigate to [https://www.meta.ai](https://www.meta.ai) in your browser and make sure you are logged into your account.
2. **Open the Side Panel**:
   Click the **Meta Automation** icon in your Chrome toolbar. The extension side panel will slide open right beside your Meta AI tab.
3. **Select Mode & Add Prompts**:
   - Choose your generation mode: *Text to Video*, *Image to Video*, or *Text to Image*.
   - Enter your prompt list (separate prompts with newlines or import via spreadsheet).
   - Configure batch size, duration, and aspect ratio (`16:9` widescreen or `9:16` vertical).
4. **Start Automation**:
   Click **Run Batch / Start**. The extension will automatically input prompts, trigger generation, monitor completion status, and download media files hands-free!

---

## ⚙️ Advanced Settings & Customization

Inside the **Settings** tab of the extension:
- **Concurrent Prompts**: Set how many prompts to process at once.
- **Random Delays**: Add randomized delays (e.g., 2–8 seconds) between prompts to mimic organic human activity.
- **Quality & Format**: Select output video quality (720p / HD) and image resolution (1k / 2k).
- **Auto-Retry**: Configure automatic retry attempts if Meta AI experiences server throttling or temporary failures.
- **Folder Routing**: Specify custom destination folders for downloaded files.

---

## 🏗️ Technical Architecture

- **Extension Framework**: Chrome Manifest V3
- **Core APIs**: `chrome.sidePanel`, `chrome.downloads`, `chrome.storage.local`, `chrome.tabs`
- **Frontend Stack**: Vue 3, PrimeVue UI Component Library, Tailwind CSS Utility Tokens
- **Icons**: PrimeIcons & Custom 3D Glossy AI Automation Emblem
- **Resilience Engine**: Built-in fallback selector dictionary ensuring persistent DOM automation across Meta.ai updates

---

## 👨‍💻 Author & Developer

Developed and maintained with ❤️ by **Abid Ali Dev**:

- 🌐 **Website**: [abidalidev.com](https://abidalidev.com)
- 💻 **GitHub**: [@abidalidevv](https://github.com/abidalidevv)
- 💼 **LinkedIn**: [in/abidalidev](https://linkedin.com/in/abidalidev)
- 🐦 **X (Twitter)**: [@abidalidevv](https://x.com/abidalidevv)
- 📸 **Instagram**: [@abidalidevv](https://www.instagram.com/abidalidevv)
- 📘 **Facebook**: [abidalidevv](https://www.facebook.com/abidalidevv)
- ☕ **Support / Ko-fi**: [ko-fi.com/abidalidev](https://ko-fi.com/abidalidev)
- 📍 **Location**: Punjab, Pakistan
- 📧 **Contact**: [abidmmp99@gmail.com](mailto:abidmmp99@gmail.com)

---

## 🤝 Contributing & Feedback

Contributions, feature suggestions, and issues are always welcome!
- Found a bug? Open an [Issue](https://github.com/abidalidevv/Meta-Automation-Auto-Meta-on-Meta.ai/issues) or send an email to `abidmmp99@gmail.com`.
- Have an idea? Submit a Pull Request.
- If you find this project helpful, please give it a **⭐ Star** on GitHub!

---

## ⚖️ License & Disclaimer

Distributed under the **MIT License**. See `LICENSE` for details.

*Disclaimer: This extension is an independent automation tool developed for research, productivity, and personal automation workflows. It is not affiliated with, endorsed by, or sponsored by Meta Platforms, Inc. or Meta.ai.*
