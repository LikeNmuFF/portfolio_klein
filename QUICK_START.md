# ⚡ Quick Start Guide (5 Minutes)

## What You Just Got

A complete Flask portfolio website with:
- Real ratings system with email masking
- GitHub stats integration
- 30+ project showcase
- 3 certificates display
- CV viewer + PDF download
- Beautiful dark mode design
- Fully responsive

## Installation (2 minutes)

```bash
# Navigate to portfolio directory
cd /mnt/c/Users/Hp/Documents/porfolio

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR: venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Get It Running (1 minute)

```bash
# Run the Flask app
python3 app.py

# Open browser to:
http://localhost:5000
```

**That's it! Your portfolio is running!** 🎉

## Add Your Stuff (2 minutes)

### 1. Profile Image
```bash
# Add your photo as:
static/images/profile.jpg
```

### 2. Your Projects
Edit `data/projects.json` and add:
```json
{
  "id": 1,
  "title": "My Project",
  "description": "What it does",
  "image": "projects/project-1.jpg",
  "tech": ["React", "Flask"],
  "github_link": "https://github.com/klyjj/project",
  "live_link": "https://example.com",
  "featured": true
}
```

### 3. Your Certificates
Edit `data/certificates.json` and add similar entries

### 4. Your CV
Save your CV as `static/downloads/cv.pdf`

## Next Steps

1. Read `IMPLEMENTATION_GUIDE.md` for detailed setup
2. Read `CHECKLIST.md` for testing & tasks
3. Customize colors in `static/css/style.css`
4. Add all 30+ projects and images
5. Share and get ratings! 

## Test It Works

- [ ] Home page loads
- [ ] Can submit a rating
- [ ] GitHub stats show
- [ ] Projects page works
- [ ] Certificates page works
- [ ] CV page works
- [ ] PDF downloads
- [ ] Works on mobile

## Troubleshooting

**Port already in use?**
```bash
# Edit app.py last line:
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

**Images not showing?**
- Check files are in `static/images/`
- Use relative paths in JSON: `projects/project-1.jpg`

**Database error?**
```bash
rm portfolio.db
python3 app.py  # Recreates it
```

**Virtual env issues?**
```bash
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app |
| `data/projects.json` | Your 30+ projects |
| `data/certificates.json` | Your 3 certificates |
| `static/images/profile.jpg` | Your profile photo |
| `static/css/style.css` | All styling |
| `static/downloads/cv.pdf` | Your CV file |

## Features You Have

✨ **Real Ratings** - Users can rate your work  
✨ **GitHub Integration** - Shows your live stats  
✨ **Projects Showcase** - Display 30+ projects  
✨ **Certificates** - Show 3 professional certs  
✨ **CV/Resume** - View in browser, download PDF  
✨ **Email Masking** - Protects user privacy  
✨ **Responsive** - Works on all devices  
✨ **Beautiful Design** - Dark mode with animations  

## Need More Help?

1. `README.md` - Full documentation
2. `IMPLEMENTATION_GUIDE.md` - Step-by-step
3. `CHECKLIST.md` - Tasks & testing

---

**Your portfolio is ready to go! 🚀**

Start with: `python3 app.py`
