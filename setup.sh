#!/bin/bash

echo "🚀 Setting up your Flask Portfolio..."
echo ""

# Check Python
echo "✓ Checking Python installation..."
python3 --version

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: python3 app.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "📝 Don't forget to:"
echo "   - Add your profile image to static/images/profile.jpg"
echo "   - Edit data/projects.json with your projects"
echo "   - Edit data/certificates.json with your certificates"
echo "   - Add project and certificate images"
echo "   - Add your CV to static/downloads/cv.pdf"
