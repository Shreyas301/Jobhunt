# 🚀 JobStream Pro - CV-Based Job Discovery App

An intelligent cross-platform (web & mobile) job discovery application that analyzes your CV and finds relevant job opportunities across multiple platforms with direct application links.

## 🎯 Features

✅ **intelligent CV Parsing**: Automatically extract skills from your resume  
✅ **Multi-Platform Search**: Searches LinkedIn, Indeed, Glassdoor, AngelList, and more  
✅ **Direct Job Links**: Get direct links to apply without intermediaries  
✅ **Mobile & Desktop Responsive**: Works seamlessly on laptops, tablets, and phones  
✅ **Smart Filtering**: Filter by job type, experience level, and platform  
✅ **Zero Sign-ups**: No need to create accounts on multiple job sites  

## 🛠️ Setup Instructions

### 1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Get Firecrawl API Key** (Optional but Recommended)

- Visit [firecrawl.dev](https://firecrawl.dev)
- Sign up for a free account
- Copy your API key
- Create a `.env` file (copy from `.env.example`):

```bash
FIRECRAWL_API_KEY=your_api_key_here
```

### 3. **Run the App**

```bash
streamlit run app.py
```

Your app will open at `http://localhost:8501`

### 4. **Access on Phone (Mobile)**

To access the app from your phone:

- Get your laptop's IP address:
  ```bash
  # Windows PowerShell
  ipconfig  # Look for IPv4 Address
  
  # macOS/Linux
  ifconfig  # Look for inet address
  ```

- On your phone, navigate to: `http://<YOUR_IP>:8501`
  
- Example: `http://192.168.1.100:8501`

## 📱 Usage

### Option 1: Upload CV (Recommended)
1. Click "Upload your CV (PDF)" 
2. Select your resume file
3. App automatically extracts your skills
4. Click "Find Matching Jobs"
5. Browse and apply directly!

### Option 2: Quick Search
1. Enter a job title in the search box
2. Click "Find Matching Jobs"
3. Results appear instantly

## 🌐 Supported Job Platforms

- **LinkedIn** - 500+ million professionals
- **Indeed** - 250+ million users
- **Glassdoor** - Company reviews + jobs
- **AngelList (Wellfound)** - Startup jobs
- **RemoteOK** - Remote work focus
- **Stack Overflow** - Tech jobs
- **Lever** - Company career pages
- **Greenhouse** - Company career pages

## 🎨 Customization

### Filter Jobs by:
- **Job Type**: Full-time, Part-time, Contract, Remote, Freelance
- **Experience Level**: Entry-level, Mid-level, Senior, Lead
- **Platform**: LinkedIn, Indeed, Glassdoor, etc.

### Detected Skills
The app recognizes 50+ skills including:
- Programming: Python, Java, JavaScript, Go, Rust, C++, etc.
- Frameworks: React, Django, Spring, Next.js, etc.
- Databases: PostgreSQL, MongoDB, Redis, etc.
- Cloud: AWS, Azure, GCP, Docker, Kubernetes
- AI/ML: TensorFlow, PyTorch, Pandas, NLP, etc.
- Soft Skills: Leadership, Management, Communication, etc.

## 🔒 Privacy & Security

- ✅ Your CV is processed locally (not stored on servers)
- ✅ No account creation required
- ✅ No personal data collection
- ✅ Direct links only (no tracking)

## 🚀 Deployment

### Deploy to Streamlit Cloud (FREE)

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select your repository
4. Set environment variables (FIRECRAWL_API_KEY)
5. Deploy!

Your app will be live at: `https://your-username-JobStream.streamlit.app`

### Deploy to Mobile

**Option A: Streamlit App (Simple)**
- Just use the web version on your phone
- Responsive design works great on mobile

**Option B: Build Native App (Advanced)**
- Use React Native + Streamlit backend
- Or use Flutter with Python backend via APIs

## 📊 How It Works

```
1. Upload CV (PDF)
   ↓
2. Extract Text & Parse Skills
   ↓
3. Generate Targeted Queries
   ↓
4. Search Job Platforms (Firecrawl API)
   ↓
5. Display Results with Direct Links
   ↓
6. Apply Directly (1-Click)
```

## ❓ Troubleshooting

### Issue: "Missing Firecrawl API Key"
**Solution**: 
- Get a free key at [firecrawl.dev](https://firecrawl.dev)
- Add to `.env` file
- Restart the app

### Issue: PDF upload fails
**Solution**: 
- Ensure PDF is valid and not corrupted
- Try an OCR-scanned PDF converter if it's an image PDF
- File should be < 50MB

### Issue: No results found
**Solution**: 
- Try a more specific job title
- Check internet connection
- Verify API key is working

### Issue: App slow to load
**Solution**: 
- Firecrawl API might be rate-limited (wait a minute)
- System resources may be low (restart app)
- Use manual search instead of CV upload for quick results

## 📝 Tips & Tricks

1. **Resume Format**: Use clean, text-based PDFs (avoid image PDFs)
2. **Keyword Rich**: Include industry keywords in your CV for better detection
3. **Multiple Searches**: Run multiple searches with different roles
4. **Save Results**: Copy URLs to a document/spreadsheet for tracking
5. **Customization**: Adjust preferences in sidebar for tailored results

## 🤝 Contributing

Found a bug or have suggestions? 
- Create an issue
- Submit pull requests
- Add support for more job platforms

## 📄 License

MIT License - feel free to fork and modify!

## 🌟 Support

- 📧 Email: support@JobStreampro.com
- 💬 Issues: GitHub Issues
- 🐦 Twitter: @JobStreamProApp

---

**Happy job hunting! 🎉**

