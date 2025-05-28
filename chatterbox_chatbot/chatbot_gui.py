from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import json
import requests
#importthe training.py
#and testing.py file
import testing as testpy
import training as trainpy
import wikipedia
import urllib.parse

ctk.set_appearance_mode("dark")  # Start in dark mode
ctk.set_default_color_theme("dark-blue")

FONT = ("Segoe UI", 16)
FONT_BOLD = ("Segoe UI", 16, "bold")

class ChatBot:
    def __init__(self):
        #initialize customtkinter window
        self.theme = "dark"
        self.window = ctk.CTk()
        self.window.title("Chatterbox")
        self.window.geometry("540x650")
        self.window.resizable(False, False)
        self.test = testpy.Testing()
        self.sender_labels = []
        self.main_window()

    def toggle_theme(self):
        # Switch between dark and light mode
        if self.theme == "dark":
            ctk.set_appearance_mode("light")
            self.theme = "light"
            self.toggle_button.configure(text="🌙")
            self.chat_frame.configure(fg_color="#FFFFFF")
            self.bot_tab.configure(fg_color="#FFFFFF")
        else:
            ctk.set_appearance_mode("dark")
            self.theme = "dark"
            self.toggle_button.configure(text="☀️")
            self.chat_frame.configure(fg_color="transparent")
            self.bot_tab.configure(fg_color="transparent")
        # Dynamically update all sender label colors
        sender_fg = "#181818" if self.theme == "light" else "#fff"
        for label in self.sender_labels:
            label.configure(text_color=sender_fg)

    def main_window(self):
        #add tab for Chatbot and Train Bot in Notebook frame
        self.tabview = ctk.CTkTabview(self.window, width=520, height=600)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        self.bot_tab = self.tabview.add("💬 Chatterbox")
        self.train_tab = self.tabview.add("⚙️ Train Bot")

        #Add heading to the Chabot window
        self.head_label = ctk.CTkLabel(self.bot_tab, text="Welcome to Chatterbox", font=FONT_BOLD, anchor="w")
        self.head_label.pack(fill="x", pady=(10, 0), padx=10)

        # Theme toggle button (top right)
        self.toggle_button = ctk.CTkButton(self.bot_tab, text="☀️", width=40, command=self.toggle_theme)
        self.toggle_button.place(relx=0.92, rely=0.01)

        # Modern chat area frame using CTkScrollableFrame for chat bubbles
        self.chat_frame = ctk.CTkScrollableFrame(self.bot_tab, width=480, height=370, fg_color="transparent")
        self.chat_frame.pack(padx=10, pady=(10, 0), fill="both", expand=True)
        self.bot_tab.configure(fg_color="transparent")

        # Modern bottom frame for entry and send button
        entry_frame = ctk.CTkFrame(self.bot_tab, fg_color="transparent")
        entry_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        # Quick actions frame
        actions_frame = ctk.CTkFrame(self.bot_tab, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        # Quick action buttons
        quick_actions = [
            ("🌤️ Weather", "weather"),
            ("🔍 Search", "duck"),
            ("📚 Wiki", "wiki"),
            ("😄 Joke", "tell me a joke"),
            ("🧮 Calc", "calc")
        ]

        for text, cmd in quick_actions:
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                width=70,
                height=30,
                font=("Segoe UI", 12),
                command=lambda c=cmd: self.quick_action(c)
            )
            btn.pack(side="left", padx=5)

        # Entry and send button
        self.msg_entry = ctk.CTkEntry(entry_frame, width=350, font=FONT)
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", self.on_enter)
        self.send_button = ctk.CTkButton(entry_frame, text="➤", width=50, font=FONT_BOLD, command=lambda: self.on_enter(None))
        self.send_button.pack(side="right")

        self.add_train()

    def add_train(self):
        #Add heading to the Train Bot window
        head_label = ctk.CTkLabel(self.train_tab, text="Train Bot", font=FONT_BOLD)
        head_label.pack(pady=10, fill="x")

        #Tag Label and Entry for intents tag 
        taglabel = ctk.CTkLabel(self.train_tab, text="Tag", font=FONT)
        taglabel.place(relx=0.01, rely=0.12)
        self.tag = ctk.CTkEntry(self.train_tab, width=300, font=FONT)
        self.tag.place(relx=0.22, rely=0.12, relwidth=0.7)

        #Pattern Label and Entry for pattern to our tag
        self.pattern = []
        for i in range(2):
            patternlabel = ctk.CTkLabel(self.train_tab, text=f"Pattern{i+1}", font=FONT)
            patternlabel.place(relx=0.01, rely=0.22 + 0.08 * i)
            entry = ctk.CTkEntry(self.train_tab, width=300, font=FONT)
            entry.place(relx=0.22, rely=0.22 + 0.08 * i, relwidth=0.7)
            self.pattern.append(entry)

        #Response Label and Entry for response to our pattern.
        self.response = []
        for i in range(2):
            responselabel = ctk.CTkLabel(self.train_tab, text=f"Response{i+1}", font=FONT)
            responselabel.place(relx=0.01, rely=0.38 + 0.08 * i)
            entry = ctk.CTkEntry(self.train_tab, width=300, font=FONT)
            entry.place(relx=0.22, rely=0.38 + 0.08 * i, relwidth=0.7)
            self.response.append(entry)

        #to train our bot create Train Bot button which will call on_train function
        train_button = ctk.CTkButton(self.train_tab, text="Train Bot", font=FONT_BOLD, command=lambda: self.on_train(None))
        train_button.place(relx=0.20, rely=0.60, relwidth=0.60)

    def on_train(self, event):
        #read intent file and append created tag,pattern and responses from add_train function
        with open('intents.json', 'r+') as json_file:
            file_data = json.load(json_file)
            file_data['intents'].append({
                "tag": self.tag.get(),
                "patterns": [i.get() for i in self.pattern],
                "responses": [i.get() for i in self.response],
                "context": ""
            })
            json_file.seek(0)
            json.dump(file_data, json_file, indent=1)
        #run and compile model from our training.py file
        train = trainpy.Training()
        train.build(); print("Trained Successfully")
        self.test = testpy.Testing()

    def on_enter(self, event):
        #get user query and bot response
        msg = self.msg_entry.get()
        self.my_msg(msg, "You")
        self.bot_response(msg, "Chatterbox")
        
    # API calls
        #Joke API
    def get_joke(self):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"{data['setup']}\n{data['punchline']}"
            else:
                return "Sorry, I couldn't fetch a joke right now."
        except Exception:
            return "Sorry, I couldn't fetch a joke right now."
       
       #Wikipedia API
    def get_wikipedia_summary(self, query):
        try:
            summary = wikipedia.summary(query, sentences=2)
            return summary
        except Exception:
            return "Sorry, I couldn't find a Wikipedia summary for that."
       
        #DuckDuckGo API
    def get_duckduckgo_answer(self, query):
        try:
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_redirect=1"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                # Try AbstractText
                if data.get("AbstractText"):
                    return data["AbstractText"]
                # Try Answer
                elif data.get("Answer"):
                    return data["Answer"]
                # Try RelatedTopics
                elif data.get("RelatedTopics"):
                    topics = data["RelatedTopics"]
                    for topic in topics:
                        if isinstance(topic, dict) and topic.get("Text"):
                            return topic["Text"]
                    # Sometimes RelatedTopics is a list of dicts with "Topics" key
                    for topic in topics:
                        if isinstance(topic, dict) and "Topics" in topic:
                            for subtopic in topic["Topics"]:
                                if subtopic.get("Text"):
                                    return subtopic["Text"]
                return "Sorry, I couldn't find an instant answer, but you can try searching online."
            else:
                return "Sorry, DuckDuckGo search failed."
        except Exception:
            return "Sorry, DuckDuckGo search failed."
          
        #Calculator API                 
    def get_calculation(self, expr):
        try:
            url = f"https://api.mathjs.org/v4/?expr={urllib.parse.quote(expr)}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                return resp.text
            else:
                return "Sorry, I couldn't calculate that."
        except Exception:
            return "Sorry, I couldn't calculate that."
        
        #Weather API
    def get_weather(self, city):
        try:
            # Get coordinates from geocoding API
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
            geo_resp = requests.get(geo_url, timeout=5)
            geo_data = geo_resp.json()
            if "results" not in geo_data or not geo_data["results"]:
                return "Sorry, I couldn't find that city."
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            # Get weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_resp = requests.get(weather_url, timeout=5)
            weather_data = weather_resp.json()
            if "current_weather" in weather_data:
                w = weather_data["current_weather"]
                return f"Weather in {city.title()}: {w['temperature']}°C, wind {w['windspeed']} km/h"
            else:
                return "Sorry, I couldn't get the weather."
        except Exception:
            return "Sorry, I couldn't get the weather."

    def bot_response(self, msg, sender):
        # Calculator
        if msg.lower().startswith("calc ") or msg.lower().startswith("calculate "):
            expr = msg.split(" ", 1)[1] if " " in msg else ""
            if expr:
                result = self.get_calculation(expr)
                self.insert_bubble(result, sender, "bot")
            else:
                self.insert_bubble("Please provide an expression after 'calc'.", sender, "bot")
        # Weather
        elif msg.lower().startswith("weather "):
            city = msg.split(" ", 1)[1] if " " in msg else ""
            if city:
                result = self.get_weather(city)
                self.insert_bubble(result, sender, "bot")
            else:
                self.insert_bubble("Please provide a city after 'weather'.", sender, "bot")
        # Check for joke request
        elif any(phrase in msg.lower() for phrase in ["give me a joke", "write a joke", "tell me a joke"]):
            joke = self.get_joke()
            self.insert_bubble(joke, sender, "bot")
        # Wikipedia search
        elif msg.lower().startswith("wiki ") or msg.lower().startswith("wikipedia "):
            topic = msg.split(" ", 1)[1] if " " in msg else ""
            if topic:
                summary = self.get_wikipedia_summary(topic)
                self.insert_bubble(summary, sender, "bot")
            else:
                self.insert_bubble("Please provide a topic after 'wiki'.", sender, "bot")
        # DuckDuckGo search
        elif msg.lower().startswith("duck ") or msg.lower().startswith("search "):
            query = msg.split(" ", 1)[1] if " " in msg else ""
            if query:
                answer = self.get_duckduckgo_answer(query)
                self.insert_bubble(answer, sender, "bot")
            else:
                self.insert_bubble("Please provide a query after 'duck' or 'search'.", sender, "bot")
        else:
            self.insert_bubble(self.test.response(msg), sender, "bot")

    def my_msg(self, msg, sender):
        #it will display user query and bot response in chat_frame
        if not msg:
            return
        self.msg_entry.delete(0, "end")
        self.insert_bubble(msg, sender, "user")

    def insert_bubble(self, msg, sender, who):
        # Modern chat bubble style using CTkLabel
        if who == "user":
            bubble_color = "#8338ec"
            fg = "#fff"
            anchor = "e"
            padx = (80, 10)
            side = "right"
        else:
            bubble_color = "#232323" if self.theme == "dark" else "#F1F0F0"
            fg = "#fff" if self.theme == "dark" else "#181818"
            anchor = "w"
            padx = (10, 80)
            side = "left"
        # Frame for sender and bubble (so they stay together)
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_frame.pack(anchor=anchor, padx=padx, pady=1)  # No fill, minimal vertical space

        # Inner frame for alignment
        inner = ctk.CTkFrame(msg_frame, fg_color="transparent")
        inner.pack(side=side, anchor=anchor)

        # Sender label (small, above bubble)
        sender_fg = "#181818" if self.theme == "light" else "#fff"
        sender_label = ctk.CTkLabel(
            inner,
            text=sender,
            font=("Segoe UI", 12, "bold"),
            text_color=sender_fg,
            fg_color="transparent",
            anchor=anchor
        )
        sender_label.pack(anchor=anchor, pady=(0, 0))  # No extra space below sender
        self.sender_labels.append(sender_label)  #Store reference

        # Bubble label (do NOT fill x, so bubble is only as wide as needed)
        bubble = ctk.CTkLabel(
            inner,
            text=msg,
            font=FONT,
            fg_color=bubble_color,
            text_color=fg,
            corner_radius=16,
            anchor=anchor,
            padx=18,
            pady=8,  # Tighter bubble
            wraplength=340
        )
        bubble.pack(anchor=anchor)

        # Auto-scroll to bottom after widget is packed
        self.window.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def quick_action(self, cmd):
        """Handle quick action button clicks"""
        if cmd == "tell me a joke":
            # Directly fetch and display a joke
            joke = self.get_joke()
            self.insert_bubble(joke, "Chatterbox", "bot")
        else:
            # Prompt the user for input
            self.msg_entry.delete(0, "end")
            self.msg_entry.insert(0, f"{cmd} ")
            self.msg_entry.focus()

# run the file
if __name__ == "__main__":
    bot = ChatBot()
    bot.window.mainloop()
