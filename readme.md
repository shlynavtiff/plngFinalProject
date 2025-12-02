# 🍽 Restaurant Management System - GitHub Guide

## 🚀 For Team Members (Read Carefully!)

### First Time Setup (Do This Once!)

1. **Clone the repository**
```bash
[git clone https://github.com/YOUR-USERNAME/restaurant-rms.git](https://github.com/shlynavtiff/plngFinalProject.git)
cd plngFinalProject
```

2. **Switch to YOUR assigned branch**
```bash
# Replace 'your-module-name' with your actual branch
git checkout your-module-name

# Examples:
# git checkout billing-and-payment
# git checkout menu-management
# git checkout user-management
# etc.........wasdasdawasd
```

---

## How to Commit Your Work

### Step 1: Make sure you're on YOUR branch
```bash
git branch  # Should show * next to YOUR branch name
```

### Step 2: Add your module file
```bash
# Add ONLY your file
git add your_module.py 
git add . 

# Example:
# git add user_management.py
# git add menu_management.py
# git add . (lalagay lahat ng changes sa buong branch)
```

### Step 3: Commit with a clear message
```bash
git commit -m "Add [your module name] - [what you did]"

# Examples:
# git commit -m "Add user management - login and registration"
# git commit -m "Add menu management - CRUD operations"
# git commit -m "wasdasddasasdasdas"
```

### Step 4: Push to YOUR branch
```bash
git push origin your-branch-name

# Examples:
# git push origin user-management
# git push origin menu-management
# kung mali naman ng branch, magbabato naman yan ng error
```

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
- **NEVER** force push (`git push -f`), wag, pls lang

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

## Quick Reference

```bash
# 1. Clone (first time only)
https://github.com/shlynavtiff/plngFinalProject.git

# 2. Go to your branch
git checkout your-branch-name
refer here
<img width="353" height="441" alt="image" src="https://github.com/user-attachments/assets/1d19589b-a065-4417-8cb6-77db91a86c9e" />


# 3. Do your work, then:
git add your_file.py or git add .
git commit -m "Your message here"
git push origin your-branch-name

```

---

## 💡 Testing Your Module

Before pushing, test your module:

```bash
python your_module.py
```

If it runs without errors, you're good to push!

---

**Questions?** Message the group chat or ask someone that can help with version control.
