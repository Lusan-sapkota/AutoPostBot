import os
import re
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import argparse
import questionary
from colorama import init, Fore, Style

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize colorama for colored console output
init()

class LinkedInBot:
    def __init__(self):
        self.driver = self.setup_driver()
        self.login()

    def setup_driver(self):
        """Sets up a highly-disguised Chrome WebDriver that mimics human behavior."""
        chrome_options = Options()
        
        # Anti-detection options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Random user agent from pool
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.92",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        ]
        selected_user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"user-agent={selected_user_agent}")

        # Language and feature flags
        chrome_options.add_argument("--lang=en-US")
        chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")

        # WebGL and media stream
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--use-fake-device-for-media-stream")

        # Persistent session
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        os.makedirs(user_data_dir, exist_ok=True)
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        # Headless mode (optional toggle with DISABLE_HEADLESS env)
        if not os.getenv("DISABLE_HEADLESS", False):
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")

        # Start WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Standard screen size
        driver.set_window_size(1920, 1080)

        # JavaScript-based anti-detection fingerprinting
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("window.navigator.chrome = { runtime: {} }")
        driver.execute_script("Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] })")
        driver.execute_script("Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] })")
        driver.execute_script("""
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            Object.defineProperty(screen, 'colorDepth', {get: () => 24});
        """)

        # Optional: Add fake timezone
        driver.execute_script("const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto")

        # Call custom behavior functions
        self._configure_random_behavior(driver)
        self._set_consistent_fingerprint(driver)

        return driver

    def _set_consistent_fingerprint(self, driver):
        """Set consistent fingerprint values to avoid triggering security alerts."""
        try:
            # Set consistent navigator properties
            js_script = """
            # Set consistent values for properties that are used in fingerprinting
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            Object.defineProperty(screen, 'colorDepth', {get: () => 24});
            Object.defineProperty(screen, 'pixelDepth', {get: () => 24});
            Object.defineProperty(navigator, 'platform', {get: () => 'Linux x86_64'});
            
            # Override canvas fingerprinting
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {
                if (this.width === 0 || this.height === 0) {
                    return originalToDataURL.apply(this, arguments);
                }
                return originalToDataURL.call(this, type);
            };
            
            # Override AudioContext fingerprinting
            if (typeof AudioBuffer !== 'undefined') {
                const originalGetChannelData = AudioBuffer.prototype.getChannelData;
                AudioBuffer.prototype.getChannelData = function() {
                    const channelData = originalGetChannelData.apply(this, arguments);
                    return channelData;
                }
            }
            """
            driver.execute_script(js_script)
        except Exception as e:
            logging.error(f"Error setting consistent fingerprint: {str(e)}")

    def _configure_random_behavior(self, driver):
        """Configure random behavioral patterns to appear more human-like."""
        # Inject mouse movement script
        mouse_script = """
        (function(){
            const origOpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function() {
                this.addEventListener('load', function() {
                    # Add slight random delay to responses
                    setTimeout(() => {}, Math.floor(Math.random() * 100));
                });
                origOpen.apply(this, arguments);
            };
        })();
        """
        try:
            driver.execute_script(mouse_script)
        except:
            pass

    def random_delay(self, min_delay=1, max_delay=3):
        """Introduce a random delay to mimic human behavior."""
        time.sleep(random.uniform(min_delay, max_delay))

    def login(self):
        """Logs into LinkedIn using credentials from environment variables, with session handling."""
        try:
            # First check if we're already logged in by visiting the feed
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(2, 3)
            
            # Check for login state by looking for feed elements
            already_logged_in = False
            try:
                # Look for elements that only appear when logged in
                feed_elements = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]"))
                )
                logging.info("Already logged in - session exists")
                already_logged_in = True
            except:
                logging.info("Not logged in - will need to authenticate")
                already_logged_in = False
                
            # If we're already logged in, we can skip the login procedure
            if already_logged_in:
                return
                
            # Not logged in, proceed with login process
            # Add a random delay to avoid pattern detection
            self.random_delay(1, 3)
            
            self.driver.get("https://www.linkedin.com/login")
            
            # Use different timing patterns for credentials entry
            # Sometimes fast, sometimes slow - more human-like
            typing_speed = random.choice(["slow", "normal", "fast"])
            
            delay_ranges = {
                "slow": (0.2, 0.5),
                "normal": (0.1, 0.3),
                "fast": (0.05, 0.15)
            }
            
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")

            # Enter username with random timing
            for char in os.getenv("LINKEDIN_USERNAME"):
                username_field.send_keys(char)
                self.random_delay(*delay_ranges[typing_speed])
                
            # Random pause between username and password
            self.random_delay(0.5, 2)

            # Enter password with different timing
            # Use a different typing pattern for password
            typing_speed = random.choice(["slow", "normal", "fast"])
            for char in os.getenv("LINKEDIN_PASSWORD"):
                password_field.send_keys(char)
                self.random_delay(*delay_ranges[typing_speed])
                
            self.random_delay(0.5, 1.5)

            # Sometimes click the button, sometimes press Enter
            if random.random() < 0.7:  # 70% chance to press Enter
                password_field.send_keys(Keys.RETURN)
            else:
                sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                sign_in_button.click()
                
            # Wait longer for login to complete
            self.random_delay(5, 8)

            # Check for verification code input form
            try:
                verification_form = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "email-pin-challenge"))
                )
                logging.info("Verification code required. Prompting user for input.")
                verification_code = input("Enter the verification code sent to your email: ")

                # Enter the verification code
                code_input = self.driver.find_element(By.ID, "input__email_verification_pin")
                for char in verification_code:
                    code_input.send_keys(char)
                    self.random_delay(0.1, 0.3)

                # Submit the verification form
                submit_button = self.driver.find_element(By.ID, "email-pin-submit-button")
                submit_button.click()

                # Wait for the process to complete
                self.random_delay(10, 12)
                
                # Navigate to the feed after verification
                self.driver.get("https://www.linkedin.com/feed/")
                logging.info("Logged in with verification and navigated to feed")
            except Exception as e:
                logging.info("Verification code not required or error occurred.")
                
                # Check if we're actually logged in by looking for feed elements
                try:
                    self.driver.get("https://www.linkedin.com/feed/")
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]"))
                    )
                    logging.info("Successfully logged in and verified by checking feed elements")
                except:
                    logging.error("Failed to verify login state after authentication attempt")
                    
        except Exception as e:
            logging.error(f"Error during login process: {str(e)}", exc_info=True)
            # Take a screenshot for debugging
            self.driver.save_screenshot(f"login_error_{int(time.time())}.png")

    def remove_markdown(self, text, ignore_hashtags=False):
        """Removes markdown syntax from a given text string."""
        patterns = [
            r"(\*{1,2})(.*?)\1",  # Bold and italics
            r"\[(.*?)\]\((.*?)\)",  # Links
            r"`(.*?)`",  # Inline code
            r"(\n\s*)- (.*)",  # Unordered lists (with `-`)
            r"(\n\s*)\* (.*)",  # Unordered lists (with `*`)
            r"(\n\s*)[0-9]+\. (.*)",  # Ordered lists
            r"(#+)(.*)",  # Headings
            r"(>+)(.*)",  # Blockquotes
            r"(---|\*\*\*)",  # Horizontal rules
            r"!\[(.*?)\]\((.*?)\)",  # Images
        ]

        # If ignoring hashtags, remove the heading pattern
        if ignore_hashtags:
            patterns.remove(r"(#+)(.*)")

        # Replace markdown elements with an empty string
        for pattern in patterns:
            text = re.sub(
                pattern, r" ", text
            )  

        return text.strip()

    def generate_post_content(self, topic):
        """Generates high-quality post content using Gemini AI based on the given topic and current trends."""
        logging.info(f"Generating post content for topic: {topic}")
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")
            client = genai.GenerativeModel("gemini-1.5-flash")
            
            # Get current date for context
            current_date = time.strftime("%B %d, %Y")
            
            # Try to fetch trending topics (optional)
            trending_topics = self._get_trending_topics()
            trending_context = ""
            if trending_topics:
                trending_context = f"Consider these current trending topics if relevant: {', '.join(trending_topics[:3])}."
            
            prompt = f"""
            Today is {current_date}. Create a LinkedIn post about: "{topic}"
            
            The post should:
            1. Start with a compelling hook or statistic
            2. Share a personal insight or experience related to the topic
            3. Provide 3-4 practical takeaways or insights
            4. Include relevant hashtags (5-7 hashtags)
            5. End with an engaging question to promote comments
            
            {trending_context}
            
            Make the post sound authentic, professional and conversational.
            Total length should be 1000-1500 characters.
            Avoid obvious AI-generated patterns and corporate jargon.
            Include some personality and a touch of human imperfection.
            """
            
            # Use structured generation
            messages = [{"role": "user", "parts": [prompt]}]
            
            generation_config = {
                "temperature": 0.7,  # Add some creativity
                "top_p": 0.95,
                "top_k": 40,
            }
            
            post_response = client.generate_content(
                messages,
                generation_config=generation_config
            )
            
            if post_response.text:
                # Process the generated text
                post_text = self.remove_markdown(post_response.text, ignore_hashtags=True)
                
                # Ensure hashtags are properly formatted
                post_text = self._ensure_proper_hashtags(post_text)
                
                return post_text
            else:
                return f"Excited to share some thoughts on {topic}! #technology #leadership"
        except Exception as e:
            logging.error(f"Failed to generate post content: {str(e)}", exc_info=True)
            return f"Excited to share some thoughts on {topic}! #technology #leadership"

    def _get_trending_topics(self):
        """Try to fetch trending topics from LinkedIn to make posts more relevant."""
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(2, 3)
            
            trending_elements = self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'trending-item')]//span[contains(@class, 'feed-shared-text')]")
            
            if not trending_elements:
                trending_elements = self.driver.find_elements(By.XPATH,
                    "//div[contains(@class, 'news-module')]//span[contains(@class, 'item-title')]")
            
            trending_topics = []
            for element in trending_elements[:5]:  # Get top 5 trending topics
                topic_text = element.text.strip()
                if topic_text:
                    trending_topics.append(topic_text)
                    
            return trending_topics
        except Exception as e:
            logging.error(f"Error fetching trending topics: {str(e)}")
            return []
            
    def _ensure_proper_hashtags(self, text):
        """Ensure text has properly formatted hashtags."""
        # Check if text already has hashtags
        if '#' in text:
            return text
            
        # Extract potential hashtag words (nouns, adjectives, etc.)
        words = text.split()
        potential_hashtags = [word for word in words 
                             if len(word) > 4 and word[0].isupper() and word.isalpha()]
        
        # Add topic-related hashtags
        hashtags = ["#LinkedInPost", "#ProfessionalDevelopment", "#CareerGrowth"]
        
        # Add a few from potential hashtags
        for word in potential_hashtags[:4]:
            hashtags.append(f"#{word.strip('.,!?;:()[]{}').lower()}")
        
        # Add hashtags to the end of the post
        return text + "\n\n" + " ".join(hashtags)

    def generate_image(self, topic):
        """Generate a relevant image for the post using a stock image API."""
        try:
            image_method = random.choice(["unsplash", "pexels", "local"])
            
            # Try the chosen method first
            image_path = None
            if image_method == "unsplash":
                image_path = self._get_unsplash_image(topic)
            elif image_method == "pexels":
                image_path = self._get_pexels_image(topic)
            else:
                image_path = self._get_local_image()
                
            # If the chosen method failed, try alternatives
            if not image_path:
                if image_method != "unsplash":
                    image_path = self._get_unsplash_image(topic)
                if not image_path and image_method != "pexels":
                    image_path = self._get_pexels_image(topic)
                if not image_path and image_method != "local":
                    image_path = self._get_local_image()
                    
            # If all methods failed, use a backup approach - store some default images
            if not image_path:
                # Create backup folder if it doesn't exist
                backup_dir = "backup_images"
                os.makedirs(backup_dir, exist_ok=True)
                
                # Default to a professional image by category
                categories = {
                    "cloud": "cloud_computing.jpg",
                    "technology": "technology.jpg",
                    "leadership": "leadership.jpg",
                    "business": "business.jpg",
                    "collaboration": "collaboration.jpg",
                    "default": "professional.jpg"
                }
                
                # Find relevant category
                topic_lower = topic.lower()
                image_file = categories["default"]
                for key, filename in categories.items():
                    if key in topic_lower:
                        image_file = filename
                        break
                        
                # Check if file exists in backup folder, if not, use online source
                backup_file = os.path.join(backup_dir, image_file)
                if os.path.exists(backup_file):
                    # Copy to a temp file
                    temp_image = f"temp_image_{int(time.time())}.jpg"
                    import shutil
                    shutil.copy(backup_file, temp_image)
                    return temp_image
                    
                # Otherwise return None, and the post will be made without an image
                logging.info("No suitable image found, will post without an image")
                    
            return image_path
        except Exception as e:
            logging.error(f"Failed to generate image: {str(e)}")
            return None

    def _get_unsplash_image(self, topic):
        """Get a relevant image from Unsplash."""
        import requests
        
        try:
            # Get API key from environment
            access_key = os.getenv("UNSPLASH_API_KEY")
            if not access_key:
                logging.error("Unsplash API key not found in environment variables")
                return None
            
            # Clean and enhance the topic for search
            # Extract meaningful keywords from the topic
            topic_lower = topic.lower()
            
            # List of common filler words to remove
            fillers = ["the", "of", "in", "on", "at", "and", "or", "for", "to", "a", "an", "benefits", "impact"]
            
            # Extract key concepts based on topic
            search_terms = []
            if "cloud" in topic_lower or "collaboration" in topic_lower:
                search_terms.append("cloud computing collaboration")
            elif "technology" in topic_lower and "automotive" in topic_lower:
                search_terms.append("automotive technology")
            elif "machine learning" in topic_lower or "ai" in topic_lower:
                search_terms.append("artificial intelligence technology")
            elif "sustainability" in topic_lower or "green" in topic_lower:
                search_terms.append("sustainability business")
            else:
                # Default approach - extract key words
                words = topic_lower.split()
                key_words = [word for word in words if word not in fillers and len(word) > 3]
                search_terms = [" ".join(key_words[:2])]
                if not search_terms[0]:
                    search_terms = ["business professional"]
            
            search_term = search_terms[0]
            
            logging.info(f"Generated image search term: '{search_term}' from topic: '{topic}'")
            url = f"https://api.unsplash.com/photos/random?query={search_term}&orientation=landscape"
            headers = {"Authorization": f"Client-ID {access_key}"}
            
            logging.info(f"Requesting image from Unsplash for search term: {search_term}")
            response = requests.get(url, headers=headers, timeout=10)  # Add timeout
            
            if response.status_code == 200:
                image_data = response.json()
                image_url = image_data["urls"]["regular"]
                
                # Download the image
                logging.info(f"Downloading image from URL: {image_url}")
                image_response = requests.get(image_url, timeout=10)  # Add timeout
                
                if image_response.status_code == 200:
                    image_path = f"temp_image_{int(time.time())}.jpg"
                    with open(image_path, "wb") as file:
                        file.write(image_response.content)
                    logging.info(f"Image saved to: {image_path}")
                    return image_path
                else:
                    logging.error(f"Failed to download image. Status code: {image_response.status_code}")
            else:
                logging.error(f"Failed to get image from Unsplash. Status code: {response.status_code}")
                if response.status_code == 403:
                    logging.error("Possible API key issue or rate limit exceeded")
                elif response.status_code == 429:
                    logging.error("Rate limit exceeded")
            
            return None
        except Exception as e:
            logging.error(f"Error getting Unsplash image: {str(e)}")
            return None

    def _get_pexels_image(self, topic):
        """Get a relevant image from Pexels."""
        import requests
        
        try:
            # Note: Get your own API key from Pexels
            api_key = os.getenv("PEXELS_API_KEY")
            
            # Clean the topic for search
            search_term = topic.lower().split()
            search_term = "+".join(search_term[:2])
            
            url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=1"
            headers = {"Authorization": api_key}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                image_data = response.json()
                if image_data["photos"]:
                    image_url = image_data["photos"][0]["src"]["medium"]
                    
                    # Download the image
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_path = f"temp_image_{int(time.time())}.jpg"
                        with open(image_path, "wb") as file:
                            file.write(image_response.content)
                        return image_path
            
            return None
        except Exception as e:
            logging.error(f"Error getting Pexels image: {str(e)}")
            return None

    def _get_local_image(self):
        """Get a professional image from a local collection."""
        try:
            # Create a directory for professional images if it doesn't exist
            image_dir = "linkedin_images"
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
                # Here you would download or copy some professional stock images
                # For now, we'll assume there are no images
                return None
                
            # Get list of images in the directory
            images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if not images:
                return None
                
            # Select a random image
            selected_image = os.path.join(image_dir, random.choice(images))
            
            # Copy to a temp file to avoid deleting the original
            temp_image = f"temp_image_{int(time.time())}.jpg"
            import shutil
            shutil.copy(selected_image, temp_image)
            
            return temp_image
        except Exception as e:
            logging.error(f"Error getting local image: {str(e)}")
            return None

    def close_overlapping_elements(self):
        """Close any overlays or popups that might interfere with posting."""
        try:
            # List of common overlay selectors
            overlay_selectors = [
                "//button[contains(@class, 'msg-overlay-bubble-header__control--close')]",  # Chat overlay
                "//button[contains(@class, 'artdeco-modal__dismiss')]",  # Modal overlay
                "//button[contains(@aria-label, 'Dismiss')]",  # Generic dismiss
                "//button[contains(@aria-label, 'Close')]",  # Generic close
                "//div[contains(@class, 'feed-shared-overlay')]//button",  # Feed overlay
                "//div[contains(@class, 'welcome-modal')]//button",  # Welcome modal
                "//div[contains(@role, 'dialog')]//button[contains(@aria-label, 'Close')]"  # Dialog
            ]
            
            # Try each selector
            for selector in overlay_selectors:
                try:
                    overlay_elements = self.driver.find_elements(By.XPATH, selector)
                    for element in overlay_elements:
                        if element.is_displayed():
                            element.click()
                            logging.info(f"Closed overlay with selector: {selector}")
                            self.random_delay(1, 2)
                except Exception as e:
                    continue
                    
            # Check for and handle any "Continue" buttons on prompts
            try:
                continue_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Continue')]")
                for button in continue_buttons:
                    if button.is_displayed():
                        button.click()
                        logging.info("Clicked 'Continue' button")
                        self.random_delay(1, 2)
            except:
                pass
                
            logging.info("Finished closing overlapping elements")
        except Exception as e:
            logging.info(f"Error while closing overlapping elements: {str(e)}")

    def post_to_linkedin(self, post_text):
        """Posts content to LinkedIn with enhanced error handling and debugging."""
        timestamp = int(time.time())
        logging.info("Posting to LinkedIn - starting process.")
        try:
            # Close overlapping elements
            self.close_overlapping_elements()
            
            # Handle any welcome screens that may appear
            self.handle_welcome_screens()

            # Navigate to feed to ensure we're in the right context
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(3, 5)
            
            # Save debugging screenshot
            self.driver.save_screenshot(f"before_starting_post_{timestamp}.png")

            # Handle any welcome screens that may appear after navigation
            self.handle_welcome_screens()
            
            # Multiple selector options to find the post button
            post_button_selectors = [
                # Try spans first (outer elements that might be more clickable)
                "//span[text()='Start a post']/parent::*",
                "//span[contains(., 'Start a post')]/parent::*",
                # Then buttons
                "//button[contains(., 'Start a post')]",
                "//button[contains(@class, 'share-box-feed-entry__trigger')]",
                "//button[contains(@data-control-name, 'share.open_share_box')]",
                # Then divs
                "//div[contains(@class, 'share-box-feed-entry__trigger')]",
                "//div[contains(@class, 'share-box')]"
            ]
            
            # Try each selector until one works
            start_post_button = None
            for selector in post_button_selectors:
                try:
                    self.driver.save_screenshot(f"looking_for_start_post_{int(time.time())}.png")
                    start_post_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    # Add highlight for debugging
                    try:
                        self.driver.execute_script("arguments[0].style.border='3px solid red'", start_post_button)
                    except:
                        pass
                    self.driver.save_screenshot(f"found_start_post_button_{int(time.time())}.png")
                    logging.info(f"Found start post button with selector: {selector}")
                    break
                except:
                    continue
            
            if not start_post_button:
                # Try the JavaScript approach to find and click the start post element
                logging.info("Using JavaScript to find start post button")
                try:
                    found = self.driver.execute_script("""
                        # Look for elements containing "Start a post" text
                        const elements = Array.from(document.querySelectorAll('*'))
                            .filter(el => el.textContent.includes('Start a post'));
                        
                        # Find the most likely clickable parent
                        for (const el of elements) {
                            # If the element itself is clickable
                            if (el.tagName === 'BUTTON' || el.tagName === 'A') {
                                el.click();
                                return true;
                            }
                            
                            # Look for clickable parent
                            let parent = el.parentElement;
                            for (let i = 0; i < 3 && parent; i++) {
                                if (parent.tagName === 'BUTTON' || parent.tagName === 'A' || 
                                    parent.getAttribute('role') === 'button') {
                                    parent.click();
                                    return true;
                                }
                                parent = parent.parentElement;
                            }
                        }
                        
                        # If text search failed, try to find share box by class
                        const shareBoxes = document.querySelectorAll('[class*="share-box"]');
                        if (shareBoxes.length) {
                            shareBoxes[0].click();
                            return true;
                        }
                        
                        return false;
                    """)
                    
                    if found:
                        logging.info("Found and clicked start post button using JavaScript")
                    else:
                        logging.error("Could not find the 'Start a post' button using JavaScript")
                        self.driver.save_screenshot(f"error_start_post_js_{int(time.time())}.png")
                        return False
                except Exception as js_error:
                    logging.error(f"JavaScript error finding start post: {str(js_error)}")
                    self.driver.save_screenshot(f"error_start_post_{int(time.time())}.png")
                    return False
                
            # If we found the button via selectors, click it
            if start_post_button:
                # Click the button safely with a random delay before clicking
                self.random_delay(1.5, 3)
                try:
                    start_post_button.click()
                    logging.info("Clicked start post button directly")
                except:
                    # Fall back to JavaScript click if direct click fails
                    self.driver.execute_script("arguments[0].click();", start_post_button)
                    logging.info("Clicked start post button using JavaScript")
            
            self.random_delay(3, 5)
            self.driver.save_screenshot(f"after_start_post_click_{timestamp}.png")
            
            # Multiple selectors for text area with enhanced selection
            text_area_selectors = [
                "div[role='textbox']",
                "div.ql-editor",
                "div[data-placeholder='What do you want to talk about?']",
                "div[contenteditable='true']",
                "div[aria-placeholder='What do you want to talk about?']"
            ]
            
            # Try each selector until one works
            post_text_area = None
            for selector in text_area_selectors:
                try:
                    post_text_area = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    logging.info(f"Found text area with selector: {selector}")
                    break
                except:
                    continue
                    
            if not post_text_area:
                # Try using JavaScript to find editable area
                logging.info("Using JavaScript to find editable text area")
                try:
                    js_result = self.driver.execute_script("""
                        # Look for any contenteditable div
                        const editableElements = document.querySelectorAll('div[contenteditable="true"]');
                        if (editableElements.length) {
                            return editableElements[0];
                        }
                        
                        # Look for elements with textbox role
                        const textboxElements = document.querySelectorAll('[role="textbox"]');
                        if (textboxElements.length) {
                            return textboxElements[0];
                        }
                        
                        # Look for elements with placeholder text about posting
                        const elements = Array.from(document.querySelectorAll('div'))
                            .filter(el => el.getAttribute('data-placeholder') && 
                                el.getAttribute('data-placeholder').includes('talk about'));
                        
                        if (elements.length) {
                            return elements[0];
                        }
                        
                        return null;
                    """)
                    
                    if js_result:
                        post_text_area = js_result
                        logging.info("Found text area using JavaScript")
                    else:
                        logging.error("Could not find the post text area using JavaScript")
                        self.driver.save_screenshot(f"error_text_area_js_{int(time.time())}.png")
                        return False
                except Exception as js_error:
                    logging.error(f"JavaScript error finding text area: {str(js_error)}")
                    self.driver.save_screenshot(f"error_text_area_{int(time.time())}.png")
                    return False
            
            if not post_text_area:
                logging.error("Could not find the post text area using any method")
                self.driver.save_screenshot(f"error_text_area_{int(time.time())}.png")
                return False
            
            # Clear any existing text and enter our content in a human-like way
            try:
                post_text_area.clear()
            except:
                pass
                
            try:
                post_text_area.click()
                self.random_delay(1, 2)
            except:
                # Try JavaScript click
                self.driver.execute_script("arguments[0].click();", post_text_area)
                self.random_delay(1, 2)
            
            # Add a unique identifier to each post for verification
            unique_id = f"[Post ID: {timestamp}]"
            # Add it at the end of the post, but before hashtags
            if "#" in post_text:
                parts = post_text.split("#", 1)
                post_text = parts[0].strip() + f" {unique_id}\n\n#" + parts[1]
            else:
                post_text = post_text.strip() + f" {unique_id}"
            
            # Try to insert text using multiple methods
            inserted_text = False
            
            # Method 1: Standard sendKeys
            try:
                post_text_area.send_keys(post_text)
                inserted_text = True
                logging.info("Inserted text using standard sendKeys")
            except Exception as send_keys_error:
                logging.error(f"Error using standard sendKeys: {str(send_keys_error)}")
                
            # Method 2: Break into chunks and use JavaScript
            if not inserted_text:
                try:
                    # Type text in chunks with variable delays to simulate human typing
                    chunks = self._split_text_into_chunks(post_text, avg_chunk_size=30)
                    for i, chunk in enumerate(chunks):
                        # Occasionally pause longer between paragraphs
                        if "\n\n" in chunk and random.random() < 0.7:
                            self.random_delay(1.5, 3)
                            
                        self.driver.execute_script(
                            "arguments[0].innerText += arguments[1]", post_text_area, chunk
                        )
                        # Vary typing speed
                        if i < len(chunks) - 1:  # Don't delay after the last chunk
                            self.random_delay(0.2, 0.8)
                            
                    inserted_text = True
                    logging.info("Inserted text using JavaScript in chunks")
                except Exception as js_insert_error:
                    logging.error(f"Error using JavaScript text insertion: {str(js_insert_error)}")
                    
            # Method 3: Use clipboard
            if not inserted_text:
                try:
                    # Copy text to clipboard and paste
                    from pyperclip import copy
                    copy(post_text)
                    
                    # Focus the element
                    self.driver.execute_script("arguments[0].focus();", post_text_area)
                    
                    # Send paste command
                    actions = ActionChains(self.driver)
                    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                    
                    inserted_text = True
                    logging.info("Inserted text using clipboard paste")
                except Exception as clipboard_error:
                    logging.error(f"Error using clipboard insertion: {str(clipboard_error)}")
            
            if not inserted_text:
                logging.error("Could not insert text using any method")
                self.driver.save_screenshot(f"error_inserting_text_{int(time.time())}.png")
                return False
            
            # Verify text was entered
            self.random_delay(2, 4)
            self.driver.save_screenshot(f"after_text_entry_{timestamp}.png")
            
            # Random pause before posting (human-like behavior)
            self.random_delay(2, 4)
            
            # Use the enhanced method to find and click the post button
            post_button_result = self._find_post_button_advanced()
            
            if post_button_result is True:  # Button was already clicked by the finder method
                logging.info("Post button was already clicked by the finder method")
            elif post_button_result:  # Button element was returned
                # Click post button with a delay to mimic human behavior
                self.random_delay(1, 2)
                try:
                    # Try direct click first
                    post_button_result.click()
                    logging.info("Clicked post button directly")
                except:
                    # Fall back to JavaScript click if direct click fails
                    self.driver.execute_script("arguments[0].click();", post_button_result)
                    logging.info("Clicked post button using JavaScript")
            else:
                logging.error("Could not find or click the post button")
                self.driver.save_screenshot(f"error_post_button_{int(time.time())}.png")
                return False
            
            # Wait for posting to complete
            self.random_delay(3, 5)
            
            # Take screenshot after clicking
            self.driver.save_screenshot(f"after_post_click_{timestamp}.png")
            
            # Verify the post was successful
            try:
                # Go to profile to check
                self.driver.get("https://www.linkedin.com/in/me/recent-activity/shares/")
                self.random_delay(5, 7)  # Longer delay to ensure the post appears
                
                # Check if our unique ID is in the page
                page_source = self.driver.page_source
                if unique_id in page_source:
                    logging.info("Post verified by finding unique ID in profile activity")
                    self.driver.save_screenshot(f"post_verified_{timestamp}.png")
                    return True
                else:
                    # Go back to feed and see if we can see our post there
                    self.driver.get("https://www.linkedin.com/feed/")
                    self.random_delay(3, 5)
                    
                    # Check if we can see our post in the feed
                    page_source = self.driver.page_source
                    if unique_id in page_source:
                        logging.info("Post verified by finding unique ID in feed")
                        self.driver.save_screenshot(f"post_verified_in_feed_{timestamp}.png")
                        return True
                    else:
                        logging.warning("Could not verify post by finding unique ID")
                        # Still return True as LinkedIn sometimes delays showing posts
                        self.driver.save_screenshot(f"post_unverified_{timestamp}.png")
                        return True
            except Exception as verification_error:
                logging.error(f"Error during post verification: {str(verification_error)}")
                # Assume success anyway since we made it this far
                return True
                    
        except Exception as e:
            logging.error(f"Failed to post to LinkedIn: {str(e)}", exc_info=True)
            self.driver.save_screenshot(f"error_posting_{int(time.time())}.png")
            
            # Save the HTML source for debugging
            try:
                with open(f"page_source_error_{int(time.time())}.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
            except:
                pass
                
            return False

    
    def _find_post_button_advanced(self):
        """Advanced method to find the post button using multiple approaches with enhanced debugging."""
        try:
            logging.info("Starting advanced post button detection...")
            self.driver.save_screenshot(f"post_button_search_start_{int(time.time())}.png")
            
            # APPROACH 1: Direct full page screenshot analysis and JavaScript query
            try:
                # Take a full screenshot for analysis
                self.driver.save_screenshot(f"full_page_before_button_search_{int(time.time())}.png")
                
                # Use JavaScript to find all buttons on the page
                all_buttons_js = """
                return Array.from(document.querySelectorAll('button')).map(button => ({
                    text: button.innerText.trim(),
                    classes: button.className,
                    enabled: !button.disabled,
                    visible: button.offsetParent !== null,
                    ariaLabel: button.getAttribute('aria-label'),
                    id: button.id,
                    rect: button.getBoundingClientRect()
                }));
                """
                buttons_info = self.driver.execute_script(all_buttons_js)
                
                # Log all buttons found
                with open(f"all_buttons_info_{int(time.time())}.json", "w") as f:
                    import json
                    json.dump(buttons_info, f, indent=2)
                    
                # Find potential post buttons by text
                post_button_candidates = []
                for btn in buttons_info:
                    button_text = btn.get('text', '').lower()
                    aria_label = (btn.get('ariaLabel') or '').lower()
                    classes = btn.get('classes', '')
                    
                    # Check various patterns that would indicate a Post button
                    if (('post' in button_text or 'share' in button_text or 'publish' in button_text) and 
                        btn.get('enabled', False) and btn.get('visible', False)):
                        post_button_candidates.append(btn)
                        
                    # Also check aria-label for accessibility text
                    elif (('post' in aria_label or 'share' in aria_label or 'publish' in aria_label) and 
                        btn.get('enabled', False) and btn.get('visible', False)):
                        post_button_candidates.append(btn)
                        
                    # Check for primary action buttons in share context
                    elif ('primary-action' in classes or 'share' in classes) and btn.get('enabled', False) and btn.get('visible', False):
                        post_button_candidates.append(btn)
                        
                # Log potential candidates
                logging.info(f"Found {len(post_button_candidates)} potential post button candidates via JavaScript")
                
                # Try to click the most likely candidate via JavaScript
                if post_button_candidates:
                    # Sort by probability (post > share > publish)
                    def btn_score(btn):
                        text = (btn.get('text') or '').lower()
                        score = 0
                        if 'post' in text: score += 10
                        if 'share' in text: score += 5 
                        if 'publish' in text: score += 3
                        if btn.get('enabled', False): score += 2
                        if 'primary' in (btn.get('classes') or ''): score += 2
                        return score
                    
                    post_button_candidates.sort(key=btn_score, reverse=True)
                    
                    # Try clicking the highest scored button
                    best_candidate = post_button_candidates[0]
                    logging.info(f"Best post button candidate: {best_candidate}")
                    
                    # Use JavaScript to find and click the button using multiple attributes
                    click_script = """
                    const buttons = document.querySelectorAll('button');
                    for (const button of buttons) {
                        if (button.innerText.trim().toLowerCase() === arguments[0] && 
                            !button.disabled && 
                            button.offsetParent !== null) {
                            console.log('Found button by text:', button);
                            button.click();
                            return true;
                        }
                    }
                    return false;
                    """
                    if best_candidate.get('text'):
                        result = self.driver.execute_script(click_script, best_candidate.get('text').lower())
                        if result:
                            logging.info("Successfully clicked post button using JavaScript text search")
                            return True
                
            except Exception as js_error:
                logging.error(f"JavaScript button analysis failed: {str(js_error)}")
                
            # APPROACH 2: Updated standard selectors with new LinkedIn UI patterns
            post_button_selectors = [
                # Traditional selectors
                "//button[contains(@class, 'share-actions__primary-action')]",
                "//button[contains(text(), 'Post')]",
                "//button[text()='Post']",
                "//button[contains(@class, 'share-box_actions')]",
                "//button[contains(@class, 'share-actions__publish-button')]",
                # New LinkedIn UI selectors (2025)
                "//button[@data-test-id='post-button']",
                "//button[contains(@data-control-name, 'share.post')]",
                "//div[contains(@class, 'share-box-footer')]//button[contains(@class, 'primary')]",
                "//div[contains(@class, 'share-creation-state__footer')]//button[contains(@class, 'primary')]",
                "//div[contains(@class, 'share-box-footer')]//button[last()]",
                # Very generic fallbacks
                "//footer//button[contains(@class, 'primary')]",
                "//div[contains(@role, 'dialog')]//footer//button[last()]",
                "//div[contains(@class, 'share-creation-state')]//footer//button"
            ]
            
            # Try each selector with detailed logging
            for idx, selector in enumerate(post_button_selectors):
                try:
                    logging.info(f"Trying post button selector #{idx+1}: {selector}")
                    post_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if post_button and post_button.is_displayed() and post_button.is_enabled():
                        # Take a screenshot with the button highlighted if possible
                        try:
                            self.driver.execute_script(
                                "arguments[0].style.border='3px solid red'", post_button
                            )
                        except:
                            pass
                        self.driver.save_screenshot(f"found_post_button_{int(time.time())}.png")
                        logging.info(f"Found post button with selector: {selector}")
                        return post_button
                except:
                    continue
            
            # APPROACH 3: Try to find by button position in the modal footer
            logging.info("Trying to find post button by modal footer position...")
            try:
                # Look for the share dialog (modal)
                share_dialog = None
                dialog_selectors = [
                    "//div[contains(@role, 'dialog')]",
                    "//div[contains(@class, 'share-creation-state')]",
                    "//div[contains(@class, 'share-box-creation-content')]"
                ]
                
                for selector in dialog_selectors:
                    try:
                        dialog = self.driver.find_element(By.XPATH, selector)
                        if (dialog.is_displayed()):
                            share_dialog = dialog
                            break
                    except:
                        continue
                
                if share_dialog:
                    # First try to find a footer inside the dialog
                    try:
                        footer = share_dialog.find_element(By.XPATH, ".//footer")
                        buttons = footer.find_elements(By.TAG_NAME, "button")
                        
                        # Usually the post button is the last button in the footer
                        if buttons and len(buttons) > 0:
                            # Try the last button first
                            post_button = buttons[-1]
                            if post_button.is_enabled() and post_button.is_displayed():
                                # Highlight it
                                try:
                                    self.driver.execute_script(
                                        "arguments[0].style.border='3px solid green'", post_button
                                    )
                                except:
                                    pass
                                self.driver.save_screenshot(f"found_post_button_in_footer_{int(time.time())}.png")
                                logging.info(f"Found post button as last button in modal footer")
                                return post_button
                    except:
                        pass
                        
                    # If no footer, look for the bottom-right corner of the dialog
                    buttons = share_dialog.find_elements(By.TAG_NAME, "button")
                    primary_buttons = []
                    
                    for button in buttons:
                        try:
                            classes = button.get_attribute("class") or ""
                            if "primary" in classes and button.is_enabled() and button.is_displayed():
                                primary_buttons.append(button)
                        except:
                            continue
                    
                    # The post button is usually a primary button
                    if primary_buttons:
                        post_button = primary_buttons[-1]  # take the last primary button
                        logging.info(f"Found post button as primary button in share dialog")
                        return post_button
            except Exception as e:
                logging.error(f"Error finding button in dialog: {str(e)}")
                
            # APPROACH 4: Last resort - attempt to bypass the default flow by using keyboard shortcut
            logging.info("Trying keyboard shortcut approach...")
            try:
                # First click in the share dialog to ensure focus
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.TAB)  # Tab to potentially focus the post button
                actions.perform()
                self.random_delay(0.5, 1)
                
                # Save screenshots to track focus state
                self.driver.save_screenshot(f"after_tab_keypress_{int(time.time())}.png")
                
                # Try Ctrl+Enter shortcut (commonly used for submitting forms)
                actions = ActionChains(self.driver)
                actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL)
                actions.perform()
                
                # Save after keyboard shortcut
                self.random_delay(1, 2)
                self.driver.save_screenshot(f"after_ctrl_enter_{int(time.time())}.png")
                
                # Check if we're redirected to feed (sign of success)
                current_url = self.driver.current_url
                if "feed" in current_url:
                    logging.info("Post seems successful after keyboard shortcut")
                    return True
            except Exception as keyboard_error:
                logging.error(f"Keyboard shortcut approach failed: {str(keyboard_error)}")
                
            # If all approaches fail, take a final screenshot and give up
            self.driver.save_screenshot(f"all_post_button_attempts_failed_{int(time.time())}.png")
            logging.error("All approaches to find post button failed")
            return None
                
        except Exception as e:
            logging.error(f"Error in advanced post button finder: {str(e)}")
            return None

    def post_to_linkedin_with_image(self, post_text, image_path=None):
        """Posts content to LinkedIn with an optional image."""
        logging.info("Posting to LinkedIn with image.")
        try:
            # Close overlapping elements
            self.close_overlapping_elements()
            
            # Handle any welcome screens that may appear
            self.handle_welcome_screens()

            # Navigate to feed to ensure we're in the right context
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(3, 5)

            # Handle any welcome screens that may appear after navigation
            self.handle_welcome_screens()
            
            # Multiple selector options to find the post button (same as post_to_linkedin method)
            post_button_selectors = [
                "//button[contains(., 'Start a post')]",
                "//button[contains(@class, 'share-box-feed-entry__trigger')]",
                "//button[contains(@data-control-name, 'share.open_share_box')]",
                "//div[contains(@class, 'share-box-feed-entry__trigger')]",
                "//span[text()='Start a post']/..",
                "//div[contains(@class, 'share-box')]"
            ]

            # Try each selector until one works
            start_post_button = None
            for selector in post_button_selectors:
                try:
                    self.driver.save_screenshot(f"looking_for_start_post_{int(time.time())}.png")
                    start_post_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logging.info(f"Found start post button with selector: {selector}")
                    break
                except:
                    continue

            if not start_post_button:
                logging.error("Could not find the 'Start a post' button using any selector")
                self.driver.save_screenshot(f"error_start_post_{int(time.time())}.png")
                return False
                
            # Click the button safely
            self.driver.execute_script("arguments[0].click();", start_post_button)
            self.random_delay(2, 3)
            
            # Multiple selectors for text area
            text_area_selectors = [
                "div[role='textbox']",
                "div.ql-editor",
                "div[data-placeholder='What do you want to talk about?']"
            ]
            
            # Try each selector until one works
            post_text_area = None
            for selector in text_area_selectors:
                try:
                    post_text_area = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
                    
            if not post_text_area:
                logging.error("Could not find the post text area using any selector")
                self.driver.save_screenshot(f"error_text_area_{int(time.time())}.png")
                return False
            
            # Clear any existing text and enter our content
            post_text_area.clear()
            post_text_area.click()
            
            # Type text in chunks to be more human-like
            chunks = self._split_text_into_chunks(post_text)
            for chunk in chunks:
                self.driver.execute_script(
                    "arguments[0].innerText += arguments[1]", post_text_area, chunk
                )
                self.random_delay(0.3, 0.7)
            
            # Attach image if available - Use multiple selectors for the media button
            if image_path and os.path.exists(image_path):
                try:
                    # Multiple selectors for the media/photo button
                    media_button_selectors = [
                        "//button[contains(@aria-label, 'Add a photo')]",
                        "//button[contains(@aria-label, 'media')]",
                        "//button[contains(@class, 'share-actions__primary-action')]//following-sibling::button",
                        "//button[contains(@class, 'artdeco-button')][contains(@class, 'share-creation-state__media-button')]",
                        "//button[contains(@class, 'share-creation-state__image-button')]",
                        "//button[contains(@class, 'gallery-control__button')]"
                    ]
                    
                    media_button = None
                    for selector in media_button_selectors:
                        try:
                            media_button = WebDriverWait(self.driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            break
                        except:
                            continue
                            
                    if media_button:
                        self.driver.execute_script("arguments[0].click();", media_button)
                        self.random_delay(1, 2)
                        
                        # Try to find the file input - also with multiple selectors
                        file_input_selectors = [
                            "//input[@type='file']",
                            "//input[contains(@accept, 'image')]",
                            "//div[contains(@class, 'share-box-file-input')]//input"
                        ]
                        
                        file_input = None
                        for selector in file_input_selectors:
                            try:
                                file_input = self.driver.find_element(By.XPATH, selector)
                                break
                            except:
                                continue
                        
                        if file_input:
                            file_input.send_keys(os.path.abspath(image_path))
                            logging.info(f"Image file path sent: {os.path.abspath(image_path)}")
                            self.random_delay(3, 5)  # Wait for upload
                            
                            # Wait for upload to complete - also with multiple indicators
                            try:
                                WebDriverWait(self.driver, 20).until_not(
                                    EC.presence_of_element_located((By.XPATH, 
                                        "//div[contains(@class, 'share-creation-state__progress-bar') or contains(@class, 'progress-bar')]"))
                                )
                                logging.info("Image upload completed successfully")
                            except:
                                logging.info("Progress bar not found or upload completed quickly")
                        else:
                            logging.error("Could not find the file input element")
                    else:
                        logging.error("Could not find the media/photo button using any selector")
                except Exception as img_error:
                    logging.error(f"Failed to attach image: {str(img_error)}")
                    # We'll continue without the image
            
            # After successful image upload, use enhanced post button selectors
            post_button_selectors = [
                "//button[contains(@class, 'share-actions__primary-action')]",
                "//button[contains(., 'Post')]",
                "//button[contains(@class, 'share-box_actions')]",
                "//button[contains(@class, 'share-actions__publish-button')]",
                "//div[contains(@class, 'share-box-footer__main-actions')]//button",
                "//button[contains(@class, 'share-actions__primary-action')][not(contains(@disabled, 'true'))]"
            ]
            
            # Try each selector until one works, with longer timeout
            post_button = None
            for selector in post_button_selectors:
                try:
                    # Take screenshot to debug button location
                    self.driver.save_screenshot(f"debug_finding_post_button_{int(time.time())}.png")
                    
                    # Use a longer wait time and add print of page source
                    post_button = WebDriverWait(self.driver, 12).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logging.info(f"Found post button with selector: {selector}")
                    break
                except:
                    continue
                
            if not post_button:
                # Additional fallback: try to find any enabled button that might be the post button
                try:
                    buttons = self.driver.find_elements(By.XPATH, "//button[not(contains(@disabled, 'true'))]")
                    for button in buttons:
                        button_text = button.text.lower()
                        if "post" in button_text or "share" in button_text or "publish" in button_text:
                            post_button = button
                            logging.info(f"Found post button by text: {button_text}")
                            break
                except:
                    pass
                
            if not post_button:
                logging.error("Could not find the 'Post' button using any selector")
                self.driver.save_screenshot(f"error_post_button_{int(time.time())}.png")
                
                # Print page source for debugging
                with open(f"page_source_{int(time.time())}.html", "w") as f:
                    f.write(self.driver.page_source)
                
                return False
                
            # Click post button with a delay to mimic human behavior
            self.random_delay(1, 2)
            logging.info("Attempting to click the post button")
            self.driver.execute_script("arguments[0].click();", post_button)
            
            # Verify post was successful by waiting for success toast or redirection
            post_success = False
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'artdeco-toast') or contains(@class, 'success')]"))
                )
                post_success = True
            except:
                # Check if we're back on the feed (another indicator of success)
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]"))
                    )
                    post_success = True
                except:
                    pass
            
            # Clean up temporary image file
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
                
            if post_success:
                logging.info("Post with image successful.")
                return True
            else:
                logging.info("Post may have been successful, but couldn't confirm with indicators.")
                return True  # Assume success if we got this far
                
        except Exception as e:
            logging.error(f"Failed to post to LinkedIn with image: {str(e)}", exc_info=True)
            # Clean up temporary image file in case of error
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
                
            # Take a screenshot for debugging
            self.driver.save_screenshot(f"post_with_image_error_{int(time.time())}.png")
            return False

    def check_duplicate_topic(self, topic):
        """Check if a topic has already been posted using semantic similarity."""
        try:
            with open("Topics_done.txt", "r") as file:
                done_topics = [line.strip() for line in file.readlines()]
            
            # First check for exact matches
            if topic in done_topics:
                logging.info(f"Topic '{topic}' is an exact match to a previously posted topic.")
                return True
                
            # Then check for high similarity using basic word matching
            topic_words = set(topic.lower().split())
            
            for done_topic in done_topics:
                done_topic_words = set(done_topic.lower().split())
                
                # Calculate Jaccard similarity
                intersection = len(topic_words.intersection(done_topic_words))
                union = len(topic_words.union(done_topic_words))
                
                similarity = intersection / union if union > 0 else 0
                
                # If similarity is above threshold, consider it a duplicate
                if similarity > 0.7:  # 70% similar words
                    logging.info(f"Topic '{topic}' is semantically similar to '{done_topic}' (similarity: {similarity:.2f})")
                    return True
                    
            # If we have Gemini API access, we can use it for semantic similarity as well
            try:
                if len(done_topics) > 0 and random.random() < 0.3:  # Only check 30% of the time to save API calls
                    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                    client = genai.GenerativeModel("gemini-1.5-flash")
                    
                    # Check against the last 10 topics
                    recent_topics = done_topics[-10:]
                    
                    prompt = f"""
                    I have a new topic: "{topic}"
                    
                    And these existing topics:
                    {", ".join(recent_topics)}
                    
                    Is my new topic semantically very similar to any of the existing topics? 
                    Answer with just YES or NO.
                    """
                    
                    response = client.generate_content(prompt)
                    if "YES" in response.text.upper():
                        logging.info(f"Gemini AI determined that '{topic}' is semantically similar to a previous topic")
                        return True
            except Exception as semantic_err:
                logging.error(f"Error checking semantic similarity: {str(semantic_err)}")
                    
            return False
        except Exception as e:
            logging.error(f"Error checking for duplicate topics: {str(e)}")
            return False

    def process_topics(self):
        """Processes the first topic from Topics.txt, posts it to LinkedIn, and updates the files accordingly."""
        try:
            with open("Topics.txt", "r") as file:
                topics = file.readlines()

            if not topics:
                logging.info("No topics to process.")
                return

            # Get the first topic
            topic = topics[0].strip()
            if not topic:
                logging.info("The first topic is empty.")
                return

            if self.check_duplicate_topic(topic):
                return

            post_text = self.generate_post_content(topic)
            image_path = self.generate_image(topic)
            if self.post_to_linkedin_with_image(post_text, image_path):
                with open("Topics_done.txt", "a") as done_file:
                    done_file.write(topic + "\n")
                logging.info(f"Topic posted and saved to Topics_done.txt: {topic}")

                # Remove the posted topic from Topics.txt
                with open("Topics.txt", "w") as file:
                    file.writelines(topics[1:])
                logging.info("First topic removed from Topics.txt.")
            else:
                logging.info(f"Failed to post topic: {topic}")
            self.random_delay(5, 10)

        except Exception as e:
            logging.error("An error occurred while processing topics.", exc_info=True)

    def process_topics_advanced(self):
        """Advanced processing of topics with smart scheduling and human-like behavior."""
        try:
            # Check if we should even post based on day and time
            if not self._should_post_now():
                logging.info("Skipping posting based on time schedule")
                return
                
            with open("Topics.txt", "r") as file:
                topics = file.readlines()

            if not topics:
                logging.info("No topics to process.")
                return

            # Select a topic - usually the first one, but sometimes random from the first 5
            use_random = random.random() < 0.2  # 20% chance to use random topic
            
            if use_random and len(topics) >= 5:
                topic_index = random.randint(0, min(4, len(topics)-1))
                topic = topics[topic_index].strip()
                logging.info(f"Randomly selected topic #{topic_index+1}: {topic}")
            else:
                topic = topics[0].strip()
                topic_index = 0
                
            if not topic:
                logging.info("Selected topic is empty.")
                return
                
            # Check for duplicate
            if self.check_duplicate_topic(topic):
                logging.info(f"Skipping duplicate topic: {topic}")
                # Remove the duplicate topic from Topics.txt
                with open("Topics.txt", "w") as file:
                    file.writelines([t for i, t in enumerate(topics) if i != topic_index])
                return
                
            # Sometimes browse the feed before posting to appear more natural
            if random.random() < 0.4:  # 40% chance
                self._browse_feed_naturally()
                
            # Generate post content
            post_text = self.generate_post_content(topic)
            
            # Decide whether to include an image based on topic and randomness
            image_worthy_keywords = ["visual", "design", "product", "technology", "innovation", "graphic"]
            topic_suggests_image = any(keyword in topic.lower() for keyword in image_worthy_keywords)
            
            include_image = random.random() < (0.6 if topic_suggests_image else 0.3)
            image_path = None
            
            if include_image:
                image_path = self.generate_image(topic)
                
            # Add occasional typos to seem more human
            if random.random() < 0.2:  # 20% chance
                post_text = self._add_realistic_typo(post_text)
                
            # Post to LinkedIn with or without an image
            success = False
            attempt_count = 0
            max_attempts = 3
            
            while not success and attempt_count < max_attempts:
                try:
                    if image_path and os.path.exists(image_path) and attempt_count == 0:
                        # Try with image only on first attempt
                        success = self.post_to_linkedin_with_image(post_text, image_path)
                    else:
                        # Fall back to no image on subsequent attempts
                        success = self.post_to_linkedin(post_text)
                except Exception as posting_error:
                    logging.error(f"Error during posting attempt #{attempt_count+1}: {str(posting_error)}")
                    success = False
                    
                if not success:
                    attempt_count += 1
                    logging.info(f"Post attempt #{attempt_count} failed, waiting before retry...")
                    self.random_delay(30, 60)  # Longer delay between attempts
                    
            if success:
                # Record the successful post
                with open("Topics_done.txt", "a") as done_file:
                    done_file.write(topic + "\n")
                logging.info(f"Topic posted and saved to Topics_done.txt: {topic}")

                # Remove the posted topic from Topics.txt
                with open("Topics.txt", "w") as file:
                    file.writelines([t for i, t in enumerate(topics) if i != topic_index])
                logging.info("Topic removed from Topics.txt.")
                
                # Post-posting activities to seem more natural
                
                # 1. Sometimes view your own post
                if random.random() < 0.3:
                    self._view_own_recent_post()
                    
                # 2. Engage with other content
                if random.random() < 0.7:  # 70% chance
                    engagement_count = random.randint(1, 5)  # Engage with 1-5 posts
                    self._engage_with_feed_content(engagement_count)
                    
                # 3. Randomly check notifications
                if random.random() < 0.4:
                    self._check_notifications()
                    
                # 4. Sometimes message connections
                if random.random() < 0.15:  # 15% chance
                    self._message_random_connections()
            else:
                logging.error(f"Failed to post topic after {max_attempts} attempts: {topic}")
                
            # Variable delay before ending session
            self.random_delay(5, 15)

        except Exception as e:
            logging.error(f"An error occurred while processing topics: {str(e)}", exc_info=True)
            
    def _should_post_now(self):
        """Determine if we should post based on day and time to appear more natural."""
        current_time = time.localtime()
        day_of_week = current_time.tm_wday  # 0-6 (Mon-Sun)
        hour = current_time.tm_hour
        
        # Avoid posting during nighttime hours (11 PM - 6 AM)
        if hour < 6 or hour >= 23:
            return False
            
        # Post less frequently on weekends
        if day_of_week >= 5:  # Saturday or Sunday
            return random.random() < 0.4  # 40% chance
            
        # Peak posting times get higher probability
        if hour in [8, 9, 12, 13, 17, 18]:  # Morning, lunch, end of workday
            return random.random() < 0.9  # 90% chance
            
        # Normal business hours
        if 7 <= hour <= 19:
            return random.random() < 0.7  # 70% chance
            
        # Evening hours
        return random.random() < 0.5  # 50% chance

    def _browse_feed_naturally(self):
        """Browse the feed in a natural way before posting."""
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(2, 5)
            
            # Scroll a random number of times
            scroll_count = random.randint(2, 8)
            for _ in range(scroll_count):
                self.driver.execute_script("window.scrollBy(0, window.innerHeight * 0.7)")
                self.random_delay(1, 4)
                
            # Sometimes like a post
            if random.random() < 0.4:
                try:
                    like_buttons = self.driver.find_elements(By.XPATH, 
                        "//button[contains(@aria-label, 'Like') or contains(@class, 'react-button__trigger')]")
                    if like_buttons:
                        rand_button = random.choice(like_buttons)
                        self.driver.execute_script("arguments[0].scrollIntoView();", rand_button)
                        self.random_delay(0.5, 1.5)
                        self.driver.execute_script("arguments[0].click();", rand_button)
                        self.random_delay(1, 3)
                except Exception as e:
                    logging.error(f"Error while trying to like a post: {str(e)}")
                    
        except Exception as e:
            logging.error(f"Error browsing feed naturally: {str(e)}")

    def _add_realistic_typo(self, text):
        """Add realistic typos to text to appear more human."""
        if len(text) < 20:
            return text
            
        words = text.split()
        if len(words) < 5:
            return text
            
        # Types of realistic typos:
        # 1. Missing letter
        # 2. Double letter
        # 3. Swapped letters
        # 4. Wrong capitalization
        
        typo_type = random.randint(1, 4)
        word_index = random.randint(5, min(len(words) - 1, 20))  # Not too early, not too late
        word = words[word_index]
        
        if len(word) < 4:
            return text  # Skip short words
            
        if typo_type == 1:  # Missing letter
            char_index = random.randint(1, len(word) - 2)
            new_word = word[:char_index] + word[char_index+1:]
        elif typo_type == 2:  # Double letter
            char_index = random.randint(1, len(word) - 2)
            new_word = word[:char_index] + word[char_index] + word[char_index:]
        elif typo_type == 3:  # Swapped letters
            char_index = random.randint(1, len(word) - 2)
            new_word = word[:char_index] + word[char_index+1] + word[char_index] + word[char_index+2:]
        else:  # Wrong capitalization
            if word[0].isupper():
                new_word = word[0].lower() + word[1:]
            else:
                new_word = word[0].upper() + word[1:]
                
        words[word_index] = new_word
        return " ".join(words)

    def search_connections(self, keywords):
        """Search for connections based on keywords."""
        try:
            self.driver.get("https://www.linkedin.com/mynetwork/")
            self.random_delay(2, 4)
            
            # Click on connections
            connections_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/mynetwork/connections/')]"))
            )
            connections_button.click()
            self.random_delay(2, 4)
            
            # Search for connections
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search by name']"))
            )
            
            for char in keywords:
                search_input.send_keys(char)
                self.random_delay(0.1, 0.2)
            
            search_input.send_keys(Keys.RETURN)
            self.random_delay(3, 5)
            
            # Collect connection profiles
            connections = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'reusable-search__entity-result-list')]/li"))
            )
            
            connection_profiles = []
            for conn in connections[:5]:  # Limit to first 5 connections
                try:
                    name = conn.find_element(By.XPATH, ".//span[@aria-hidden='true']").text
                    profile_link = conn.find_element(By.XPATH, ".//a[contains(@href, '/in/')]").get_attribute("href")
                    connection_profiles.append({"name": name, "profile_link": profile_link})
                except:
                    continue
                    
            return connection_profiles
        except Exception as e:
            logging.error(f"Error searching connections: {str(e)}")
            return []

    def generate_personalized_message(self, connection_name, connection_info=""):
        """Generate a personalized message for a connection using Gemini API."""
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            client = genai.GenerativeModel("gemini-1.5-flash")  # Updated model
            
            prompt = f"""
            Generate a personalized LinkedIn message to {connection_name}.
            The message should be friendly, professional, and not too long (under 200 characters).
            It should not be too pushy or sales-focused, but rather aim to start a genuine conversation.
            
            Additional information about the connection: {connection_info}
            """
            
            response = client.generate_content(prompt)
            message = response.text.strip().strip('"')
            
            return message
        except Exception as e:
            logging.error(f"Error generating personalized message: {str(e)}")
            return f"Hi {connection_name}, hope you're doing well! I'd love to connect and learn more about your work."

    def send_message_to_connection(self, profile_link, message):
        """Send a message to a connection."""
        try:
            self.driver.get(profile_link)
            self.random_delay(2, 4)
            
            # Find and click message button
            message_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Message') or contains(@aria-label, 'Message')]"))
            )
            message_button.click()
            self.random_delay(2, 3)
            
            # Enter message
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            
            for char in message:
                message_input.send_keys(char)
                self.random_delay(0.05, 0.1)
            
            # Send message
            send_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'msg-form__send-button')]"))
            )
            send_button.click()
            
            logging.info(f"Message sent to profile: {profile_link}")
            return True
        except Exception as e:
            logging.error(f"Error sending message to {profile_link}: {str(e)}")
            return False

    def generate_comment_based_on_content(self, post_text):
        """Generates a comment based on the content of a post using Gemini AI."""
        logging.info("Generating comment based on post content.")
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            client = genai.GenerativeModel("gemini-1.5-flash")  # Updated model

            # Truncate post_text if it's too long
            truncated_text = post_text[:500] + "..." if len(post_text) > 500 else post_text
            
            prompt = f"""
            Generate a thoughtful, professional comment for this LinkedIn post:
            "{truncated_text}"
            
            The comment should:
            - Be between 50-100 characters
            - Sound natural and conversational
            - Add value to the discussion
            - Be specific to the post content
            - Not use generic phrases like "Great post!"
            - Not sound like it was written by AI
            """
            
            response = client.generate_content(prompt)
            
            if response.text:
                # Clean up the comment
                comment = response.text.strip().strip('"')
                # Remove markdown if any
                comment = self.remove_markdown(comment)
                return comment
            else:
                return "This is a really insightful perspective. Thanks for sharing!"
        except Exception as e:
            logging.error(f"Error generating comment: {str(e)}", exc_info=True)
            return "This is a really insightful perspective. Thanks for sharing!"

    def _reset_post_modal(self):
        """Reset the post creation modal if it gets stuck."""
        try:
            # Try to find and click the cancel button
            cancel_button_selectors = [
                "//button[contains(@class, 'cancel-button')]",
                "//button[contains(@class, 'artdeco-modal__dismiss')]",
                "//button[contains(@aria-label, 'Dismiss')]"
            ]
            
            for selector in cancel_button_selectors:
                try:
                    cancel_btn = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].click();", cancel_btn)
                    self.random_delay(1, 2)
                    return True
                except:
                    continue
                    
            # If cancel button not found, try refreshing the page
            self.driver.refresh()
            self.random_delay(3, 5)
            return True
        except Exception as e:
            logging.error(f"Error resetting post modal: {str(e)}")
            return False

    def _view_own_recent_post(self):
        """View your own recent post to simulate natural behavior."""
        try:
            logging.info("Viewing own recent post")
            # Navigate to profile page
            self.driver.get("https://www.linkedin.com/in/me/")
            self.random_delay(2, 4)
            
            # Look for the recent activity section or posts
            try:
                posts = self.driver.find_elements(By.XPATH, 
                    "//div[contains(@class, 'feed-shared-update-v2') or contains(@class, 'occludable-update')]")
                
                if posts and len(posts) > 0:
                    # Click on the first (most recent) post
                    self.driver.execute_script("arguments[0].scrollIntoView();", posts[0])
                    self.random_delay(1, 2)
                    
                    # Try to find and click on "See more" or the post content
                    try:
                        see_more = posts[0].find_element(By.XPATH, 
                            ".//button[contains(@class, 'feed-shared-inline-show-more-text')]")
                        self.driver.execute_script("arguments[0].click();", see_more)
                    except:
                        # If no "See more" button, just click the post content area
                        try:
                            content_area = posts[0].find_element(By.XPATH, 
                                ".//div[contains(@class, 'feed-shared-update-v2__description')]")
                            self.driver.execute_script("arguments[0].click();", content_area)
                        except:
                            pass
                    
                    # Mimic reading time
                    self.random_delay(3, 8)
                    
                    # Scroll down a bit to view comments
                    self.driver.execute_script("window.scrollBy(0, 300);")
                    self.random_delay(2, 4)
                    
                    return True
                else:
                    logging.info("No recent posts found")
                    return False
            except Exception as e:
                logging.error(f"Error finding recent posts: {str(e)}")
                return False
                
        except Exception as e:
            logging.error(f"Error viewing own recent post: {str(e)}")
            return False

    def _message_random_connections(self):
        """Send messages to random connections."""
        try:
            # Get random keywords for searching connections
            search_terms = ["work", "project", "team", "business", "tech", "development", "marketing", "design"]
            keyword = random.choice(search_terms)
            
            # Search for connections
            connections = self.search_connections(keyword)
            
            if connections and len(connections) > 0:
                # Select random connection (max 2)
                message_count = min(len(connections), 2)
                selected_connections = random.sample(connections, message_count)
                
                for connection in selected_connections:
                    message = self.generate_personalized_message(connection["name"])
                    self.send_message_to_connection(connection["profile_link"], message)
                    self.random_delay(3, 5)
                    
                logging.info(f"Sent messages to {message_count} connections")
                return True
            else:
                logging.info("No connections found to message")
                return False
        except Exception as e:
            logging.error(f"Error messaging random connections: {str(e)}")
            return False

    def _check_notifications(self):
        """Check notifications to mimic human behavior."""
        try:
            self.driver.get("https://www.linkedin.com/notifications/")
            self.random_delay(2, 4)
            
            # Scroll down a bit
            for _ in range(random.randint(1, 3)):
                self.driver.execute_script("window.scrollBy(0, 400)")
                self.random_delay(1, 3)
                
            # Sometimes click on a notification
            if random.random() < 0.3:
                try:
                    notifications = self.driver.find_elements(By.XPATH, 
                        "//div[contains(@class, 'nt-card')]//a")
                    
                    if notifications and len(notifications) > 0:
                        random_notification = random.choice(notifications)
                        self.driver.execute_script("arguments[0].click();", random_notification)
                        self.random_delay(3, 5)
                        
                        # Go back
                        self.driver.back()
                        self.random_delay(1, 2)
                except:
                    pass
                    
            return True
        except Exception as e:
            logging.error(f"Error checking notifications: {str(e)}")
            return False

    def _engage_with_feed_content(self, count=3):
        """Engage with content in feed (like, comment)."""
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(2, 4)
            
            # Find feed posts
            posts = self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'feed-shared-update-v2')]")
            
            if not posts or len(posts) == 0:
                logging.info("No feed posts found")
                return False
                
            # Limit to available posts or requested count
            engagement_count = min(len(posts), count)
            
            for i in range(engagement_count):
                try:
                    # Scroll to the post
                    self.driver.execute_script("arguments[0].scrollIntoView();", posts[i])
                    self.random_delay(1, 3)
                    
                    # Like with 60% probability
                    if random.random() < 0.6:
                        try:
                            like_button = posts[i].find_element(By.XPATH, 
                                ".//button[contains(@aria-label, 'Like') or contains(@class, 'react-button__trigger')]")
                            self.driver.execute_script("arguments[0].click();", like_button)
                            self.random_delay(1, 2)
                        except:
                            pass
                    
                    # Comment with 20% probability
                    if random.random() < 0.2:
                        try:
                            # Get post text
                            post_text = posts[i].find_element(By.XPATH, 
                                ".//div[contains(@class, 'feed-shared-update-v2__description')]").text
                            
                            # Generate comment
                            comment = self.generate_comment_based_on_content(post_text)
                            
                            # Click comment button
                            comment_button = posts[i].find_element(By.XPATH, 
                                ".//button[contains(@aria-label, 'Comment')]")
                            self.driver.execute_script("arguments[0].click();", comment_button)
                            self.random_delay(1, 2)
                            
                            # Enter comment
                            comment_box = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and contains(@aria-label, 'Add a comment')]"))
                            )
                            
                            # Type comment character by character
                            for char in comment:
                                comment_box.send_keys(char)
                                self.random_delay(0.03, 0.1)
                            
                            self.random_delay(1, 2)
                            
                            # Post comment
                            post_comment_button = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'comments-comment-box__submit-button')]"))
                            )
                            post_comment_button.click()
                            self.random_delay(2, 3)
                        except Exception as comment_error:
                            logging.error(f"Error commenting on post: {str(comment_error)}")
                            
                    # Add random delay between post interactions
                    self.random_delay(2, 4)
                            
                except Exception as post_error:
                    logging.error(f"Error interacting with post #{i+1}: {str(post_error)}")
                    continue
                    
            return True
        except Exception as e:
            logging.error(f"Error engaging with feed content: {str(e)}")
            return False

    def _maintain_session(self):
        """Periodically visit pages to maintain the login session."""
        try:
            # Get a random LinkedIn page to maintain the session
            random_pages = [
                "https://www.linkedin.com/feed/",
                "https://www.linkedin.com/mynetwork/",
                "https://www.linkedin.com/jobs/",
                "https://www.linkedin.com/notifications/"
            ]
            
            # Visit a random page
            self.driver.get(random.choice(random_pages))
            self.random_delay(2, 4)
            
            # Scroll a bit
            self.driver.execute_script("window.scrollBy(0, 300);")
            self.random_delay(1, 3)
            
            logging.info("Session maintained successfully")
            return True
        except Exception as e:
            logging.error(f"Error maintaining session: {str(e)}")
            return False

    def _clean_cookies_periodically(self):
        """Clean non-essential cookies periodically to avoid fingerprinting."""
        try:
            # Get all cookies
            all_cookies = self.driver.get_cookies()
            
            # Identify essential LinkedIn cookies (keep these)
            essential_cookies = [
                "li_at",  # LinkedIn authentication
                "JSESSIONID",  # Session ID
                "li_mc",  # Member cookie
                "lidc",  # LinkedIn Data Cookie
            ]
            
            # Remove some non-essential tracking cookies (but keep essential ones)
            for cookie in all_cookies:
                if not any(essential in cookie['name'] for essential in essential_cookies):
                    # Only remove a subset of cookies to avoid detection (50% chance)
                    if random.random() < 0.5:
                        try:
                            self.driver.delete_cookie(cookie['name'])
                        except:
                            pass
                            
            logging.info("Cleaned non-essential cookies")
            return True
        except Exception as e:
            logging.error(f"Error cleaning cookies: {str(e)}")
            return False

    def verify_latest_post(self):
        """Verifies if the latest post is visible on your profile."""
        try:
            print(f"{Fore.CYAN}Checking your LinkedIn profile for the latest post...{Style.RESET_ALL}")
            
            # Go to profile activity page
            self.driver.get("https://www.linkedin.com/in/me/recent-activity/shares/")
            self.random_delay(3, 5)
            
            # Check if any posts exist
            try:
                posts = self.driver.find_elements(By.XPATH, 
                    "//div[contains(@class, 'feed-shared-update-v2') or contains(@class, 'occludable-update')]")
                
                if posts and len(posts) > 0:
                    print(f"{Fore.GREEN}Found {len(posts)} recent posts on your profile.{Style.RESET_ALL}")
                    
                    # Get the most recent post text
                    try:
                        post_text = posts[0].find_element(By.XPATH, 
                            ".//div[contains(@class, 'feed-shared-update-v2__description')]").text
                        
                        print(f"{Fore.GREEN}Most recent post:{Style.RESET_ALL}")
                        print(f"{post_text[:150]}...")
                        
                        # Save screenshot of the post
                        self.driver.save_screenshot(f"latest_post_{int(time.time())}.png")
                        print(f"{Fore.CYAN}Screenshot saved of your latest post.{Style.RESET_ALL}")
                        
                        # Like your own post to increase visibility (sometimes helps)
                        try:
                            like_button = posts[0].find_element(By.XPATH, 
                                ".//button[contains(@aria-label, 'Like') or contains(@class, 'react-button__trigger')]")
                            self.driver.execute_script("arguments[0].click();", like_button)
                            print(f"{Fore.GREEN}Liked your own post to boost visibility.{Style.RESET_ALL}")
                        except:
                            pass
                        
                        return True
                    except:
                        print(f"{Fore.YELLOW}Found posts but couldn't extract the text.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No posts found on your profile. Your post may be delayed or rejected by LinkedIn.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}LinkedIn sometimes has delayed processing for new posts.{Style.RESET_ALL}")
                    
                    # Take a screenshot of the activity page
                    self.driver.save_screenshot(f"no_posts_found_{int(time.time())}.png")
                    return False
                    
            except Exception as e:
                print(f"{Fore.RED}Error checking posts: {str(e)}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}Failed to verify latest post: {str(e)}{Style.RESET_ALL}")
            return False

    def _split_text_into_chunks(self, text, avg_chunk_size=30):
        """
        Split text into random-sized chunks to simulate human typing.
        
        Args:
            text (str): The text to split
            avg_chunk_size (int): Average size of each chunk
            
        Returns:
            list: List of text chunks
        """
        if not text:
            return []
            
        # Preserve paragraph breaks
        paragraphs = text.split('\n\n')
        chunks = []
        
        for paragraph in paragraphs:
            # If paragraph is short enough, keep it intact
            if len(paragraph) <= avg_chunk_size * 1.5:
                chunks.append(paragraph + ('\n\n' if paragraph != paragraphs[-1] else ''))
                continue
                
            # For longer paragraphs, split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            current_chunk = ""
            
            for sentence in sentences:
                # If sentence is longer than the chunk size, split by words
                if len(sentence) > avg_chunk_size * 2:
                    words = sentence.split()
                    for word in words:
                        current_chunk += word + " "
                        # Randomize chunk size for more human-like typing
                        target_size = avg_chunk_size * random.uniform(0.7, 1.3)
                        if len(current_chunk) >= target_size:
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
                else:
                    # If adding this sentence exceeds target chunk size, start a new chunk
                    if len(current_chunk) + len(sentence) > avg_chunk_size * 1.5:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + " "
                    else:
                        current_chunk += sentence + " "
                        
            # Add any remaining text
            if current_chunk:
                chunks.append(current_chunk.strip() + ('\n\n' if paragraph != paragraphs[-1] else ''))
        
        return chunks

    def generate_topic_title(self):
        """Generate a fresh topic title using Gemini AI."""
        logging.info("Generating new topic title")
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")
            client = genai.GenerativeModel("gemini-1.5-flash")
            
            # Get current date for context
            current_date = time.strftime("%B %d, %Y")
            
            # Get topics already done to avoid duplicates
            done_topics = []
            try:
                with open("Topics_done.txt", "r") as file:
                    done_topics = [line.strip() for line in file.readlines()]
            except:
                pass
                
            # Generate prompt with current trends
            trending_topics = self._get_trending_topics()
            trending_context = ""
            if trending_topics:
                trending_context = f"Consider these current trending topics if relevant: {', '.join(trending_topics[:3])}."
            
            prompt = f"""
            Today is {current_date}. Generate a professional, engaging LinkedIn post title about technology, business, or leadership. 

            The title should:
            1. Be specific and actionable
            2. Follow the pattern "How to..." or "The role of..." or "The impact of..." or "The future of..."
            3. Be 5-10 words in length
            4. Focus on a topic that would interest professionals
            5. NOT contain hashtags or special characters
            
            {trending_context}
            
            Make sure the title is NOT similar to any of these already used titles:
            {', '.join(done_topics[-10:]) if done_topics else 'No previous titles'}
            """
            
            # Use structured generation
            messages = [{"role": "user", "parts": [prompt]}]
            
            generation_config = {
                "temperature": 0.8,  # More creativity
                "top_p": 0.95,
                "top_k": 40,
            }
            
            response = client.generate_content(
                messages,
                generation_config=generation_config
            )
            
            if response.text:
                # Clean up the title
                topic_title = response.text.strip().strip('"\'').strip()
                
                # Ensure it starts with a capital letter
                if topic_title and len(topic_title) > 0:
                    topic_title = topic_title[0].upper() + topic_title[1:]
                    
                    # Add to Topics.txt
                    with open("Topics.txt", "a") as file:
                        file.write(topic_title + "\n")
                    
                    logging.info(f"Generated and saved new topic title: {topic_title}")
                    return topic_title
            
            return "How to leverage AI for business growth"
        except Exception as e:
            logging.error(f"Failed to generate topic title: {str(e)}", exc_info=True)
            return "How to leverage AI for business growth"

    def analyze_error_image(self, image_path):
        """Analyze error images to identify UI elements that might have changed."""
        try:
            print(f"{Fore.CYAN}Analyzing error image at {image_path}...{Style.RESET_ALL}")
            
            # Check if the file exists
            if not os.path.exists(image_path):
                print(f"{Fore.RED}Error image not found: {image_path}{Style.RESET_ALL}")
                return
                
            # Basic image analysis - check for key LinkedIn UI elements
            # Open image in browser for visual inspection
            self.driver.get(f"file://{os.path.abspath(image_path)}")
            self.random_delay(1, 2)
            
            print(f"{Fore.GREEN}Image loaded for visual inspection.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Looking for common UI elements...{Style.RESET_ALL}")
            
            # Capturing page source from the current state when error occurred
            state_analysis = """
            Based on the error screenshot, here's what might be happening:
            
            1. Post modal present? Look for a large centered dialog box
            2. Text entered properly? Check if text is visible in the editor
            3. Post button visible? Look for a blue "Post" button at the bottom right
            4. Any error messages? Look for red text or warning icons
            5. LinkedIn layout changed? Compare to current LinkedIn UI
            
            Common fixes:
            - Try refreshing the page before posting
            - Check if LinkedIn has updated their UI elements
            - Make sure you're not rate limited (too many posts in a short time)
            - Try posting at a different time of day
            - Check if your LinkedIn account has any restrictions
            """
            
            print(state_analysis)
            
            if questionary.confirm("Would you like to modify web element selectors?", default=False).ask():
                print(f"{Fore.YELLOW}Current selectors for post button:{Style.RESET_ALL}")
                selectors = [
                    "//button[contains(@class, 'share-actions__primary-action')]",
                    "//button[contains(text(), 'Post')]",
                    "//button[text()='Post']", 
                    "//button[contains(@class, 'share-box_actions')]"
                ]
                
                for i, selector in enumerate(selectors):
                    print(f"{i+1}. {selector}")
                    
                print(f"\n{Fore.YELLOW}You can add new selectors in the browser.py file.{Style.RESET_ALL}")
            
            return True
        except Exception as e:
            print(f"{Fore.RED}Error analyzing image: {str(e)}{Style.RESET_ALL}")
            return False

    def handle_welcome_screens(self):
        """Handle any welcome back screens or overlays that appear after login."""
        try:
            # Take screenshot for debugging
            self.driver.save_screenshot(f"welcome_screen_debug_{int(time.time())}.png")
            
            # Check for "Welcome back" screen - multiple possible selectors
            welcome_selectors = [
                "//button[contains(@class, 'artdeco-modal__dismiss')]",
                "//button[contains(@aria-label, 'Dismiss')]",
                "//button[contains(@aria-label, 'Close')]",
                "//button[contains(text(), 'Continue')]",
                "//button[contains(text(), 'Get started')]",
                "//button[contains(text(), 'Skip')]",
                "//div[contains(@class, 'welcome-modal')]//button",
                "//h2[contains(text(), 'Welcome back')]/following::button",
                "//h2[contains(text(), 'welcome back')]/following::button"
            ]
            
            for selector in welcome_selectors:
                try:
                    welcome_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logging.info(f"Found welcome screen dismiss button with selector: {selector}")
                    self.random_delay(0.5, 1.5)
                    welcome_button.click()
                    logging.info("Clicked welcome screen dismiss button")
                    
                    # Verify it was dismissed
                    self.random_delay(1, 2)
                    self.driver.save_screenshot(f"after_welcome_dismiss_{int(time.time())}.png")
                    return True
                except:
                    continue
                    
            # Special case: Check if we're on a specific welcome page that requires navigation
            page_source = self.driver.page_source.lower()
            if "welcome back" in page_source or "welcome to linkedin" in page_source:
                logging.info("Detected welcome page based on page content")
                
                # Try to navigate directly to feed to bypass welcome screen
                self.driver.get("https://www.linkedin.com/feed/")
                self.random_delay(3, 5)
                logging.info("Navigated directly to feed to bypass welcome screen")
                return True
                
            return False
        except Exception as e:
            logging.error(f"Error handling welcome screens: {str(e)}")
            return False

    def detect_linkedin_ui_elements(self):
        """Advanced detection of LinkedIn UI elements to adapt to UI changes."""
        try:
            print(f"{Fore.CYAN}Detecting LinkedIn UI elements...{Style.RESET_ALL}")
            
            # Navigate to feed
            self.driver.get("https://www.linkedin.com/feed/")
            self.random_delay(3, 5)
            
            # Save screenshot and HTML for reference
            self.driver.save_screenshot(f"linkedin_ui_detection_{int(time.time())}.png")
            
            # Use JavaScript to identify key UI components
            ui_data = self.driver.execute_script("""
                return {
                    # Start Post area detection
                    startPostButton: {
                        byText: Boolean(Array.from(document.querySelectorAll('*'))
                                    .find(el => el.textContent.includes('Start a post'))),
                        byClass: Boolean(document.querySelector('[class*="share-box"]')),
                        byRole: Boolean(document.querySelector('[role="button"][aria-label*="post"]'))
                    },
                    
                    # Post dialog/modal detection
                    postDialog: {
                        byRole: Boolean(document.querySelector('[role="dialog"]')),
                        byClass: Boolean(document.querySelector('[class*="share-creation-state"]')),
                    },
                    
                    # Post button detection within dialog
                    postButton: {
                        byText: Boolean(Array.from(document.querySelectorAll('button'))
                                    .find(el => el.textContent.trim().toLowerCase() === 'post')),
                        byPrimaryClass: Boolean(document.querySelector('button[class*="primary"]')),
                        byFooterPosition: Boolean(document.querySelector('footer button:last-child'))
                    },
                    
                    # Other LinkedIn UI markers
                    feedItems: document.querySelectorAll('[data-id]').length,
                    navBar: Boolean(document.querySelector('nav')),
                    notificationButton: Boolean(document.querySelector('[aria-label*="notification"]')),
                    
                    # Detect any error messages or warnings
                    errorMessages: Array.from(document.querySelectorAll('*'))
                        .filter(el => {
                            const text = el.textContent;
                            return text && 
                                (text.includes('error') || text.includes('failed') || 
                                 text.includes('unable') || text.includes('not working'));
                        }).map(el => el.textContent.trim())
                };
            """)
            
            # Output UI detection results
            print(f"\n{Fore.GREEN}LinkedIn UI Detection Results:{Style.RESET_ALL}")
            
            print(f"\nStart Post Element:")
            print(f"  By Text: {'✅ Found' if ui_data['startPostButton']['byText'] else '❌ Not found'}")
            print(f"  By Class: {'✅ Found' if ui_data['startPostButton']['byClass'] else '❌ Not found'}")
            print(f"  By Role: {'✅ Found' if ui_data['startPostButton']['byRole'] else '❌ Not found'}")
            
            print(f"\nPost Dialog:")
            print(f"  By Role: {'✅ Found' if ui_data['postDialog']['byRole'] else '❌ Not found'}")
            print(f"  By Class: {'✅ Found' if ui_data['postDialog']['byClass'] else '❌ Not found'}")
            
            print(f"\nPost Button:")
            print(f"  By Text: {'✅ Found' if ui_data['postButton']['byText'] else '❌ Not found'}")
            print(f"  By Primary Class: {'✅ Found' if ui_data['postButton']['byPrimaryClass'] else '❌ Not found'}")
            print(f"  By Footer Position: {'✅ Found' if ui_data['postButton']['byFooterPosition'] else '❌ Not found'}")
            
            print(f"\nOther UI Elements:")
            print(f"  Feed Items: {ui_data['feedItems']}")
            print(f"  Navigation Bar: {'✅ Found' if ui_data['navBar'] else '❌ Not found'}")
            print(f"  Notification Button: {'✅ Found' if ui_data['notificationButton'] else '❌ Not found'}")
            
            if ui_data['errorMessages'] and len(ui_data['errorMessages']) > 0:
                print(f"\n{Fore.YELLOW}Detected Error Messages:{Style.RESET_ALL}")
                for msg in ui_data['errorMessages']:
                    print(f"  - {msg[:100]}" + ("..." if len(msg) > 100 else ""))
            
            # Generate recommendations based on findings
            print(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
            
            if not ui_data['startPostButton']['byText'] and not ui_data['startPostButton']['byClass']:
                print(f"⚠️ The 'Start a post' button wasn't detected. LinkedIn UI may have changed significantly.")
                print(f"   Try running in non-headless mode to manually view the current UI.")
            
            if not ui_data['postButton']['byText'] and not ui_data['postButton']['byPrimaryClass']:
                print(f"⚠️ The 'Post' button wasn't detected. This may cause posting failures.")
                print(f"   Consider updating the selectors or trying a different approach.")
            
            if ui_data['errorMessages'] and len(ui_data['errorMessages']) > 0:
                print(f"⚠️ Error messages detected on the page. You may be rate-limited or there might be other issues.")
                print(f"   Consider waiting for some time before trying again.")
            
            return ui_data
        except Exception as e:
            print(f"{Fore.RED}Error detecting LinkedIn UI: {str(e)}{Style.RESET_ALL}")
            return None

def check_and_handle_lock_file():
    """Check if the lock file exists and handle it appropriately."""
    if os.path.exists("linkedin_bot.lock"):
        try:
            # Read the lock file to get the PID
            with open("linkedin_bot.lock", "r") as lock_file:
                content = lock_file.read()
                pid_match = re.search(r"PID: (\d+)", content)
                
                if pid_match:
                    pid = int(pid_match.group(1))
                    
                    # Check if the process is still running on Linux/Mac
                    if os.name == 'posix':
                        try:
                            # Sending signal 0 is a way to check if process exists
                            os.kill(pid, 0)
                            # Process exists
                            print(f"{Fore.YELLOW}Another instance (PID: {pid}) appears to be running.{Style.RESET_ALL}")
                            
                            # Ask if user wants to force override
                            force_override = input(f"{Fore.CYAN}Force start anyway? This could cause issues if another instance is running. (y/n): {Style.RESET_ALL}").lower() == 'y'
                            
                            if not force_override:
                                print(f"{Fore.YELLOW}Exiting. If you're sure no other instance is running, delete the lock file: {Style.RESET_ALL}linkedin_bot.lock")
                                sys.exit(0)
                        except OSError:
                            # Process doesn't exist, lock file is stale
                            print(f"{Fore.YELLOW}Found stale lock file. The process is no longer running. Removing lock file.{Style.RESET_ALL}")
                    else:
                        # On Windows, we'll use the creation time as a heuristic
                        lock_time = os.path.getmtime("linkedin_bot.lock")
                        if time.time() - lock_time < 10800:  # 3 hours in seconds
                            # Ask if user wants to force override
                            force_override = input(f"{Fore.CYAN}Another instance might be running. Force start anyway? (y/n): {Style.RESET_ALL}").lower() == 'y'
                            
                            if not force_override:
                                print(f"{Fore.YELLOW}Exiting. If you're sure no other instance is running, delete the lock file: {Style.RESET_ALL}linkedin_bot.lock")
                                sys.exit(0)
                else:
                    print(f"{Fore.YELLOW}Lock file found but no PID information. It may be corrupted.{Style.RESET_ALL}")
                    force_override = input(f"{Fore.CYAN}Delete lock file and continue? (y/n): {Style.RESET_ALL}").lower() == 'y'
                    if not force_override:
                        sys.exit(0)
        except Exception as e:
            print(f"{Fore.YELLOW}Error reading lock file: {str(e)}. Will replace it.{Style.RESET_ALL}")
            
        # If we got here, we're removing the lock file
        os.remove("linkedin_bot.lock")
        
    # Create new lock file with current PID
    with open("linkedin_bot.lock", "w") as lock_file:
        lock_file.write(f"Process started at {time.ctime()}\nPID: {os.getpid()}")

def cleanup():
    """Clean up resources when the program exits."""
    try:
        # Remove lock file
        if os.path.exists("linkedin_bot.lock"):
            os.remove("linkedin_bot.lock")
            print(f"{Fore.GREEN}Lock file removed.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error removing lock file: {str(e)}{Style.RESET_ALL}")

# Use atexit to register the cleanup function
import atexit
atexit.register(cleanup)

if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description="LinkedIn Automation Bot")
        parser.add_argument("--force", action="store_true", help="Force posting regardless of time schedule")
        parser.add_argument("--no-verify", action="store_true", help="Disable device verification detection")
        args = parser.parse_args()
        
        # Check and handle lock file
        check_and_handle_lock_file()
        
        print(f"{Fore.GREEN}=== LinkedIn Automation Bot ==={Style.RESET_ALL}")
        print(f"{Fore.CYAN}Initializing browser...{Style.RESET_ALL}")
        
        # Initialize bot
        bot = LinkedInBot()
        
        # Clean cookies periodically (40% chance on startup)
        if random.random() < 0.4:
            bot._clean_cookies_periodically()
            
        # Load topics
        try:
            with open("Topics.txt", "r") as file:
                topics = file.readlines()
            
            if not topics:
                print(f"{Fore.RED}No topics found in Topics.txt. Please add topics first.{Style.RESET_ALL}")
                sys.exit(0)
                
            # Display available topics
            print(f"\n{Fore.GREEN}Available Topics:{Style.RESET_ALL}")
            for i, topic in enumerate(topics[:5]):  # Show first 5 topics
                print(f"{i+1}. {topic.strip()}")
            if len(topics) > 5:
                print(f"...and {len(topics)-5} more")
            print()
            
            # Create menu
            while True:
                choice = questionary.select(
                    "What would you like to do?",
                    choices=[
                        "Post with image",
                        "Post without image",
                        "Generate new topic title",
                        "Search topics",
                        "Browse all topics",
                        "Verify latest post",
                        "Check trending topics",
                        "View LinkedIn feed",
                        "Analyze error images",
                        "Clear welcome screens",  # Fixed comma here
                        "View HTML Source",       # New debug option
                        "Exit"
                    ]
                ).ask()
                
                if choice == "Exit":
                    break
                
                elif choice == "Check trending topics":
                    print(f"\n{Fore.CYAN}Fetching trending topics...{Style.RESET_ALL}")
                    trending = bot._get_trending_topics()
                    if trending:
                        print(f"\n{Fore.GREEN}Trending Topics:{Style.RESET_ALL}")
                        for i, topic in enumerate(trending):
                            print(f"{i+1}. {topic}")
                    else:
                        print(f"{Fore.YELLOW}No trending topics found.{Style.RESET_ALL}")
                    print()
                    
                elif choice == "View LinkedIn feed":
                    print(f"\n{Fore.CYAN}Opening LinkedIn feed...{Style.RESET_ALL}")
                    bot._browse_feed_naturally()
                    print(f"{Fore.GREEN}Done browsing feed.{Style.RESET_ALL}\n")
                
                elif choice == "Verify latest post":
                    print(f"\n{Fore.CYAN}Verifying your latest post...{Style.RESET_ALL}")
                    bot.verify_latest_post()
                    print()

                elif choice == "Detect LinkedIn UI":
                    print(f"\n{Fore.CYAN}Running LinkedIn UI detector...{Style.RESET_ALL}")
                    ui_data = bot.detect_linkedin_ui_elements()
                    print()

                elif choice == "Clear welcome screens":
                    print(f"{Fore.CYAN}Checking for and clearing welcome screens...{Style.RESET_ALL}")
                    if bot.handle_welcome_screens():
                        print(f"{Fore.GREEN}Successfully cleared welcome screens.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}No welcome screens detected or unable to clear them.{Style.RESET_ALL}")
                    print()

                elif choice == "Post with image" or choice == "Post without image":
                    # Let user select a topic or use the first one
                    use_first = questionary.confirm("Use the first topic from the list?", default=True).ask()
                    
                    if use_first:
                        topic = topics[0].strip()
                        topic_index = 0
                    else:
                        # Allow user to choose a topic index
                        topic_index = questionary.select(
                            "Select a topic:",
                            choices=[f"{i+1}. {topic.strip()}" for i, topic in enumerate(topics[:10])]
                        ).ask()
                        topic_index = int(topic_index.split(".")[0]) - 1
                        topic = topics[topic_index].strip()
                    
                    print(f"\n{Fore.CYAN}Selected topic: {topic}{Style.RESET_ALL}")
                    
                    # Check for duplicate
                    if bot.check_duplicate_topic(topic):
                        print(f"{Fore.YELLOW}This topic appears to be a duplicate. Do you still want to post it?{Style.RESET_ALL}")
                        if not questionary.confirm("Continue with this topic?", default=False).ask():
                            continue
                    
                    # Force posting regardless of time schedule if requested
                    if args.force or questionary.confirm("Override time scheduling?", default=False).ask():
                        proceed = True
                    else:
                        proceed = bot._should_post_now()
                        if not proceed:
                            print(f"{Fore.YELLOW}Current time is not optimal for posting. Post anyway?{Style.RESET_ALL}")
                            proceed = questionary.confirm("Post anyway?", default=False).ask()
                    
                    if proceed:
                        print(f"{Fore.CYAN}Generating post content...{Style.RESET_ALL}")
                        post_text = bot.generate_post_content(topic)
                        
                        # Show preview
                        print(f"\n{Fore.GREEN}Post Preview:{Style.RESET_ALL}")
                        preview_lines = post_text.split('\n')
                        for line in preview_lines[:min(10, len(preview_lines))]:
                            print(line)
                        if len(preview_lines) > 10:
                            print("...")
                            
                        if not questionary.confirm("Proceed with this post?", default=True).ask():
                            continue
                            
                        # Post with or without image
                        if choice == "Post with image":
                            print(f"{Fore.CYAN}Generating image...{Style.RESET_ALL}")
                            image_path = bot.generate_image(topic)
                            
                            if image_path:
                                print(f"{Fore.GREEN}Image generated at {image_path}{Style.RESET_ALL}")
                                print(f"{Fore.CYAN}Posting to LinkedIn with image...{Style.RESET_ALL}")
                                success = bot.post_to_linkedin_with_image(post_text, image_path)
                            else:
                                print(f"{Fore.YELLOW}Failed to generate image. Post without image?{Style.RESET_ALL}")
                                if questionary.confirm("Post without image?", default=True).ask():
                                    print(f"{Fore.CYAN}Posting to LinkedIn without image...{Style.RESET_ALL}")
                                    success = bot.post_to_linkedin(post_text)
                                else:
                                    continue
                        else:
                            print(f"{Fore.CYAN}Posting to LinkedIn without image...{Style.RESET_ALL}")
                            success = bot.post_to_linkedin(post_text)
                            
                        if success:
                            print(f"{Fore.GREEN}Post successful!{Style.RESET_ALL}")
                            
                            # Save to Topics_done.txt and remove from Topics.txt
                            with open("Topics_done.txt", "a") as done_file:
                                done_file.write(topic + "\n")
                            
                            # Update the topics list
                            topics.pop(topic_index)
                            with open("Topics.txt", "w") as file:
                                file.writelines(topics)
                                
                            print(f"{Fore.GREEN}Topic saved to Topics_done.txt and removed from Topics.txt.{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Failed to post. Please check the logs for details.{Style.RESET_ALL}")
                            
                    else:
                        print(f"{Fore.YELLOW}Posting skipped based on time schedule.{Style.RESET_ALL}")
                
                elif choice == "Generate new topic title":
                    print(f"\n{Fore.CYAN}Generating new topic title...{Style.RESET_ALL}")
                    new_title = bot.generate_topic_title()
                    print(f"\n{Fore.GREEN}Generated Title:{Style.RESET_ALL}")
                    print(f"{new_title}")
                    print(f"\n{Fore.GREEN}Title added to Topics.txt{Style.RESET_ALL}")
                    print()

                elif choice == "Browse all topics":
                    with open("Topics.txt", "r") as file:
                        topics = file.readlines()

                    def display_topic_options(topics, page=0, per_page=10):
                        """Display topics with pagination."""
                        total_pages = (len(topics) + per_page - 1) # per_page
                        start = page * per_page
                        end = min(start + per_page, len(topics))
                        
                        print(f"\n{Fore.GREEN}Available Topics (Page {page+1}/{total_pages}):{Style.RESET_ALL}")
                        for i in range(start, end):
                            print(f"{i+1}. {topics[i].strip()}")
                        
                        print(f"\n{Fore.YELLOW}Navigation: 'n' for next page, 'p' for previous page, 's' to search{Style.RESET_ALL}")
                        return total_pages

                    def search_topics(topics, search_term):
                        """Search for topics containing the search term."""
                        matching_topics = [(i, topic) for i, topic in enumerate(topics) if search_term.lower() in topic.lower()]
                        
                        if not matching_topics:
                            print(f"{Fore.YELLOW}No topics found matching '{search_term}'{Style.RESET_ALL}")
                            return None
                        
                        print(f"\n{Fore.GREEN}Matching Topics:{Style.RESET_ALL}")
                        for i, (index, topic) in enumerate(matching_topics):
                            print(f"{i+1}. {topic.strip()} (#{index+1})")
                        
                        # Let user choose from matching topics
                        choice = questionary.select(
                            "Select a topic:",
                            choices=[f"{i+1}. {topic[1].strip()}" for i, topic in enumerate(matching_topics)] + ["Back to main list"]
                        ).ask()
                        
                        if choice == "Back to main list":
                            return None
                        
                        # Extract the original index from the chosen topic
                        chosen_index = matching_topics[int(choice.split(".")[0]) - 1][0]
                        return chosen_index
                    
                    if not topics:
                        print(f"{Fore.RED}No topics found in Topics.txt.{Style.RESET_ALL}")
                        continue
                        
                    page = 0
                    per_page = 15  # Show more topics per page
                    total_pages = display_topic_options(topics, page, per_page)
                    
                    while True:
                        nav_choice = input(f"{Fore.CYAN}Enter 'n' (next), 'p' (prev), 's' (search), or a number to select topic, or 'q' to quit: {Style.RESET_ALL}").lower()
                        
                        if nav_choice == 'q':
                            break
                        elif nav_choice == 'n' and page < total_pages - 1:
                            page += 1
                            total_pages = display_topic_options(topics, page, per_page)
                        elif nav_choice == 'p' and page > 0:
                            page -= 1
                            total_pages = display_topic_options(topics, page, per_page)
                        elif nav_choice == 's':
                            search_term = input(f"{Fore.CYAN}Enter search term: {Style.RESET_ALL}")
                            topic_index = search_topics(topics, search_term)
                            if topic_index is not None:
                                # User has selected a topic, proceed to posting
                                topic = topics[topic_index].strip()
                                topic_index = topic_index
                                print(f"\n{Fore.CYAN}Selected topic: {topic}{Style.RESET_ALL}")
                                # Add posting logic here
                                break
                            else:
                                # Return to browsing
                                total_pages = display_topic_options(topics, page, per_page)
                        elif nav_choice.isdigit():
                            idx = int(nav_choice) - 1
                            if 0 <= idx < len(topics):
                                topic = topics[idx].strip()
                                topic_index = idx
                                print(f"\n{Fore.CYAN}Selected topic: {topic}{Style.RESET_ALL}")
                                # Add posting logic here
                                break
                            else:
                                print(f"{Fore.RED}Invalid topic number.{Style.RESET_ALL}")

                elif choice == "Search topics":
                    with open("Topics.txt", "r") as file:
                        topics = file.readlines()
                    
                    search_term = input(f"{Fore.CYAN}Enter search term: {Style.RESET_ALL}")
                    topic_index = search_topics(topics, search_term)
                    
                    if topic_index is not None:
                        topic = topics[topic_index].strip()
                        print(f"\n{Fore.CYAN}Selected topic: {topic}{Style.RESET_ALL}")
                        # Continue with posting options
                        post_with_image = questionary.confirm("Post with image?", default=True).ask()
                        
                        if proceed:
                            print(f"{Fore.CYAN}Generating post content...{Style.RESET_ALL}")
                            post_text = bot.generate_post_content(topic)
                            
                            # Show preview
                            print(f"\n{Fore.GREEN}Post Preview:{Style.RESET_ALL}")
                            preview_lines = post_text.split('\n')
                            for line in preview_lines[:min(10, len(preview_lines))]:
                                print(line)
                            if len(preview_lines) > 10:
                                print("...")
                                
                            if not questionary.confirm("Proceed with this post?", default=True).ask():
                                continue
                                
                            # Post with or without image
                            if post_with_image:
                                print(f"{Fore.CYAN}Generating image...{Style.RESET_ALL}")
                                image_path = bot.generate_image(topic)
                                
                                if image_path:
                                    print(f"{Fore.GREEN}Image generated at {image_path}{Style.RESET_ALL}")
                                    print(f"{Fore.CYAN}Posting to LinkedIn with image...{Style.RESET_ALL}")
                                    success = bot.post_to_linkedin_with_image(post_text, image_path)
                                else:
                                    print(f"{Fore.YELLOW}Failed to generate image. Post without image?{Style.RESET_ALL}")
                                    if questionary.confirm("Post without image?", default=True).ask():
                                        print(f"{Fore.CYAN}Posting to LinkedIn without image...{Style.RESET_ALL}")
                                        success = bot.post_to_linkedin(post_text)
                                    else:
                                        continue
                            else:
                                print(f"{Fore.CYAN}Posting to LinkedIn without image...{Style.RESET_ALL}")
                                success = bot.post_to_linkedin(post_text)

                elif choice == "Analyze error images":
                    error_images = [f for f in os.listdir() if f.startswith(("error_", "before_", "post_button_not_found"))]
                    
                    if not error_images:
                        print(f"{Fore.YELLOW}No error images found.{Style.RESET_ALL}")
                        continue
                        
                    print(f"\n{Fore.GREEN}Found {len(error_images)} error images:{Style.RESET_ALL}")
                    for i, img in enumerate(error_images[:10]):  # Show max 10
                        print(f"{i+1}. {img}")
                    
                    if len(error_images) > 10:
                        print(f"...and {len(error_images)-10} more")
                    
                    try:
                        selected = questionary.select(
                            "Select an image to analyze:",
                            choices=[f"{i+1}. {img}" for i, img in enumerate(error_images[:10])] + ["Cancel"]
                        ).ask()
                        
                        if selected != "Cancel":
                            img_idx = int(selected.split(".")[0]) - 1
                            img_path = error_images[img_idx]
                            bot.analyze_error_image(img_path)
                    except Exception as e:
                        print(f"{Fore.RED}Error selecting image: {str(e)}{Style.RESET_ALL}")

                elif choice == "View HTML Source":
                    print(f"{Fore.CYAN}Saving current page HTML for analysis...{Style.RESET_ALL}")
                    try:
                        with open(f"page_source_{int(time.time())}.html", "w", encoding="utf-8") as f:
                            f.write(bot.driver.page_source)
                        print(f"{Fore.GREEN}HTML source saved successfully.{Style.RESET_ALL}")
                        
                        # Also take a screenshot
                        screenshot_path = f"current_page_{int(time.time())}.png"
                        bot.driver.save_screenshot(screenshot_path)
                        print(f"{Fore.GREEN}Screenshot saved to {screenshot_path}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving HTML source: {str(e)}{Style.RESET_ALL}")
                    print()
            
            print(f"{Fore.GREEN}Thank you for using LinkedIn Automation Bot!{Style.RESET_ALL}")
                
        except Exception as e:
            logging.error(f"Error in main menu: {str(e)}", exc_info=True)
            print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
            
        finally:
            # Properly close session
            try:
                bot.driver.quit()
                logging.info("Driver session ended cleanly.")
            except:
                pass
                
            # Remove lock file
            if os.path.exists("linkedin_bot.lock"):
                os.remove("linkedin_bot.lock")
                
    except Exception as e:
        logging.error(f"Critical error: {str(e)}", exc_info=True)
        print(f"{Fore.RED}Critical error: {str(e)}{Style.RESET_ALL}")
        # Remove lock file in case of critical error
        if os.path.exists("linkedin_bot.lock"):
            os.remove("linkedin_bot.lock")

