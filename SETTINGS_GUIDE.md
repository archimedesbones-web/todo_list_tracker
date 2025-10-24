# Settings & AI Task Categorization Guide

## 🆕 New Settings Tab

Access via the **Settings** tab in the notebook to customize AI task behavior.

---

## ⚙️ AI Task Settings

### 1. **Add '#' prefix to AI-generated tasks**
- **Default:** ON (enabled)
- **When enabled:** All AI-generated tasks start with `#`
  - Example: `# Schedule workout times in calendar`
- **When disabled:** Tasks added without prefix
  - Example: `Schedule workout times in calendar`

**Purpose:** Easily identify which tasks came from AI suggestions vs. manually entered.

---

### 2. **Automatically categorize AI tasks**
- **Default:** ON (enabled)
- **When enabled:** AI tasks are placed in relevant categories based on content
- **When disabled:** All AI tasks go into "AI Generated" category

---

## 📁 Smart Categories

When "Automatically categorize AI tasks" is enabled, tasks are intelligently sorted:

### Category Detection Rules:

| Category | Keywords Detected | Context |
|----------|------------------|---------|
| **Fitness** | workout, exercise, gym, health, run, cardio, yoga, diet, meal, sleep | Fitness conversations |
| **Learning** | learn, study, course, practice, read, book, programming, python, skill | Learning conversations |
| **Work** | project, meeting, report, deadline, email, interview, career, business | Work-related tasks |
| **Writing** | write, blog, article, draft, edit, publish, content, story | Writing conversations |
| **Home** | organize, clean, tidy, groceries, shopping, laundry, maintenance | Home/organization tasks |
| **Personal** | goal, habit, routine, meditate, journal, mindfulness, growth | Personal development |
| **Finance** | budget, money, bill, tax, savings, investment, expense | Financial tasks |

**Note:** The AI also uses conversation context - if you're discussing fitness, related tasks automatically go to "Fitness" category.

---

## 📋 Example: Fitness Conversation

**You:** "I want to start a fitness routine"

**AI generates tasks:**
```
- Schedule workout times in calendar
- Start with 20-30 min sessions, 3x per week
- Track workouts in a journal or app
```

**With smart categories enabled:**
- ✅ `# Schedule workout times in calendar` → **Fitness** category
- ✅ `# Start with 20-30 min sessions, 3x per week` → **Fitness** category
- ✅ `# Track workouts in a journal or app` → **Fitness** category

**With smart categories disabled:**
- All tasks → **AI Generated** category

---

## 🎯 Task Confirmation Format

When you add an AI task, the confirmation shows:

```
✅ Added task: # Schedule workout times in calendar
   📁 Fitness | 🔴 High | 📅 2025-10-26
```

Shows:
- Task name (with # if enabled)
- Category assignment
- Priority level (🔴 High / 🟡 Medium / 🟢 Low)
- Deadline date

---

## 💾 Settings Persistence

- Settings are automatically saved to `todo_settings.json`
- Click **"Save Settings"** button to confirm changes
- Settings persist between app sessions

---

## 🔄 Changing Settings

1. Go to **Settings** tab
2. Toggle checkboxes on/off
3. Click **"Save Settings"** button
4. New tasks will use updated settings immediately

**Note:** Changing settings doesn't affect existing tasks - only new tasks added after the change.

---

## 📊 Benefits

### With # Prefix:
- ✅ Instantly recognize AI-suggested tasks
- ✅ Distinguish from manually entered tasks
- ✅ Easy to search/filter AI tasks

### With Smart Categories:
- ✅ Better organization
- ✅ Tasks grouped with related items
- ✅ Easier to find fitness, learning, or work tasks
- ✅ More meaningful task lists

### Without Features (when disabled):
- All AI tasks go to "AI Generated" category
- No visual distinction from manual tasks
- Still get intelligent priority and deadline assignment

---

## 🎨 Customization Examples

### Scenario 1: Minimalist (clean look)
- ❌ Disable "# prefix"
- ✅ Enable "Smart categories"
- **Result:** Clean task names, organized by topic

### Scenario 2: AI Tracking (identify AI tasks)
- ✅ Enable "# prefix"
- ❌ Disable "Smart categories"
- **Result:** All AI tasks marked with #, grouped in one category

### Scenario 3: Full Intelligence (recommended)
- ✅ Enable "# prefix"
- ✅ Enable "Smart categories"
- **Result:** AI tasks marked AND organized by topic (default)

---

Enjoy your personalized task management! 🚀
