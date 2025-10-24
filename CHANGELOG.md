# Changelog - Todo List Tracker

## Version 1.03 (2025-10-24)

### 🌟 Major New Features - Chibi 3D Avatar System

#### **True 3D Claymation Avatar**
- **Real 3D Rendering**: Actual 3D mathematics with proper perspective projection and depth sorting
- **Animal Crossing GameCube Style**: Adorable chibi proportions with oversized head and tiny body
- **Multiple 3D Systems**: Fast Canvas 3D (primary), Matplotlib 3D, OpenGL 3D (fallback systems)
- **Interactive 3D Camera**: Mouse drag to rotate, scroll to zoom, full 360° viewing
- **3D Movement**: Move avatar in X, Y, Z directions with intuitive controls

#### **Chibi Character Design**
- **Oversized Round Head**: Big cute head just like Animal Crossing characters
- **Large Sparkling Eyes**: Big eyes with white highlights for maximum cuteness
- **Tiny Proportional Body**: Small torso, stubby arms, short legs - perfect chibi style
- **Round Feet**: Spherical feet instead of rectangular for added adorableness
- **Breathing Animation**: Subtle 3D breathing animation in real-time

#### **3D Pets System**
- **Chibi Pet Companions**: All pets redesigned in matching chibi style
  - **Chibi Cat**: Round body with triangle ears and tiny sparkling eyes
  - **Chibi Dog**: Floppy ears, cute nose, loyal companion
  - **Chibi Bird**: Tiny wings, little beak, perches adorably
  - **Chibi Dragon**: Majestic but cute with tiny horns and wings
- **3D Pet Animation**: Pets bob and move around the 3D environment
- **Smart Pet Positioning**: Pets positioned around avatar in 3D space

#### **Advanced 3D Features**
- **Fast Rendering**: Optimized 3D engine running at 20 FPS for smooth experience
- **Depth Sorting**: Proper 3D object rendering with correct depth layering
- **3D Floor Grid**: Realistic floor with perspective and depth
- **Clothing in 3D**: All clothing items properly scaled and positioned for 3D
- **Hat System**: 3D hats sized appropriately for the oversized chibi head

### 🎨 Enhanced Avatar Room
- **"🌟 CHIBI 3D AVATAR ROOM"**: Updated tab title reflecting new style
- **Optimized Camera**: Positioned perfectly to frame the adorable chibi character
- **Intuitive Controls**: Natural camera and movement controls
- **Performance Optimized**: Smooth real-time 3D without lag

### 🔧 Technical Improvements
- **Multiple Avatar Systems**: Graceful fallback from Fast 3D → Real 3D → Enhanced 2D → Basic 2D
- **Dependency Management**: Updated requirements with optional 3D libraries
- **Cross-Platform**: Works on systems with or without advanced 3D libraries
- **Error Handling**: Robust system handles missing 3D dependencies gracefully

### 🎮 User Experience
- **Instant Gratification**: Quick initialization of chibi avatar
- **Drag and Play**: Intuitive mouse controls for 3D camera
- **Customization**: All existing customization works with new 3D system
- **Nostalgia Factor**: Authentic Animal Crossing GameCube feel and charm

---

## Version 1.025 (2025-10-23)

### 🆕 New Features
- Avatar Room tab with a virtual room scene and a customizable avatar (hats, shirts, pants)
- Movement controls with arrow keys and boundary collision
- XP System: earn 10 XP per task; Level = 1 + floor(XP/100); stats persist
- XP UI shown in Avatar Room: level, tasks completed, and XP progress bar
- Unlocks tied to levels (cosmetics and pets):
  - L2: Wizard Hat, Pet Cat
  - L3: Leather Jacket
  - L4: Camo Pants
  - L5: Sombrero, Pet Dog
  - L7: Tuxedo
  - L8: Pet Bird
  - L10: Viking Helmet, Rainbow Pants
  - L12: Superhero Shirt
  - L15: Pet Dragon, Halo
  - L20: Gold Shirt, Gold Pants
- Pets system with simple animations (Cat, Dog, Bird, Dragon)
- Pets UI in Avatar Room: starter pets (Cat, Dog) available from level 1; unlockable pets labeled (Locked)

### 🎨 Enhancements
- Theme application extended to Avatar Room, including Checkbuttons styling
- Clothing UI disables locked items and shows (Locked) labels until unlocked

### 🐛 Fixes
- Replaced invalid hex alpha color in Tk with solid gray for avatar shadow
- Fixed toggle_complete loop structure and integrated XP awarding

---

## Version 1.02 (2025-10-23)

### 🆕 New Features
- **Multiple View Modes** for Tasks tab
  - Tree View (hierarchical categories)
  - Kanban Board (To Do | In Progress | Done)
  - List View (flat list of all tasks)
  - Compact View (focus mode - high priority only)

- **AI Tasks Tab** with conversational assistant
  - Natural conversation flow with context awareness
  - Handles "I don't know" responses with guiding questions
  - Smart task generation from dialogue
  - Quick Start prompts for common scenarios
  - Immediate task suggestions with one-click add

- **Intelligent AI Features**
  - Smart priority assignment (High/Medium/Low based on content)
  - Smart deadline calculation (0-30 days based on task type)
  - Smart categorization (Fitness, Learning, Work, Writing, Home, Personal, Finance)
  - Optional '#' prefix for AI-generated tasks

- **Settings Tab**
  - Toggle AI task prefix (#)
  - Toggle smart categorization
  - Persistent settings across sessions

- **Daily Tab Enhancements**
  - Stopwatch and Pomodoro timer modes
  - Task time tracking (per-task accumulated time)
  - Running indicator in tab title
  - Category and priority filters for next task
  - Completed Today list
  - Auto-start next task after completion
  - Sound notifications for Pomodoro phases

### 🎨 Enhanced Features
- **Theme System**
  - Gradient support for backgrounds
  - Categorized color settings
  - One-click HSV color picker
  - Built-in "Sky Gradient" theme

- **View Synchronization**
  - All views stay synced with task changes
  - Add/remove/toggle operations refresh active view

### 🐛 Bug Fixes
- Removed duplicate imports
- Fixed settings file path consistency
- Fixed view refresh after task operations
- Cleaned up initialization code

### 📦 Data Management
- Settings saved to `data/todo_settings.json`
- Tasks saved to `data/tasks.json`
- All data organized in DATA_DIR

### 💡 Improvements
- Better file organization
- Consistent data directory usage
- Improved code structure
- Enhanced error handling

---

## Version 1.01 (Previous)
- Basic task management
- Categories and priorities
- Stats and calendar views
- Theme customization
- Daily tab with timer

---

## Version 1.00 (Initial Release)
- Core task management functionality
- Category organization
- Priority levels
- Deadline tracking
- Basic themes
