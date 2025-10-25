# Todo List Tracker v1.03 🌟

A comprehensive task management application with **adorable chibi 3D avatar system** inspired by Animal Crossing GameCube! Built with Python and Tkinter.

**📱 NEW: Android version now available!** See [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md) for building and installing on Android devices.

## ✨ Key Features

### 🌟 Chibi 3D Avatar System (NEW!)
- **Real 3D claymation avatar** with Animal Crossing GameCube-style proportions
- **Interactive 3D camera** - drag mouse to rotate, scroll to zoom
- **Adorable chibi design** - oversized head, sparkling eyes, tiny body
- **3D pets** - chibi cats, dogs, birds, and dragons that follow you around
- **Smooth 3D animation** - breathing, movement, and pet interactions
- **Customizable in 3D** - hats, shirts, pants all properly sized for chibi proportions

### 📋 Advanced Task Management
- **Multiple view modes** - Tree, Kanban, List, and Compact views
- **AI task assistant** - conversational AI that helps generate tasks
- **Smart categorization** - automatic category and priority assignment
- **XP and leveling system** - earn points and unlock avatar items
- **Time tracking** - Pomodoro timer and task time tracking

### 🎨 Rich Customization
- **Multiple themes** - Light, Dark, Monokai, Sky Gradient, and more
- **Avatar customization** - unlock clothing and accessories as you level up
- **Pet collection** - unlock adorable chibi pets through completing tasks

## 🚀 Quick Start

### Desktop Version (Windows/Mac/Linux)

#### Installation

1. **Clone or download** this repository
2. **Install Python 3.7+** (if not already installed)
3. **Install optional dependencies** for enhanced 3D features:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: The app works without these - they just enable additional 3D avatar systems*

#### Launch the App

```bash
python todo_list_tracker.py
```

#### Experience Your Chibi Avatar

1. Navigate to **"🌟 CHIBI 3D AVATAR ROOM"** tab
2. Click **"🌟 Initialize Chibi 3D Avatar"**
3. **Drag mouse** to rotate camera around your adorable character
4. **Use arrow buttons** to move your avatar in 3D space
5. **Complete tasks** to earn XP and unlock new clothing and pets!

### 📱 Android Version

Want to use Todo List Tracker on your Android device? We've got you covered!

**See the complete guide:** [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md)

**Quick overview:**
1. Install Kivy and Buildozer on your Linux/Mac development machine
2. Run `buildozer android debug` to build the APK
3. Install on your Android device via USB or file transfer
4. Enjoy task management on the go!

The Android version includes:
- ✅ Core task management (add, complete, delete)
- ✅ Categories and priorities
- ✅ Task filtering (all, active, completed)
- ✅ Mobile-optimized touch interface
- ✅ Persistent data storage

*Note: The 3D avatar features are desktop-only to ensure optimal mobile performance.*

## 📁 Project Structure

```
todo_list_tracker/
│
├── todo_list_tracker.py      # Main desktop application file
├── todo_android.py           # Android/mobile version (Kivy)
├── avatar_fast_3d.py         # Fast 3D chibi avatar system (primary)
├── avatar_real_3d.py         # Matplotlib 3D avatar system
├── avatar_true_3d.py         # OpenGL 3D avatar system  
├── avatar_enhanced_2d.py     # Enhanced 2D fallback system
│
├── data/                     # Data directory (auto-created)
│   ├── tasks.json           # Your tasks and settings
│   └── todo_settings.json   # App preferences
│
├── README.md                 # This documentation
├── ANDROID_BUILD_GUIDE.md    # Android build instructions
├── CHANGELOG.md              # Version history
├── requirements.txt          # Desktop dependencies
├── requirements-android.txt  # Android build dependencies
├── buildozer.spec           # Android build configuration
└── VERSION.txt              # Current version
```

## 🎮 Avatar Systems

The app includes multiple 3D avatar systems with automatic fallback:

1. **Fast 3D** (Primary) - Optimized canvas 3D with 20 FPS smooth rendering
2. **Real 3D** - Matplotlib-based 3D with full mathematical accuracy  
3. **True 3D** - OpenGL-based system (requires system 3D support)
4. **Enhanced 2D** - Fallback system that still looks great

## Data Storage

- Tasks and theme preferences are automatically saved to `data/tasks.json`
- The data directory is created automatically if it doesn't exist
- You can manually save/load tasks to/from different locations using the Save/Load buttons

## Themes

Available themes:
- Light
- Dark
- Monokai
- Solarized Light
- Solarized Dark
- Nord
- GitHub Light
- GitHub Dark

Theme preferences are automatically saved when you close the application.