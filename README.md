# Klein Ric Abong - Portfolio Website

A professional Flask-based portfolio website featuring real ratings, 30+ projects showcase, certificates, and downloadable CV.

## Features

✨ **Key Features:**
- **Real Ratings System**: Submit and display client ratings with email masking for privacy
- **GitHub Integration**: Live stats showing followers, stars, and repositories
- **Projects Gallery**: Showcase 30+ projects with images, descriptions, and tech stacks
- **Certificates Display**: Show 3 professional certifications
- **CV Generation**: Browse CV in-browser and download as PDF
- **Floating Ratings Panel**: Beautiful side panel showing real-time ratings and GitHub stats
- **Fully Responsive**: Works beautifully on all devices
- **Modern Design**: Dark mode aesthetic with smooth animations

## Quick Start

### 1. Installation

```bash
# Clone/navigate to the project directory
cd /mnt/c/Users/Hp/Documents/porfolio

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit your information in the files:
- `app.py` - Update GitHub username (currently 'klyjj')
- `data/projects.json` - Add your 30+ projects
- `data/certificates.json` - Add your 3 certificates
- `templates/cv.html` - Update your contact information

### 3. Add Your Images

Create these folders and add your images:

```
static/images/
├── profile.jpg              # Your profile photo (used in hero section)
├── projects/
│   ├── project-1.jpg        # Project 1 image
│   ├── project-2.jpg        # Project 2 image
│   └── ... (up to project-30+)
└── certificates/
    ├── cert-1.jpg           # Certificate 1
    ├── cert-2.jpg           # Certificate 2
    └── cert-3.jpg           # Certificate 3
```

### 4. Add Your CV

Place your CV PDF in:
```
static/downloads/cv.pdf
```

### 5. Run the Application

```bash
python app.py
```

The app will be available at: `http://localhost:5000`

## Configuration Guide

### Adding Projects

Edit `data/projects.json` and add entries:

```json
{
  "id": 1,
  "title": "Project Name",
  "description": "What this project does",
  "image": "projects/project-1.jpg",
  "tech": ["React", "Flask", "Tailwind"],
  "github_link": "https://github.com/klyjj/project-name",
  "live_link": "https://live-demo-url.com",
  "featured": true
}
```

### Adding Certificates

Edit `data/certificates.json`:

```json
{
  "id": 1,
  "name": "Certificate Name",
  "organization": "Issuing Organization",
  "date_received": "2024-01-15",
  "image_path": "certificates/cert-1.jpg",
  "certificate_url": "https://certificate-link.com"
}
```

## Email Masking

When users submit ratings, their emails are automatically masked:
- `john.doe@gmail.com` → `jo***@gm***.com`

This protects user privacy while still showing legitimate feedback.

## Database

The app uses SQLite (automatically created on first run).

### Tables:
- **ratings**: Stores client ratings and reviews
- **projects**: Project metadata (auto-loaded from JSON)
- **certificates**: Certificate information (auto-loaded from JSON)

## API Endpoints

### Rating Submission
```
POST /api/submit-rating
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "rating": 5,
  "review": "Great work!"
}
```

### Get All Ratings
```
GET /api/ratings
```

## Pages

- `/` - Home page with hero, ratings panel, about, services, contact
- `/projects` - Projects gallery (30+ projects)
- `/certificates` - Certificates display
- `/cv` - CV view with PDF download
- `/download-cv` - Direct PDF download

## Customization

### Update Your Info
Edit `templates/index.html`:
- Change "Klein Ric Abong" to your name
- Update contact links (GitHub, Fiverr, etc.)
- Modify skill categories and descriptions

### Styling
All CSS is in `static/css/style.css`. The design uses CSS variables for easy theme customization:
- `--bg`, `--bg2`, `--bg3`: Background colors
- `--accent`, `--accent2`, `--accent3`: Accent colors
- `--text`, `--muted`: Text colors

### GitHub Integration
The app automatically fetches your GitHub stats. Update the username in `app.py`:

```python
@lru_cache(maxsize=1)
def get_github_stats(username='klyjj'):  # Change 'klyjj' to your username
```

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn app:app
```

### Environment Variables
Create a `.env` file for sensitive data:
```
SECRET_KEY=your-secret-key-here
GITHUB_USERNAME=klyjj
```

## Project Structure

```
porfolio/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── portfolio.db               # SQLite database (created on first run)
├── templates/
│   ├── base.html              # Base layout
│   ├── index.html             # Home page
│   ├── projects.html          # Projects page
│   ├── certificates.html      # Certificates page
│   ├── cv.html                # CV page
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
├── static/
│   ├── css/
│   │   └── style.css          # All styling
│   ├── js/
│   │   └── main.js            # JavaScript logic
│   ├── images/
│   │   ├── profile.jpg        # Your profile image
│   │   ├── projects/          # Project images
│   │   └── certificates/      # Certificate images
│   └── downloads/
│       └── cv.pdf             # Your CV file
└── data/
    ├── projects.json          # Project configuration
    └── certificates.json      # Certificate configuration
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Images Not Loading
- Ensure images are in the correct folder: `static/images/`
- Use relative paths in JSON configs: `projects/project-1.jpg`

### GitHub Stats Not Showing
- Check your GitHub username is correct
- Ensure you have an internet connection
- The API has rate limits (60 requests/hour unauthenticated)

### Database Issues
- Delete `portfolio.db` to reset the database
- Ratings will be lost, but projects/certificates are loaded from JSON

## Ratings System

Users can submit ratings directly from the home page. The system:
1. Validates all inputs
2. Masks the email address
3. Stores in SQLite database
4. Displays on the floating ratings panel
5. Shows average rating and count

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Add your profile image to `static/images/profile.jpg`
3. ✅ Edit `data/projects.json` with your projects
4. ✅ Edit `data/certificates.json` with your certificates
5. ✅ Add project and certificate images
6. ✅ Add your CV to `static/downloads/cv.pdf`
7. ✅ Update contact info in templates
8. ✅ Run: `python app.py`

## Support

For questions or issues:
- Check the code comments in `app.py`
- Review Flask documentation: https://flask.palletsprojects.com/
- Visit your GitHub profile: https://github.com/klyjj

## License

This portfolio is your personal project. Customize it as needed!

---

**Built with ♥ for Klein Ric Abong**
