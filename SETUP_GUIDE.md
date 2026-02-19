# 📋 JobStream Pro - Complete Setup & Usage Guide

## 📂 Project Structure

```
adscrape/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .env                     # Your API keys (create from .env.example)
├── .streamlit/config.toml   # Streamlit configuration
├── README.md                # Full documentation
├── QUICKSTART.md            # 5-minute setup guide
├── MOBILE_GUIDE.md          # Phone deployment options
├── launch.bat               # Windows launcher (double-click to run)
├── launch.sh                # Mac/Linux launcher
├── setup.py                 # Setup helper script
├── pyproject.toml           # Project metadata
├── .gitignore               # Git ignore rules
└── keys/                    # API keys folder (optional)
```

---

## 🚀 Getting Started (Choose Your Method)

### Method 1: Quick Launch (Windows) ⭐ EASIEST
```
1. Double-click: launch.bat
2. Wait for browser to open
3. Done! Start searching for jobs
```

### Method 2: Quick Launch (Mac/Linux)
```bash
chmod +x launch.sh
./launch.sh
```

### Method 3: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your API key
# Copy .env.example to .env
# Add your Firecrawl API key

# 3. Run the app
streamlit run app.py
```

---

## 🔑 Get Firecrawl API Key (Free)

1. Go to: **https://firecrawl.dev**
2. Click "Get API Key"
3. Sign up with GitHub or Google (takes 30 seconds)
4. Copy your API key
5. Open `.env` file in project folder
6. Replace `your_api_key_here` with your actual key
7. Save and restart app

**That's it!** The app works without API key, but with it you get:
- Full job descriptions
- Company information
- Better filtering
- Salary ranges (when available)

---

## 💻 How to Use the App

### Upload CV Method (Recommended)
1. Click **"Upload your CV (PDF)"**
2. Select your resume file (PDF)
3. App automatically extracts skills
4. Click **"Find Matching Jobs"**
5. Review results
6. Click **"🚀 Apply Now"** to go directly to job posting
7. Apply directly on the job platform

### Quick Search Method
1. Type a job title in search box
2. Click **"Find Matching Jobs"**
3. Browse results
4. Apply directly!

### Customize Your Search
In the sidebar ⬅️ , adjust:
- **Job Types**: Remote, Full-time, Contract, etc.
- **Experience Level**: Entry, Mid, Senior, Lead
- **Job Filters**: Filter by platform or sort results

---

## 📱 Use on Your Phone

### Same WiFi Network (Fastest)
1. On laptop, run: `streamlit run app.py`
2. Get laptop's IP:
   ```powershell
   ipconfig          # Windows
   ifconfig          # Mac/Linux
   ```
   Look for `IPv4 Address` like `192.168.1.100`
3. On phone, open browser and visit:
   ```
   http://192.168.1.100:8501
   ```

### Different Network (Cloud)
1. Deploy to Streamlit Cloud (automatic scaling)
2. Get URL like: `https://yourusername-JobStream.streamlit.app`
3. Access from any phone with internet!

See **MOBILE_GUIDE.md** for detailed deployment options.

---

## 🎯 What Jobs You Can Find

The app searches across:
- **LinkedIn** (500M+ professionals)
- **Indeed** (250M+ users)
- **Glassdoor** (1M+ reviews + jobs)
- **AngelList** (startup jobs)
- **RemoteOK** (remote-focused)
- **Stack Overflow** (tech positions)
- Plus direct company career pages

---

## 🧠 Skills Detected

App recognizes **50+ technical skills**:

**Languages:** Python, Java, JavaScript, TypeScript, Go, Rust, C++, C#, Swift, Ruby, PHP, Kotlin, SQL, HTML, CSS, R, MATLAB

**Web Frameworks:** React, Angular, Vue, Django, Flask, FastAPI, Spring, Node.js, Express, Next.js, Laravel, ASP.NET

**Databases:** PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, DynamoDB, Cassandra, Oracle

**Cloud/DevOps:** AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Jenkins, GitLab, Terraform, Ansible

**AI/ML:** TensorFlow, PyTorch, NLP, Computer Vision, Deep Learning, Data Science, Pandas, NumPy

**Soft Skills:** Leadership, Management, Communication, Agile, Scrum, Sales, Marketing

---

## ⚙️ Configuration

