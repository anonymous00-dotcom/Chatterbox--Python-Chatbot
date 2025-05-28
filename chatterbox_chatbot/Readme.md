# Chatterbox Chatbot

A modern, multi-feature chatbot with a WhatsApp/Instagram-style interface using `customtkinter`.  
Supports light/dark mode, Wikipedia, DuckDuckGo, calculator, weather, jokes, and more!  
You can also **train the bot with your own questions and answers** using the "Train Bot" tab.

---

## 🛠️ Requirements

Install these Python libraries in your environment:

```sh
pip install customtkinter wikipedia requests tensorflow scikit-learn numpy
```

**Required libraries:**
- `customtkinter` (for the modern GUI)
- `wikipedia` (for Wikipedia summaries)
- `requests` (for all API calls)
- `tensorflow` (for training and running the chatbot model)
- `scikit-learn` (for text processing in training/testing)
- `numpy` (for data handling in training/testing)

You also need:
- Python 3.8 or newer

---

## 🚀 How to Run

1. Make sure all required libraries are installed.
2. Place `chatbot_gui.py`, `training.py`, `testing.py`, and `intents.json` in the same folder.
3. Run:
   ```sh
   python chatbot_gui.py
   ```

---

## 💡 Features & Example Inputs

| Feature         | Example Input                        | Description                                      |
|-----------------|-------------------------------------|--------------------------------------------------|
| **Chat**        | `Hello`                             | General conversation                             |
| **Joke**        | `tell me a joke`                    | Get a random joke                                |
| **Calculator**  | `calc 2+2*5`<br>`calculate sqrt(16)`| Math calculation using Math.js API                |
| **Weather**     | `weather London`                    | Get current weather for a city (Open-Meteo API)  |
| **Wikipedia**   | `wiki Python`<br>`wikipedia India`  | Get a summary from Wikipedia                     |
| **DuckDuckGo**  | `duck Alan Turing`<br>`search AI`   | Get instant answers from DuckDuckGo              |
| **Train Bot**   | *(GUI tab)*                         | Add new intents and responses                    |
| **Light/Dark**  | *(Toggle button in GUI)*            | Switch between light and dark mode               |

---

## 🧠 Train Your Bot

- Go to the **"Train Bot"** tab in the app.
- Enter a tag, patterns (questions), and responses (answers).
- Click **"Train Bot"** to add new knowledge to your chatbot!

---

## 📝 Notes

- **Weather and calculator** do not require API keys.
- **Wikipedia and DuckDuckGo** work for most general queries.
- **Training**: Use the "Train Bot" tab to add new patterns and responses.
- **Auto-scroll**: Chat always scrolls to the latest message.
- **Sender color**: "You" and "Chatterbox" labels adapt to light/dark mode.

---

## 📷 Screenshots

![Dark Mode Example]([[Dark_Theme.png]([url](https://drive.google.com/file/d/1Sxl6snvdh4mSrCwTzcvo2HtCdNiMOXck/view?usp=sharing))]
![Light Mode Example]([Light_Theme.png](https://drive.google.com/file/d/1pN0lGOp7SqtByP416LYjWm_vs_6vuRGN/view?usp=sharing))

---

## 👨‍💻 Author

Created by Suvrodip aka SD  
For college project use.

---
