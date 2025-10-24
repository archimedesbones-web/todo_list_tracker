# Changelog - Todo List Tracker

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
