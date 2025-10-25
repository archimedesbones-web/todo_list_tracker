# Building Todo List Tracker for Android 📱

This guide shows you how to build and install the Android version of Todo List Tracker.

## Overview

The Android version is built using:
- **Kivy** - Cross-platform Python framework for mobile apps
- **Buildozer** - Tool that packages Python apps as Android APKs

## Features in Android Version

✅ **Core Task Management**
- Add, complete, and delete tasks
- Set task categories and priorities
- Filter tasks (All, Active, Completed)
- Persistent storage on device

✅ **Mobile-Optimized UI**
- Touch-friendly interface
- Responsive layout
- Material-style buttons
- Scrollable task list

📝 **Note:** The 3D avatar features from the desktop version are not included in the mobile version to ensure optimal performance on Android devices.

## Prerequisites

### For Building (Development Machine)

You need a **Linux** or **macOS** system (or WSL2 on Windows) with:

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **pip** (Python package installer)
   ```bash
   pip3 --version
   ```

3. **Java Development Kit (JDK) 8 or 11**
   ```bash
   java -version
   javac -version
   ```

4. **Git**
   ```bash
   git --version
   ```

5. **Build tools** (Linux/Ubuntu)
   ```bash
   sudo apt update
   sudo apt install -y python3-pip build-essential git python3-dev \
       libffi-dev libssl-dev zip unzip openjdk-11-jdk autoconf libtool \
       pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
       cmake libffi-dev libssl-dev
   ```

   **macOS:**
   ```bash
   brew install python3 git
   # Install Java from https://www.oracle.com/java/technologies/downloads/
   ```

### For Running (Android Device)

- Android device or emulator running **Android 5.0 (API 21)** or higher
- At least **50 MB** of free storage space

## Installation Steps

### Step 1: Install Python Dependencies

```bash
# Install Kivy and Buildozer
pip3 install -r requirements-android.txt

# Or install individually
pip3 install kivy buildozer cython
```

### Step 2: Initialize Buildozer (First Time Only)

The `buildozer.spec` file is already configured. To verify or customize:

```bash
# View the current configuration
cat buildozer.spec

# Edit if needed
nano buildozer.spec
```

Key settings in `buildozer.spec`:
- `title`: App name shown on device
- `package.name`: Internal package identifier
- `version`: App version number
- `requirements`: Python packages to include
- `android.permissions`: Required Android permissions
- `android.api`: Target Android API level

### Step 3: Build the APK

**Important:** The first build will take 20-40 minutes as it downloads the Android SDK, NDK, and compiles dependencies. Subsequent builds are much faster.

```bash
# Clean any previous builds (optional, recommended for first build)
buildozer android clean

# Build in debug mode (for testing)
buildozer android debug

# The APK will be created in: bin/todolisttracker-1.03-arm64-v8a-debug.apk
```

**For release builds** (requires signing):
```bash
buildozer android release
```

### Step 4: Install on Android Device

**Option 1: Via USB (ADB)**

1. Enable **Developer Options** on your Android device:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   
2. Enable **USB Debugging**:
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

3. Connect device via USB and install:
   ```bash
   # Install ADB if not present
   sudo apt install adb  # Linux
   brew install android-platform-tools  # macOS
   
   # Install the APK
   adb install -r bin/todolisttracker-1.03-arm64-v8a-debug.apk
   ```

**Option 2: Manual Transfer**

1. Copy the APK file from `bin/` to your device (via USB, email, cloud storage, etc.)
2. On your Android device, navigate to the APK file
3. Tap to install (you may need to enable "Install from Unknown Sources")

**Option 3: Direct Install from Buildozer**

```bash
buildozer android deploy run
```

This builds, installs, and runs the app in one command.

## Using the App

1. **Launch** the app from your Android home screen or app drawer
2. **Add tasks** using the text input and "➕ Add Task" button
3. **Set category and priority** using the dropdown spinners
4. **Mark complete** by tapping "✓ Done" on a task
5. **Delete tasks** by tapping "✕ Delete"
6. **Filter view** using All/Active/Completed buttons

## Troubleshooting

### Build Errors

**"Command failed: python3 -m pythonforandroid..."**
- Ensure all prerequisites are installed
- Try cleaning and rebuilding: `buildozer android clean`

**"Java not found" or JDK errors**
- Install JDK 8 or 11
- Set JAVA_HOME environment variable:
  ```bash
  export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
  ```

**"SDK/NDK download failed"**
- Check internet connection
- Buildozer will auto-download these (requires ~2 GB)
- Or manually specify paths in buildozer.spec

### Installation Errors

**"App not installed"**
- Ensure device has enough storage
- Check Android version (must be 5.0+)
- Enable "Unknown Sources" in device settings

**"Parse error"**
- APK may be corrupted - rebuild
- Ensure correct architecture (arm64-v8a or armeabi-v7a)

### Runtime Errors

**App crashes on launch**
- Check device logs: `adb logcat | grep python`
- Verify all required permissions are granted
- Ensure Android version compatibility

**Data not persisting**
- Check storage permissions
- App data is stored in private app directory
- Uninstalling app will delete all tasks

## Building for Different Architectures

```bash
# For 64-bit ARM (most modern devices)
buildozer android debug

# For 32-bit ARM (older devices)
# Edit buildozer.spec and change android.archs to armeabi-v7a
nano buildozer.spec
# Then rebuild
buildozer android debug
```

## Customization

### Changing App Icon

1. Create icon images:
   - `icon.png` - 512x512 pixels
   - Or specify in buildozer.spec: `icon.filename = path/to/icon.png`

2. Rebuild the app

### Changing App Name

Edit `buildozer.spec`:
```ini
title = Your Custom Name
```

### Adding More Features

Edit `todo_android.py` to add new functionality, then rebuild.

## Development Workflow

```bash
# 1. Make changes to todo_android.py
nano todo_android.py

# 2. Test locally with Kivy (faster than full rebuild)
python3 todo_android.py

# 3. Build and deploy to device
buildozer android debug deploy run

# 4. View logs while running
adb logcat | grep python
```

## Performance Tips

- First build: ~20-40 minutes (downloads SDK, NDK, compiles)
- Incremental builds: ~2-5 minutes
- Use `buildozer android debug` for testing
- Use `buildozer android release` for distribution (smaller file size)

## File Locations

- **Source code:** `todo_android.py`
- **Build config:** `buildozer.spec`
- **Built APK:** `bin/todolisttracker-*.apk`
- **Build cache:** `.buildozer/` (can be deleted to save space)
- **App data on device:** `/data/data/org.todotracker.todolisttracker/`

## Distribution

To share your APK:

1. Build a release version:
   ```bash
   buildozer android release
   ```

2. Sign the APK (required for Google Play):
   - Use Android Studio or jarsigner
   - Or configure signing in buildozer.spec

3. Share the APK file from `bin/` directory

## Additional Resources

- **Kivy Documentation:** https://kivy.org/doc/stable/
- **Buildozer Documentation:** https://buildozer.readthedocs.io/
- **Python for Android:** https://python-for-android.readthedocs.io/

## Support

For issues specific to:
- **Building:** Check Buildozer and Python-for-Android docs
- **UI/Features:** Modify `todo_android.py`
- **Android compatibility:** Update `android.api` and `android.minapi` in buildozer.spec

---

**Happy Android Development! 📱✨**
