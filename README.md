cat <<EOF > README.md
# 🧠 Reddit API Fetcher - TrendAnalyzer

This project is a Python-based tool that connects to Reddit using the PRAW (Python Reddit API Wrapper) library. It fetches posts from a given subreddit, filters them by score, and generates both a CSV and a professional-looking PDF report with the results.

## 🚀 How to Run the Project

### 1. Clone the Repo
\`\`\`bash
git clone https://github.com/your-username/reddit-api-fetcher.git
cd reddit-api-fetcher
\`\`\`

### 2. Create a Virtual Environment
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install Required Packages
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Add Your Reddit API Credentials
Create a \`.env\` file in the root folder:
\`\`\`
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USER_AGENT=your_user_agent
\`\`\`

### 5. Run the Script
\`\`\`bash
python main.py --subreddit python --score 200 --limit 5 --type hot --path ./output
\`\`\`

## 📂 Output
- \`filtered_posts.csv\`
- \`Filtered_Posts.pdf\`
EOF
