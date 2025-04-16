# 🤖 AutoPostBot - LinkedIn Automation Suite

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/Lusan-sapkota/AutoPostBot)
[![Python](https://img.shields.io/badge/Python-3.x-green?logo=python)](https://www.python.org/)
[![LinkedIn](https://img.shields.io/badge/Platform-LinkedIn-0077B5?logo=linkedin)](https://linkedin.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?logo=selenium)](https://www.selenium.dev/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini-4285F4?logo=google)](https://ai.google.dev/)
[![Pexels](https://img.shields.io/badge/Images-Pexels-05A081?logo=pexels)](https://www.pexels.com/)
[![Unsplash](https://img.shields.io/badge/Images-Unsplash-000000?logo=unsplash)](https://unsplash.com/)

<p align="center">
  <img src="https://i.imgur.com/YourLogoHere.png" alt="AutoPostBot Logo" width="180" height="180">
</p>

<h2 align="center">Your AI-Powered Social Media Assistant</h2>

> **Take your LinkedIn content strategy to the next level with intelligent automation and AI-generated posts**

This advanced Python-based tool helps professionals and businesses maintain a consistent and engaging LinkedIn presence by automatically generating and posting high-quality content. Leveraging Google's Generative AI (Gemini) for text and professional stock photos from Pexels and Unsplash for visuals, AutoPostBot creates compelling posts that resonate with your audience - saving you hours of content creation time.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Setup](#-setup)
- [🎯 Usage](#-usage)
- [🔧 Operation Details](#-operation-details)
- [📊 Best Practices](#-best-practices)
- [🔮 Future Plans](#-future-plans)
- [❓ Troubleshooting](#-troubleshooting)
- [👨‍💻 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### Content Generation & Management
* **🤖 Automated Posting:** Schedule and publish content to LinkedIn without manual intervention
* **📝 AI Text Generation:** Harness Google's Gemini AI to craft engaging, professional post text
* **🖼️ Professional Images:** Automatically fetch relevant visuals from Pexels and Unsplash libraries
* **📚 Topic Management:** Smart tracking system that moves completed topics from `Topics.txt` to `Topics_done.txt`
* **📊 Content Variety:** Generate diverse content types including how-tos, listicles, thought leadership, and industry insights

### Technical Features
* **🔑 Secure Session Management:** Efficiently handles LinkedIn login and maintains session persistence
* **⏱️ Intelligent Scheduling:** Built-in posting schedule with manual override options
* **🛡️ Robust Error Handling:** Comprehensive error recovery with detailed logging
* **🔒 Concurrency Control:** Lock file system prevents multiple instances from causing conflicts
* **🔐 Security Protection:** Advanced handling of LinkedIn's verification prompts and security challenges

### User Experience
* **🎮 Interactive Command Menu:** User-friendly CLI interface for managing all posting operations
* **👁️ Content Preview:** Review and approve AI-generated content before posting
* **🎨 Image Selection:** Choose from multiple suggested images for each post
* **📱 Mobile-Friendly:** Creates posts optimized for both desktop and mobile viewing

## 🚀 Setup

### 1️⃣ Prerequisites:
* Python 3.x installed on your system
* Basic familiarity with command line operations
* LinkedIn account with posting permissions
* API keys for content generation (Google Gemini, Pexels, Unsplash)

### 2️⃣ Clone the Repository:
```bash
git clone https://github.com/Lusan-sapkota/AutoPostBot.git
cd AutoPostBot
```

### 3️⃣ Install Dependencies:
```bash
# Using requirements.txt
pip install -r requirements.txt

# Or manually install dependencies
pip install selenium webdriver-manager python-dotenv google-generativeai questionary colorama pillow requests
```

### 4️⃣ Configure Environment Variables:
Create a file named `.env` in the project root directory:
```dotenv
# LinkedIn Credentials
LINKEDIN_USERNAME=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password

# API Keys
GEMINI_API_KEY=your_google_gemini_api_key
PEXELS_API_KEY=your_pexels_api_key
UNSPLASH_API_KEY=your_unsplash_api_key
```

### 5️⃣ Prepare Topics:
Create a file named `Topics.txt` in the project root directory:
```
# Topics.txt example
The future of AI in software development
Tips for effective remote team collaboration
Benefits of using Python for automation
Top 10 productivity hacks for developers
How to build a personal brand on LinkedIn
The impact of blockchain on supply chain management
Essential cybersecurity practices for small businesses
Why continuous learning matters in tech careers
```

### 6️⃣ Browser Configuration (Optional):
* For headless operation, modify the browser settings in `browser.py`
* For custom browser profiles, adjust the WebDriver initialization parameters

## 🎯 Usage

### Starting the Bot:
```bash
python browser.py
```

### Command-line Arguments:
* `--force`: Override schedule and post immediately regardless of timing conditions
* `--no-verify`: Disable device verification checks during login process
* `--headless`: Run the browser in headless mode (no visible browser window)
* `--no-images`: Skip image generation for text-only posts
* `--debug`: Enable verbose debug logging for troubleshooting

### Interactive Menu Walkthrough:

#### 1️⃣ Main Menu
Upon successful login, you'll be presented with an interactive menu:
- **Post from Topics.txt:** Create and publish content from your topic list
- **Generate New Topics:** Get AI suggestions for new content ideas
- **View Posting History:** See your previously posted content
- **Settings:** Configure bot behavior and preferences
- **Exit:** Safely terminate the bot

#### 2️⃣ Topic Selection
When choosing to post:
1. Select from available topics in `Topics.txt`
2. Review the AI-generated content with formatting preview
3. Choose from suggested images (from Pexels or Unsplash)
4. Edit content if needed before final approval
5. Confirm posting to your LinkedIn profile

#### 3️⃣ Image Selection
For posts with images:
1. View thumbnails of AI-selected relevant images
2. Choose your preferred image or request new options
3. Optionally adjust image cropping/positioning

## 🔧 Operation Details

The bot follows this sophisticated workflow during operation:

1. **Initialization:** Launches a Selenium WebDriver with optimized settings
2. **Authentication:** Securely logs in using your LinkedIn credentials
3. **Session Persistence:** Saves authenticated session to `linkedin_session.json` for faster future logins
4. **Topic Selection:** Intelligently chooses topics based on your preference or scheduling parameters
5. **Content Generation:** 
   - Sends topic to Google Gemini AI for professional content creation
   - Queries Pexels and Unsplash APIs for relevant high-quality images
6. **User Review:** Presents generated content for your approval
7. **Publishing:** Posts approved content to LinkedIn with proper formatting
8. **Tracking:** Updates topic lists and maintains posting history
9. **Cleanup:** Safely removes temporary files and releases system resources

## 📊 Best Practices

### Content Strategy
* **Topic Diversity:** Mix thought leadership, educational content, and industry news
* **Posting Frequency:** 2-3 times per week for optimal engagement without overwhelming followers
* **Image Selection:** Choose images that enhance your message rather than distract from it
* **Content Length:** 150-250 words typically perform best on LinkedIn

### Technical Optimization
* **Schedule Posts:** Use during business hours for maximum visibility (Tues-Thurs typically best)
* **API Limits:** Be mindful of daily API request limits for image services
* **Browser Updates:** Keep your Chrome/Firefox browser updated for compatibility
* **Regular Backups:** Periodically back up your `Topics.txt` and settings

## 🔮 Future Plans

* **🐦 Twitter Integration:** Automatic thread generation and posting capabilities
* **📱 Multi-Platform Support:** Expansion to Facebook, Instagram, and Medium
* **📅 Advanced Scheduling:** Calendar-based posting with time targeting
* **🔄 Content Analytics:** Track performance metrics to optimize future posts
* **🖥️ Web Interface:** Browser-based dashboard for easier management
* **🧠 Learning Algorithm:** Content optimization based on engagement patterns
* **🔁 Content Repurposing:** Transform single topics into multiple platform-specific formats
* **🔍 Hashtag Optimization:** AI-powered hashtag suggestions for improved reach
* **🔊 Audio/Video Content:** Support for multimedia content generation
* **📈 Growth Tracking:** Monitor follower growth and engagement metrics

## ❓ Troubleshooting

### Common Issues

* **Login Failures**
  * Solution: Delete `linkedin_session.json` and try again with fresh credentials
  * Check for any recent LinkedIn password changes or security settings updates

* **Verification Challenges**
  * Solution: LinkedIn may require verification when logging in from new locations
  * Manually log in once from your browser if verification is regularly triggered

* **Rate Limiting**
  * Solution: Reduce posting frequency to avoid LinkedIn's automated restrictions
  * Implement random delays between actions to appear more human-like

* **Image Generation Problems**
  * Solution: Verify your Pexels and Unsplash API keys are valid and have sufficient quota
  * Try alternative search terms if specific topics yield poor image results

* **Browser Compatibility**
  * Solution: Update Chrome/Firefox and webdriver to the latest versions
  * Check console logs for specific selenium errors

### Getting Help

If you encounter issues not covered here, please:
1. Check the [GitHub Issues](https://github.com/Lusan-sapkota/AutoPostBot/issues) section for similar problems
2. Enable debug mode (`--debug`) to generate detailed logs
3. Open a new issue with your specific error messages and environment details

## 👨‍💻 Contributing

Contributions are enthusiastically welcomed! Here's how you can help improve AutoPostBot:

1. **Fork the Repository:** Create your own copy of the project
2. **Create a Feature Branch:** `git checkout -b feature/amazing-feature`
3. **Make Your Changes:** Implement your improvements or fixes
4. **Follow Coding Standards:** Ensure your code follows project style guidelines
5. **Add Tests:** Write tests for new functionality when applicable
6. **Document Your Changes:** Update README or comments as needed
7. **Commit Changes:** `git commit -am 'Add some amazing feature'`
8. **Push to Branch:** `git push origin feature/amazing-feature`
9. **Submit a Pull Request:** Create a PR with a clear description of your changes

### Development Guidelines
* Follow PEP 8 style guidelines for Python code
* Maintain backwards compatibility when possible
* Add comments for complex logic
* Update documentation for user-facing changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <img src="https://i.imgur.com/YourBannerHere.png" alt="AutoPostBot Banner" width="600">
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/Lusan-sapkota">Lusan Sapkota</a>
</p>

<p align="center">
  <a href="https://github.com/Lusan-sapkota/AutoPostBot/stargazers">Star this repo</a> if you find it useful!
</p>