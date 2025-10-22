📘 Reality Check AI

AI-powered media verification for journalists and digital truth seekers.


---

🌍 Overview

Reality Check AI helps journalists, researchers, and everyday users detect whether an image or video frame has been AI-generated or human-made.
Powered by advanced AI models from Hugging Face, this app offers real-time authenticity analysis with a clean, mobile-friendly interface.

Upload. Analyze. Verify — before you amplify.


---

🧠 Key Features

🖼️ AI Image Detection: Quickly verify authenticity using the latest detection models.

📱 Mobile & Web Optimized: Works seamlessly across devices.

🔐 Secure & Private: Files are analyzed instantly without being stored.

🧾 Confidence Dashboard: See detection confidence scores in real time.

👥 Press Login (coming soon): Verified journalist accounts for story tracking and submissions.



---

🧰 Tech Stack

Layer	Tools

Frontend	HTML5, CSS3, Vanilla JS
Backend	Flask (Python)
AI API	Hugging Face API (Image authenticity detection)
Hosting	Vercel
Storage	Firebase (for future journalist logins)



---

🚀 Quick Start (Local Setup)

You can also run Reality Check locally on your computer before deploying.

# Clone the repository
git clone https://github.com/YOUR_USERNAME/reality-check-ai.git
cd reality-check-ai/api

# Install dependencies
pip install -r requirements.txt

# Set your Hugging Face token
export HUGGINGFACE_TOKEN="your_token_here"

# Run the app
python main.py

Then open your browser at:
👉 http://127.0.0.1:5000


---

🧩 Project Structure

api/
 ├── main.py                # Flask backend logic
 ├── requirements.txt       # Python dependencies
 ├── templates/
 │    └── index.html        # Frontend layout
 └── static/
      ├── style.css         # App styling
      ├── logo.png          # Logo image
      └── background.png    # Background image
runtime.txt
vercel.json
README.md


---

🪶 Deployment (Vercel)

1. Push your repository to GitHub.


2. Log into Vercel → Import Project → GitHub Repo


3. Set your environment variable:

HUGGINGFACE_TOKEN = your_token_here


4. Click Deploy.


5. Your app will be live in seconds! 🌐




---

🧩 Example Use Cases

Newsrooms: Rapidly vet viral images before publication.

Fact-Checking Teams: Add AI detection as a verification layer.

Educators: Demonstrate media literacy tools.

Developers: Build custom extensions for detection APIs.



---

🧑‍💻 Developer

Created by: Shane — with assistance from GPT-5.
Goal: Build open tools for truth and digital integrity.


---

📄 License

This project is released under the MIT License, allowing free use and modification with attribution.


---

Would you like me to include visual badges and a banner image at the top (so it looks even more like a professional open-source GitHub project)?
For example: “Built with Flask 🧠 | Powered by Hugging Face 🤖 | Verified for Journalists 📰”.
