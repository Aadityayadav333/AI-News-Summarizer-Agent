# 🎬 How to Embed Video in GitHub README

## Method 1: Direct Upload (Recommended & Easiest)

### Step 1: Push Everything to GitHub First
```bash
git add .
git commit -m "Add project files"
git remote add origin https://github.com/Aadityayadav333/AI-News-Summarizer-Agent.git
git push -u origin main
```

### Step 2: Edit README on GitHub
1. Go to https://github.com/Aadityayadav333/AI-News-Summarizer-Agent
2. Click on `README.md`
3. Click the **pencil icon** (Edit this file)
4. In the editor, find the Demo section
5. **Drag and drop** your video file (`Screen Recording 2026-01-14 011707.mp4`) directly into the editor
6. GitHub will automatically upload it and give you a link like:
   ```
   https://github.com/Aadityayadav333/AI-News-Summarizer-Agent/assets/123456789/abc123-video.mp4
   ```
7. **Copy that link** and replace the PLACEHOLDER line with it
8. Click **"Commit changes"**

### What It Should Look Like:
```markdown
## 📺 Demo

https://github.com/Aadityayadav333/AI-News-Summarizer-Agent/assets/123456789/your-actual-video-id.mp4
```

---

## Method 2: Using GitHub Issues (Alternative)

1. Go to your repo → Issues → New Issue
2. Drag and drop your video into the issue description
3. GitHub will upload it and show the URL
4. Copy that URL
5. Cancel the issue (don't create it)
6. Paste the URL in README

---

## Method 3: Convert to GIF (Best for Quick Preview)

If video is too large (>10MB), convert to GIF:

### Using Online Tool:
1. Go to https://ezgif.com/video-to-gif
2. Upload your MP4
3. Convert to GIF
4. Download the GIF
5. Add to repo and reference in README:
   ```markdown
   ![Demo](demo.gif)
   ```

### Or Use Command Line:
```bash
# Install ffmpeg first
# Then convert (this will make it smaller)
ffmpeg -i "Screen Recording 2026-01-14 011707.mp4" -vf "fps=10,scale=800:-1" demo.gif
```

---

## ✅ Recommended Approach:

**Just use Method 1!** It's the easiest:

1. Push your code to GitHub first
2. Go to GitHub and edit README.md online
3. Drag and drop the video
4. Commit

The video will play inline in your README! 🎉

---

## 📝 After Embedding:

Your README will show:
- A video player embedded directly in the page
- Anyone can watch without downloading
- Video plays in GitHub's native player

Perfect for showcasing your project! 🚀
