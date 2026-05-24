import os
import google.generativeai as genai

# Setup AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

user_name = os.environ.get("USER_NAME", "Guest")
user_message = os.environ.get("ISSUE_BODY", "Hello!")

# Give your bot a distinct personality
system_prompt = f"You are a helpful, witty AI assistant living on my GitHub Profile. A visitor named @{user_name} says: '{user_message}'. Respond to them concisely (under 3 sentences). Be welcoming, point out some of my pinned repositories if relevant, and keep it lighthearted!"

response = model.generate_content(system_prompt)
bot_reply = response.text

# Save response for the GitHub issue closer
with open("bot_reply.txt", "w") as f:
    f.write(f"🤖 **Assistant says:**\n\n{bot_reply}")

# Update the README file dynamically
with open("README.md", "r") as f:
    readme_content = f.read()

# Define anchor points in your markdown file
start_marker = "<!-- BOT-CHAT-START -->"
end_marker = "<!-- BOT-CHAT-END -->"

if start_marker in readme_content and end_marker in readme_content:
    before = readme_content.split(start_marker)[0]
    after = readme_content.split(end_marker)[1]
    
    # Construct new log block
    new_chat_log = f"""{start_marker}
> **Latest Transmission:**
> 💬 **@{user_name}**: {user_message}
> 🤖 **Assistant**: {bot_reply}
{end_marker}"""
    
    with open("README.md", "w") as f:
        f.write(before + new_chat_log + after)
