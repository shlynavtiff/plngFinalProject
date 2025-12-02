# 🍽 Restaurant Management System - GitHub Guide

## 🚀 For Team Members (Read Carefully!)

### First Time Setup (Do This Once!)

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/restaurant-rms.git
cd restaurant-rms
```

2. **Switch to YOUR assigned branch**
```bash
# Replace 'your-module-name' with your actual branch
git checkout your-module-name

# Examples:
# git checkout user-management
# git checkout menu-management
# git checkout billing-module
```

---

## 📝 How to Submit Your Work

### Step 1: Make sure you're on YOUR branch
```bash
git branch  # Should show * next to YOUR branch name
```

### Step 2: Add your module file
```bash
# Add ONLY your file
git add your_module.py

# Example:
# git add user_management.py
# git add menu_management.py
```

### Step 3: Commit with a clear message
```bash
git commit -m "Add [your module name] - [what you did]"

# Examples:
# git commit -m "Add user management - login and registration"
# git commit -m "Add menu management - CRUD operations"
```

### Step 4: Push to YOUR branch
```bash
git push origin your-branch-name

# Examples:
# git push origin user-management
# git push origin menu-management
```

### Step 5: Create a Pull Request (on GitHub website)
1. Go to the repository on GitHub
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select: `base: main` ← `compare: your-branch-name`
5. Click "Create pull request"
6. Add description of what you did
7. Assign the project leader as reviewer
8. Click "Create pull request"

---

## IMPORTANT RULES

### DO:
- Work ONLY on YOUR assigned branch
- Push ONLY your module file
- Test your code before pushing
- Ask for help if stuck!

### DON'T:
- **NEVER** work on the `main` branch
- **NEVER** touch other people's files
- **NEVER** merge anything yourself
- **NEVER** force push (`git push -f`)

---

## Common Problems & Solutions

### Problem: "I'm on the wrong branch!"
```bash
# Check what branch you're on
git branch

# Switch to your correct branch
git checkout your-branch-name
```

### Problem: "I accidentally changed someone else's file!"
```bash
# Undo changes to specific file
git checkout -- filename.py

# Or reset everything
git reset --hard
```

### Problem: "Git says I need to pull first"
```bash
# Pull the latest changes
git pull origin your-branch-name

# Then try pushing again
git push origin your-branch-name
```

### Problem: "I messed up everything!"
```bash
# Don't panic! Delete local copy and re-clone
cd ..
rm -rf restaurant-rms
git clone https://github.com/YOUR-USERNAME/restaurant-rms.git
cd restaurant-rms
git checkout your-branch-name
```

---

## Module Assignments

| Name | Branch | File |
|------|--------|------|
| Person 1 | `ordering-module` | `ordering_module.py` |
| Person 2 | `user-management` | `user_management.py` |
| Person 3 | `menu-management` | `menu_management.py` |
| Person 4 | `billing-module` | `billing_module.py` |
| Person 5 | `inventory-module` | `inventory_module.py` |
| Person 6 | `reports-module` | `reports_module.py` |

---

## Quick Reference

```bash
# 1. Clone (first time only)
git clone https://github.com/YOUR-USERNAME/restaurant-rms.git

# 2. Go to your branch
git checkout your-branch-name

# 3. Do your work, then:
git add your_file.py
git commit -m "Your message here"
git push origin your-branch-name

# 4. Create Pull Request on GitHub website
```

---

## 💡 Testing Your Module

Before pushing, test your module:

```bash
python your_module.py
```

If it runs without errors, you're good to push!

---

**Questions?** Message the group chat or ask the project leader.