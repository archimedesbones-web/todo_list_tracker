# Quick Start - Android Version

## For Users (Just want to use the app)

### Option 1: Download Pre-built APK (Easiest)
If someone has already built the APK:
1. Download `todolisttracker-*.apk` to your Android device
2. Enable "Install from Unknown Sources" in Android settings
3. Tap the APK file to install
4. Launch "Todo List Tracker" from your app drawer

### Option 2: Build It Yourself

**Requirements:**
- Linux or macOS computer (or WSL2 on Windows)
- Python 3.8+
- ~2 GB of free disk space (for Android SDK/NDK)

**Quick Build:**
```bash
# 1. Install build tools
pip3 install kivy buildozer cython

# 2. Navigate to the project directory
cd todo_list_tracker

# 3. Build the APK (first build takes 20-40 min)
buildozer android debug

# 4. Find your APK in the bin/ directory
ls bin/*.apk
```

**Install on Device:**
```bash
# Via USB (with ADB)
adb install -r bin/todolisttracker-*.apk

# Or manually transfer the APK file to your device and tap to install
```

## For Developers

See [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) for:
- Detailed prerequisites
- Customization options
- Troubleshooting
- Development workflow
- Building for different architectures

## Features

✅ Add, complete, and delete tasks  
✅ Organize by category (General, Work, Personal, etc.)  
✅ Set priority levels (Low, Medium, High, Urgent)  
✅ Filter view (All, Active, Completed)  
✅ Data persists in private app storage (no permissions needed)
✅ Touch-optimized interface  

## App Permissions

- **None required:** App uses private internal storage

## Support

- **Build issues:** Check [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) troubleshooting section
- **App issues:** Report in the main repository

---

**Start Managing Tasks on Android! 📱**
