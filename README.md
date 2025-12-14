# 🤖 AI Bot (Gemini CLI)

A command-line AI chatbot built in **Python** using the **Google Gemini API**.  
This project allows users to send prompts from the terminal and receive AI-generated responses, demonstrating how to integrate modern LLM APIs in a backend-focused application.

---

## 🧠 Overview

This project is a simple CLI-based AI assistant powered by **Gemini 2.5 Flash**.  
It uses environment variables for secure API key management and accepts user input via command-line arguments.

The project is designed for learning backend development concepts and AI integration using clean and minimal Python code.

---

## 🚀 Features

- Send prompts to Gemini directly from the terminal
- Uses Google Gemini `gemini-2.5-flash` model
- Secure API key handling with `.env`
- Configurable AI generation parameters
- Basic error handling for failed API requests

---

## 🛠 Tech Stack

- **Language:** Python
- **AI Model:** Google Gemini 2.5 Flash
- **Libraries:**
  - `google-genai`
  - `python-dotenv`
  - `argparse`

---

## 📂 Project Structure

```

aibot/
├── main.py              # CLI entry point for sending prompts to Gemini
├── .env                 # Environment variables (not committed)
├── requirements.txt     # Python dependencies
└── README.md

````

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Saksham-Bansal-3110/aibot.git
cd aibot
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

⚠️ **Never commit your API key to GitHub.**

---

## ▶️ Usage

Run the bot by passing a prompt as a command-line argument:

```bash
python main.py "Explain REST APIs in simple terms"
```

### Example Output

```bash
Response: REST APIs allow different systems to communicate over HTTP using standard methods like GET and POST...
```

---

## ⚙️ Model Configuration

The chatbot uses the following Gemini configuration:

* **Model:** `gemini-2.5-flash`
* **Temperature:** `0`
* **Top-p:** `0.95`
* **Top-k:** `20`

These values are defined in `main.py` and can be adjusted as needed.

---

## 🧪 Error Handling

* Ensures `GEMINI_API_KEY` is present before execution
* Handles failed API requests gracefully
* Prints meaningful error messages on failure

---

## 📈 Learning Objectives

This project helps in understanding:

* How to integrate Large Language Models (LLMs)
* Backend configuration using environment variables
* CLI-based application design
* Secure handling of API keys
* AI usage in backend systems

---

## 🔮 Future Improvements

* Add verbose/debug logging support
* Convert to a Flask or FastAPI backend
* Add conversation history support
* Add unit testing
* Support multiple AI models

---

## 📄 License

MIT License

---

## 👤 Author

**Saksham Bansal**
GitHub: [@Saksham-Bansal-3110](https://github.com/Saksham-Bansal-3110)
