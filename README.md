<p align="center">
  <img src="https://i.ibb.co/B5T5qkt2/New-Project-10.png" alt="Logo" width="200"/>
</p>

# ⚡ Conjugemos Cheater

<p align="center">
  <a href="https://github.com/locuslol/conjugemos-cheater">
    <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge&logo=github&color=00ffaa" alt="Status: Active">
  </a>
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python&logoColor=white&color=306998" alt="Python">
  <img src="https://img.shields.io/badge/AI%20Model-Gemini%202.5%20Flash-fuchsia?style=for-the-badge&logo=google&logoColor=white&color=0ea5e9" alt="Gemini 2.5 Flash">
</p>

> 🧠 A desktop automation tool built with **Python**, **Tesseract OCR**, and the **Gemini API** to automatically solve Spanish conjugation exercises from *Conjugemos* by reading the screen and typing the answer.

---

## 💡 Overview

**Conjugemos Cheater** automates the process of conjugating Spanish verbs during timed Conjugemos exercises.  
It acts as a **real-time assistant** by:

1. 📸 **Capturing** the exercise prompt (tense, subject, and verb) from the screen using **PyAutoGUI** and **Tesseract OCR**.  
2. 🤖 **Solving** the conjugation by sending the details to **Gemini 2.5 Flash** for accurate answers.  
3. ⌨️ **Typing** the correct conjugation directly into the input box automatically.

The application features a **modern, top-most GUI** built with **Tkinter** for easy setup and activity monitoring.

---

## ✨ Features

- ⚙️ **Real-Time Monitoring:** Continuously scans a user-defined screen region for new questions.  
- 🤖 **Gemini API Integration:** Uses Gemini 2.5 Flash for context-aware conjugations (handles irregular, reflexive, and compound tenses).  
- 🧠 **Robust Text Parsing:** Custom pattern matching handles OCR errors and input variations.  
- ⌨️ **Seamless Typing:** Clicks and types the correct answer automatically.  
- 🪟 **Modern Tkinter GUI:** Simple interface for managing API keys, regions, and logs.  
- 💾 **Persistent Configuration:** Saves your Gemini API key in `conjugemos_config.json`.

---

## 🛠️ Prerequisites

Before running the application, ensure the following are installed:

### 1. 🐍 Python 3.x  
Install the latest version of Python from [python.org](https://www.python.org/).

### 2. 🔍 Tesseract OCR  
Used to convert screenshots into readable text. Must be installed and added to PATH.

- **Windows:** [Tesseract-OCR GitHub Wiki](https://github.com/UB-Mannheim/tesseract/wiki)  
- **macOS:** `brew install tesseract`  
- **Linux:** `sudo apt-get install tesseract-ocr`

### 3. 🔑 Gemini API Key  
Required for conjugation logic.  
Get your free key here → [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## 📦 Installation and Usage

### 1. Clone the Repository
```bash
git clone https://github.com/locuslol/conjugemos-cheater.git
cd conjugemos-cheater
```

### 2. Install Dependencies
```bash
pip install pyautogui pytesseract pillow google-genai pyperclip keyboard
```
Or use the batch file provided in the release to install the requirements.

### 3. Run the Application
```bash
python main.py
```

---

## ⚙️ Setup Instructions

When the app launches, follow these steps:

### 🧩 A. Configure API Key
If no key is found, a prompt will appear.  
Paste your Gemini API key and click **“Save & Continue”**.  
The key is saved in `conjugemos_config.json`.

---

### 🖼️ B. Setup Monitoring Region
Defines the area the program will “watch” and where it will type.

1. Open your Conjugemos exercise.  
2. Click **“⚙ Setup Region”** in the app.  
3. You’ll have 3 seconds to set each:
   - **📍 TOP-LEFT Corner:** Top-left of the question area.  
   - **📍 BOTTOM-RIGHT Corner:** Bottom-right of the question area.  
   - **📍 ANSWER INPUT BOX:** Where the script should click to type.

---

### ▶️ C. Start Monitoring
Click **“▶ Start Monitoring.”**  
The status will turn **Active (pulsing green)**.  
Switch to your Conjugemos tab — the bot will solve and type automatically.  
Click **“⏸ Stop Monitoring”** to pause anytime.

---

## 👨‍💻 Technical Breakdown

The `monitor_loop` function powers the automation, using Gemini for real-time conjugation accuracy.

```python
# Gemini prompt template
"""You are a Spanish conjugation expert. Conjugate the verb '{verb}' in {tense} tense for the subject '{subject}'.

CRITICAL INSTRUCTIONS:
1. Translate the English verb to the MOST COMMON Spanish equivalent used in textbooks
2. If the English verb contains hints like "(not X)" or "(use Y)", follow those instructions
3. For reflexive verbs, include the reflexive pronoun (me, te, se, nos, os, se)
4. Return the COMPLETE conjugated form - for compound tenses, include both parts

Rules:
- Return ONLY the conjugated verb form, no explanations
- For compound tenses like present perfect: include auxiliary + participle (e.g., "han visto")
- For reflexive verbs: include pronoun (e.g., "me cepillo", "te lavas")

Examples:
- present perfect, ustedes, see → han visto
- preterite, yo, eat → comí
- present subjunctive, nosotros, understand → entendamos
- present, tú, brush oneself → te cepillas
- future, yo, put on → me pondré
- present subjunctive, nosotros, understand (not comprender) → entendamos

Now conjugate: {tense}, {subject}, {verb}

Answer with ONLY the conjugated form:"""
```

---

## 🛑 Disclaimer
This project is for **educational and development purposes only.**  
Use responsibly and in accordance with the **terms of service** of any platform.  
The author assumes **no liability** for misuse.

---

<p align="center">
  🧠 Built with ❤️ using Python, Gemini AI, and Tesseract OCR
</p>
