# 🚀 Quick Start Guide - JobHunter Pro

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Firecrawl API Key (FREE)
1. Visit: https://firecrawl.dev/
2. Sign up with GitHub/Google
3. Copy your API key
4. Open `.env` file and replace `your_api_key_here` with your key

### Step 3: Launch the App
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501` 🎉

---

## 📱 Use on Phone/Tablet

### Same Network (Recommended)
1. On your laptop: Go to terminal and run:
   ```bash
   # Windows: ipconfig
   # Mac/Linux: ifconfig
   ```
   Look for `IPv4 Address` (e.g., `192.168.1.100`)

2. On your phone, open browser and go to:
   ```
   http://192.168.1.100:8501
   ```

### Different Network
Deploy to Streamlit Cloud (see **Deployment** section below)

---

## 🎯 How to Use

### Method 1: Upload Your CV (Smart)
1. Click **"Upload your CV (PDF)"**
2. Select your resume
3. App extracts 50+ technical skills automatically
4. Click **"Find Matching Jobs"**
5. Browse results and apply directly!

### Method 2: Quick Search
1. Type a job title: "Full Stack Developer", "Data Scientist", etc.
2. Click **"Find Matching Jobs"**
3. Get results instantly!

### Customize Your Search
- **Job Type**: Full-time, Remote, Contract, etc.
- **Experience Level**: Entry, Mid, Senior, Lead
- **Platforms**: LinkedIn, Indeed, Glassdoor, etc.

---

## 🌐 Supported Platforms

| Platform | Jobs Added | Direct Link |
|----------|-----------|------------|
| LinkedIn | 50M+ | ✅ Yes |
| Indeed | 250M+ | ✅ Yes |
| Glassdoor | 1M+ | ✅ Yes |
| AngelList | 50K+ | ✅ Yes |
| RemoteOK | 5K+ | ✅ Yes |
| Stack Overflow | 10K+ | ✅ Yes |
| Lever | 100K+ | ✅ Yes |
| Greenhouse | 100K+ | ✅ Yes |

---

## 🔑 API Key Setup (Optional but Recommended)

**Without Firecrawl API:**
- ✅ Get job search links
- ✅ Works fine
- ❌ Limited details per job

**With Firecrawl API:**
- ✅ Full job descriptions
- ✅ Better filtering
- ✅ Company details
- ✅ Salary info (when available)

Get free API key: https://firecrawl.dev

---

## 📊 What the App Detects

The app recognizes **50+ skills** including:

**Languages:** Python, Java, JavaScript, C#, Go, Rust, Swift, etc.

**Web:** React, Vue, Angular, Django, FastAPI, Node.js, etc.

**Databases:** PostgreSQL, MongoDB, Redis, MySQL, etc.

**Cloud:** AWS, Azure, GCP, Docker, Kubernetes, etc.

**AI/ML:** TensorFlow, PyTorch, NLP, Computer Vision, etc.

---

## ⚙️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port already in use** | Kill process: `lsof -i :8501` then `kill -9 <PID>` |
| **PDF upload fails** | Convert to text-based PDF (not scanned image) |
| **No results** | Check API key, try different search term |
| **Slow loading** | API rate-limited, wait 1 min and retry |
| **Can't access from phone** | Check both devices on same WiFi, use correct IP |

---

## 🌍 Deploy to Cloud (Free)

### Streamlit Cloud
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "JobHunter Pro"
git push origin main

# 2. Go to share.streamlit.io
# 3. Connect GitHub repo
# 4. Set FIRECRAWL_API_KEY in secrets
# 5. Deploy!
```

**Your app URL:** `https://yourusername-jobhunter.streamlit.app`

### Share Link
1. Deploy to Streamlit Cloud (above)
2. Share link with others
3. Everyone can use your app!

---

## 📝 Tips & Tricks

✅ **Best Practices:**
- Use latest resume (updated within 6 months)
- Include industry keywords
- One focused search > many generic searches
- Save job links for tracking

✅ **Pro Tips:**
- Search multiple times with different roles
- Adjust experience level in sidebar
- Filter by remote/full-time as needed
- Copy results to spreadsheet for tracking

---

## 🔒 Privacy

- ✅ CV processed locally (not uploaded)
- ✅ No data stored on servers
- ✅ No cookies or tracking
- ✅ No account needed
- ✅ Direct links only

---

## 📞 Need Help?

- 📖 Check README.md for full docs
- 🐛 Report issues on GitHub
- 💬 Create a discussion
- 📧 Email: support@jobhunterpro.com

---

**Happy Job Hunting! 🎉**

