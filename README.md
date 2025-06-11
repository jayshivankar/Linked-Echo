# 🚀 LinkedIn-Echo

> Generate LinkedIn posts in your **own writing style** using your previous posts as training data.

**Built with:**  
🔗 [LangChain](https://www.langchain.com/) • 🦙 LLaMA 3 (via Groq ) • 📊 Pandas • 🎯 Streamlit

---

## 💡 Project Overview

**Linked-Echo** is an AI-powered tool designed for **LinkedIn influencers** who want to generate new posts that **match their personal writing style**.

Let’s say *Jay* is a LinkedIn influencer. He uploads his past posts to this tool, which:

1. **Analyzes** them to extract:
   - Topics
   - Language
   - Post Length
2. Uses this metadata to allow custom generation of new posts via a **few-shot prompt strategy**, imitating Jay’s writing style.

---

## 🧠 How It Works

### ✅ Stage 1: Data Ingestion & Metadata Extraction

- Upload raw LinkedIn posts in JSON format.
- NLP pipeline extracts:
  - **Topics** (via keyword extraction )
  - **Length** (line or word count buckets)
  - **Language** (via langdetect )

### ✅ Stage 2: Post Generation

- User selects:
  - Topic
  - Post Length (`Short`, `Medium`, `Long`)
  - Language
- A prompt is constructed using past posts (few-shot examples) to guide the LLM.
- New post is generated in a **matching tone, style, and topic**.

---

## 🛠️ Tech Stack

| Component         | Tooling                             |
|------------------|-------------------------------------|
| Backend LLM      | LLaMA 3 (via Groq or other APIs)    |
| Prompting        | LangChain PromptTemplates + Chains  |
| UI               | Streamlit                           |
| Vector Search    | FAISS (Optional for semantic match) |
| Data Processing  | pandas, langdetect, sklearn         |

---

## 📂 Project Structure

```
genai-post-generator/
│
├── app.py                     # Streamlit UI
├── generator.py              # Prompt construction & LLM interface
├── preprocess.py             # Metadata extraction (topics, language, length)
├── utils.py                  # Utility functions
├── data/
│   ├── raw_posts.json        # Input data
│   └── processed_posts.json  # Output with extracted metadata
├── .env                      # API keys (Groq, OpenAI, etc.)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/genai-post-generator.git
cd genai-post-generator
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

> Alternatively, use OpenAI API key if switching LLM providers.

---

## 🧪 Run the App

```bash
streamlit run app.py
```

---

## ✨ Features

- ✅ Extracts metadata: Topic, Language, Length
- ✅ Uses Few-shot learning with similar past posts
- ✅ Generates natural, human-like LinkedIn posts
- ✅ UI to filter, preview, and copy output
- ✅ Supports multiple languages

---

## 📸 Demo Screenshot

![linkedin_echo_2](https://github.com/user-attachments/assets/6126d6e6-25d2-4a7d-91f2-8a1584949be7)




## 📌 Example JSON Input Format

```json
[
  {
    "content": "I just learned about LLMs and how they work. It's fascinating!",
    "date": "2024-06-10"
  },
  {
    "content": "Growth mindset is everything when you're starting out in tech.",
    "date": "2024-06-05"
  }
]
```

---

## 🧠 Prompt Strategy

Uses LangChain to build prompts dynamically:

- Filters relevant past posts matching topic + length
- Adds them as few-shot examples
- Generates new content using LLaMA via API