### Environment Variables (.env)
```
FIRECRAWL_API_KEY=your_key_here  # Get from firecrawl.dev
```

### Streamlit Settings (.streamlit/config.toml)
- Theme colors customizable
- Upload size limit: 200MB
- Server port: 8501

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 8501 in use** | `streamlit run app.py --server.port=8502` |
| **PDF won't upload** | Convert to text-based PDF (not scanned image) |
| **No results found** | Check internet, API key, try different search |
| **Can't connect from phone** | Ensure both on same WiFi, verify IP address |
| **App runs slow** | API rate-limited, wait minute and retry |
| **ImportError for module** | Run: `pip install -r requirements.txt` again |

---

## 🌐 Deployment Options

### Free Options
1. **Streamlit Cloud** (easiest)
   - Push to GitHub
   - Connect at share.streamlit.io
   - Auto-deploys on push

2. **Local Network** (fastest)
   - Run on laptop
   - Access from phone on same WiFi

### Paid Options
1. **Railway** ($5/month, very easy)
2. **Heroku** ($7/month)
3. **Render** (free tier available)
4. **AWS/Azure** (pay-as-you-go)

---

## 📊 Example Workflow

```
1. Save your updated resume as PDF
2. Double-click launch.bat (Windows) or ./launch.sh (Mac/Linux)
3. App opens at http://localhost:8501
4. Click "Upload your CV"
5. Select your resume
6. Check detected skills
7. Click "Find Matching Jobs"
8. Browse results
9. Click "Apply Now" on interesting positions
10. Apply directly on job platform
11. Repeat with different searches if needed
```

**Time saved:** 2+ hours per job hunt session! 🎉

---

## 🔒 Privacy & Security

✅ **Your CV is safe:**
- Processed locally (not uploaded to server)
- No data stored on external servers
- No cookies or tracking
- Only API calls are to search engines

✅ **No personal data collection:**
- No login required
- No email verification needed
- No ads or analytics

---

## 📝 Tips for Better Results

1. **Resume Format**: Use clean, text-based PDFs (avoid scanned images)
2. **Keywords**: Include industry-specific keywords in resume
3. **Multiple Searches**: Try different job titles
4. **Filters**: Use sidebar filters to narrow down
5. **Save Tracking**: Copy URLs to spreadsheet for tracking applications
6. **Refresh**: Run search multiple times to see new postings
7. **Geographic**: Add location to search if relevant

---

## 🤝 Customization

### Add More Platforms
Edit `search_job_platforms()` in `app.py`:
```python
platforms = [
    "search query for new platform",
    # Add more here
]
```

### Modify Skill Detection
Edit `common_skills` dictionary to add custom skills:
```python
common_skills = {
    "Your Skill": "skill",
    # Add more
}
```

### Change Colors/Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#your_color"
```

---

## 📚 Resources

- **Firecrawl API**: https://firecrawl.dev/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **PyMuPDF (fitz)**: https://pymupdf.readthedocs.io
- **Python Docs**: https://docs.python.org

---

## 🆘 Getting Help

1. Check **README.md** (full documentation)
2. Check **QUICKSTART.md** (quick reference)
3. Check **MOBILE_GUIDE.md** (phone access)
4. Review **Troubleshooting** section above
5. Create GitHub issue

---

## 🎓 Learning Path

New to this? Here's what to learn:
1. **Running the app** (start here)
2. **Using the interface** (upload & search)
3. **Mobile access** (on phone)
4. **Cloud deployment** (always available)
5. **Customization** (advanced)

---

## 🏆 Success Tips

1. **Update resume regularly** - Keep it current
2. **Run multiple searches** - Try different titles
3. **Daily checks** - New jobs posted daily
4. **Track applications** - Spreadsheet helps
5. **Customize preferences** - Narrow down what you want
6. **Direct apply** - Faster than job boards
7. **Share with friends** - Help others find jobs!

---

## 📞 Support

- GitHub: [Your Repo URL]
- Email: support@JobStreampro.com
- Twitter: @JobStreamProApp
- Issues: [GitHub Issues]

---

## 🎉 You're All Set!

Your CV-based job discovery app is ready to use!

**Next Step:** Run `launch.bat` (Windows) or `./launch.sh` (Mac/Linux)

**Happy Job Hunting! 🚀**
