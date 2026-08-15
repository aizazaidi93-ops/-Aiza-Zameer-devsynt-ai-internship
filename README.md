-Aiza-Zameer-devsynt-ai-internship

AI Engineering Internship Task 1

DevSynt AI Automation Internship – Summer 2026

Name: Aiza Zameer

This repository contains my weekly tasks, workflows, and project progress completed during the DevSynt AI Automation Internship – Summer 2026.

PROJECT 1:
# SlotWise Discord Booking Assistant Bot
SlotWise is an AI-powered Discord bot that helps users book restaurant tables and salon/parlour appointments through natural conversation. It uses n8n for workflow automation, Google Gemini for AI responses, and Google Sheets for storing booking data.

# How It Works
1. A lightweight Node.js relay bot listens for messages in Discord.
2. Messages are forwarded to an n8n webhook.
3. An AI Agent (powered by Google Gemini) processes the message and generates a conversational response.
4. Booking details (Username, Service, Date, Time) are extracted and saved to a Google Sheet.
5. The AI-generated reply is sent back to the user in Discord.

#Tech Stack
- Node.js + discord.js — Discord message relay
- n8n — workflow automation
- Google Gemini API — AI response generation
- Google Sheets API — booking data storage
- Discord API — bot messaging
  
#Setup
1. **Discord Bot**: Create an application in the Discord Developer Portal, enable Message Content Intent, get the Bot Token, and invite the bot to your server.
2. **Relay Bot**: Clone the repo, run `npm install`, add your `N8N_WEBHOOK_URL` and `BOT_TOKEN` in `index.js`, then run `node index.js`.
3. **n8n Workflow**: Set up a Webhook node → AI Agent (Google Gemini + Simple Memory) → Edit Fields (extracts booking data) → Google Sheets (logs booking) → Discord node (sends reply). Activate/publish the workflow.

#Features
- Natural language booking for restaurants and salons
- AI-powered conversational responses
- Automatic booking data logging to Google Sheets
- Real-time reply within Discord channels

 #Notes
- The relay bot must stay running for the workflow to receive Discord messages.
- The n8n workflow must remain Published.
