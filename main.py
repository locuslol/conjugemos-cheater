import pyautogui
import pytesseract
from PIL import Image
import google.generativeai as genai
import pyperclip
import time
import re
import keyboard
import tkinter as tk
from tkinter import ttk
import threading
import json
import os

class ConjugationUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conjugemos Cheater")
        self.root.geometry("650x750")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        
        # Variables
        self.monitoring = False
        self.region_set = False
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.input_x, self.input_y = 0, 0
        self.last_text = ""
        self.api_key = None
        self.model = None
        
        # Load or prompt for API key
        self.config_file = "conjugemos_config.json"
        self.load_config()
        
        self.setup_ui()
        
        # Show API dialog if no key exists
        if not self.api_key:
            self.root.after(100, self.show_api_key_dialog)
        else:
            self.configure_gemini()
        
    def load_config(self):
        """Load API key from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
            except:
                pass
                
    def save_config(self):
        """Save API key to config file"""
        config = {'api_key': self.api_key}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
            
    def configure_gemini(self):
        """Configure Gemini with API key"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            return True
        except Exception as e:
            return False
    
    def show_api_key_dialog(self):
        """Show API key input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("API Key Required")
        dialog.geometry("500x280")
        dialog.configure(bg="#0a0a0a")
        dialog.attributes('-topmost', True)
        
        # Close dialog
        dialog.protocol("WM_DELETE_WINDOW", lambda: dialog.destroy())
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (250)
        y = (dialog.winfo_screenheight() // 2) - (140)
        dialog.geometry(f"500x280+{x}+{y}")
        
        # Border effect
        border = tk.Frame(dialog, bg="#00ffaa", bd=0)
        border.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner = tk.Frame(border, bg="#0a0a0a")
        inner.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        tk.Label(inner, text="🔑 Gemini API Key Required", 
                font=("SF Pro Display", 16, "bold"), 
                bg="#0a0a0a", fg="#00ffaa").pack(pady=(25, 10))
        
        tk.Label(inner, text="Get your free API key from:", 
                font=("SF Pro Display", 10), 
                bg="#0a0a0a", fg="#888888").pack()
        
        # Link to get a Gemini API Key
        link = tk.Label(inner, text="https://aistudio.google.com/apikey", 
                       font=("SF Pro Display", 10, "underline"), 
                       bg="#0a0a0a", fg="#0ea5e9", cursor="hand2")
        link.pack(pady=(0, 15))
        
        def open_link(e):
            import webbrowser
            webbrowser.open("https://aistudio.google.com/apikey")
        
        link.bind("<Button-1>", open_link)
        link.bind("<Enter>", lambda e: link.config(fg="#00ffaa"))
        link.bind("<Leave>", lambda e: link.config(fg="#0ea5e9"))
        
        entry_frame = tk.Frame(inner, bg="#16213e", bd=0, highlightthickness=0)
        entry_frame.pack(pady=10, padx=30, fill=tk.X)
        
        api_entry = tk.Entry(entry_frame, font=("SF Pro Display", 11), 
                            bg="#0f1b2e", fg="#ffffff", 
                            insertbackground="#00ffaa",
                            relief=tk.FLAT, bd=0,
                            highlightthickness=0)
        api_entry.pack(pady=12, padx=12, fill=tk.X)
        api_entry.focus()
        
        error_label = tk.Label(inner, text="", 
                              font=("SF Pro Display", 9), 
                              bg="#0a0a0a", fg="#ef4444")
        error_label.pack()
        
        def save_key():
            key = api_entry.get().strip()
            if not key:
                error_label.config(text="⚠️ Please enter an API key")
                return
            
            self.api_key = key
            if self.configure_gemini():
                self.save_config()
                dialog.destroy()
                if hasattr(self, 'log_text'):
                    self.log("✓ API key configured successfully!", "success")
            else:
                error_label.config(text="⚠️ Invalid API key. Please check and try again.")
        
        btn_frame = tk.Frame(inner, bg="#0a0a0a")
        btn_frame.pack(pady=15)
        
        save_btn_bg = tk.Frame(btn_frame, bg="#10b981", bd=0, highlightthickness=0)
        save_btn_bg.pack()
        
        save_btn = tk.Button(save_btn_bg, text="Save & Continue", 
                            command=save_key,
                            font=("SF Pro Display", 11, "bold"),
                            bg="#10b981", fg="#ffffff",
                            activebackground="#059669",
                            relief=tk.FLAT, bd=0,
                            cursor="hand2",
                            padx=25, pady=8,
                            highlightthickness=0)
        save_btn.pack(padx=1, pady=1)
        
        api_entry.bind('<Return>', lambda e: save_key())
        
        dialog.transient(self.root)
        dialog.grab_set()
        
    def animate_startup(self):
        """Fade in animation"""
        self.root.attributes('-alpha', 0.0)
        self.root.update()
        for i in range(0, 11):
            self.root.attributes('-alpha', i / 10)
            self.root.update()
            time.sleep(0.02)
        
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["dragging"] = True
        
    def stop_drag(self, event):
        self.drag_data["dragging"] = False
        
    def do_drag(self, event):
        if self.drag_data["dragging"]:
            x = self.root.winfo_x() + event.x - self.drag_data["x"]
            y = self.root.winfo_y() + event.y - self.drag_data["y"]
            self.root.geometry(f"+{x}+{y}")
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1a2e", height=100)
        header.pack(fill=tk.X, pady=(0, 25))
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg="#1a1a2e")
        header_content.pack(expand=True)
        
        title = tk.Label(header_content, text="⚡ Conjugemos Cheater", 
                        font=("SF Pro Display", 24, "bold"), 
                        bg="#1a1a2e", fg="#00ffaa")
        title.pack(pady=(5, 2))
        
        subtitle = tk.Label(header_content, text="made by locuslol", 
                           font=("SF Pro Display", 11), 
                           bg="#1a1a2e", fg="#666666")
        subtitle.pack(pady=(0, 2))
        
        # API key button - subtle style
        self.api_btn = tk.Button(header_content, text="🔑 Change API Key", 
                                command=self.show_api_key_dialog,
                                font=("SF Pro Display", 9),
                                bg="#16213e", fg="#888888",
                                activebackground="#1a1a2e",
                                activeforeground="#00ffaa",
                                relief=tk.FLAT, bd=0,
                                cursor="hand2",
                                padx=12, pady=4)
        self.api_btn.pack(pady=(5, 0))
        
        # Main container with padding
        container = tk.Frame(self.root, bg="#0a0a0a")
        container.pack(fill=tk.BOTH, expand=True, padx=35, pady=(0, 25))
        
        # Status card with modern design and rounded appearance
        status_card = tk.Frame(container, bg="#16213e", relief=tk.FLAT, bd=0, highlightthickness=0)
        status_card.pack(fill=tk.X, pady=(0, 20))
        
        status_inner = tk.Frame(status_card, bg="#16213e")
        status_inner.pack(pady=18, padx=20)
        
        status_left = tk.Frame(status_inner, bg="#16213e")
        status_left.pack(side=tk.LEFT)
        
        tk.Label(status_left, text="Status", font=("SF Pro Display", 10), 
                bg="#16213e", fg="#888888").pack(anchor=tk.W)
        
        status_row = tk.Frame(status_left, bg="#16213e")
        status_row.pack(anchor=tk.W, pady=(5, 0))
        
        self.status_indicator = tk.Label(status_row, text="●", font=("SF Pro Display", 18), 
                                        bg="#16213e", fg="#ff3366")
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 8))
        
        self.status_label = tk.Label(status_row, text="Idle", 
                                     font=("SF Pro Display", 13, "bold"), 
                                     bg="#16213e", fg="#ffffff")
        self.status_label.pack(side=tk.LEFT)
        
        # Button container for better spacing
        button_container = tk.Frame(container, bg="#0a0a0a")
        button_container.pack(fill=tk.X, pady=(0, 25))
        
        # Buttons
        setup_btn_frame = tk.Frame(button_container, bg="#0ea5e9", bd=0, highlightthickness=0)
        setup_btn_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.setup_btn = tk.Button(setup_btn_frame, text="⚙  Setup Region", 
                                   command=self.setup_region,
                                   font=("SF Pro Display", 13, "bold"),
                                   bg="#0ea5e9", fg="#ffffff",
                                   activebackground="#0284c7",
                                   activeforeground="#ffffff",
                                   relief=tk.FLAT, bd=0,
                                   cursor="hand2", height=2,
                                   highlightthickness=0)
        self.setup_btn.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.setup_btn.bind("<Enter>", lambda e: self.setup_btn.config(bg="#0284c7") if self.setup_btn['state'] == 'normal' else None)
        self.setup_btn.bind("<Leave>", lambda e: self.setup_btn.config(bg="#0ea5e9") if self.setup_btn['state'] == 'normal' else None)
        
        # Start/Stop Buttons
        toggle_btn_frame = tk.Frame(button_container, bg="#10b981", bd=0, highlightthickness=0)
        toggle_btn_frame.pack(fill=tk.X)
        
        self.toggle_btn = tk.Button(toggle_btn_frame, text="▶  Start Monitoring", 
                                    command=self.toggle_monitoring,
                                    font=("SF Pro Display", 13, "bold"),
                                    bg="#10b981", fg="#ffffff",
                                    activebackground="#059669",
                                    activeforeground="#ffffff",
                                    relief=tk.FLAT, bd=0,
                                    cursor="hand2", height=2,
                                    state=tk.DISABLED,
                                    highlightthickness=0)
        self.toggle_btn.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Log section
        log_header = tk.Frame(container, bg="#0a0a0a")
        log_header.pack(fill=tk.X, pady=(0, 12))
        
        log_label = tk.Label(log_header, text="Activity Log", 
                           font=("SF Pro Display", 13, "bold"), 
                           bg="#0a0a0a", fg="#00ffaa")
        log_label.pack(side=tk.LEFT)
        
        self.log_count = tk.Label(log_header, text="0 events", 
                                 font=("SF Pro Display", 10), 
                                 bg="#0a0a0a", fg="#666666")
        self.log_count.pack(side=tk.RIGHT)
        
        # Log frame
        log_outer = tk.Frame(container, bg="#16213e", relief=tk.FLAT, bd=0, highlightthickness=0)
        log_outer.pack(fill=tk.BOTH, expand=True)
        
        log_frame = tk.Frame(log_outer, bg="#16213e")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        scrollbar = tk.Scrollbar(log_frame, bg="#16213e", troughcolor="#0f1b2e",
                                activebackground="#00ffaa", width=12)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, 
                               bg="#0f1b2e", fg="#e0e0e0",
                               font=("Consolas", 9),
                               relief=tk.FLAT, bd=0,
                               yscrollcommand=scrollbar.set,
                               padx=18, pady=18,
                               insertbackground="#00ffaa",
                               selectbackground="#1e3a5f",
                               selectforeground="#ffffff",
                               highlightthickness=0)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Configure text tags for colored output
        self.log_text.tag_config("success", foreground="#10b981", font=("Consolas", 9, "bold"))
        self.log_text.tag_config("error", foreground="#ef4444", font=("Consolas", 9, "bold"))
        self.log_text.tag_config("info", foreground="#00ffaa", font=("Consolas", 9))
        self.log_text.tag_config("warning", foreground="#f59e0b", font=("Consolas", 9))
        self.log_text.tag_config("dim", foreground="#666666", font=("Consolas", 9))
        
        self.event_count = 0
        self.log("🎯 Ready to dominate Conjugemos!", "info")
        self.log("Click 'Setup Region' to get started", "dim")
        
    def log(self, message, tag="normal"):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", "dim")
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.event_count += 1
        self.log_count.config(text=f"{self.event_count} events")
        self.root.update()
        
    def setup_region(self):
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "info")
        self.log("🎯 Starting region setup...", "info")
        self.setup_btn.config(state=tk.DISABLED)
        
        def setup_thread():
            self.log("📍 Hover TOP-LEFT corner in 3 seconds...", "warning")
            time.sleep(3)
            self.x1, self.y1 = pyautogui.position()
            self.log(f"✓ Captured: ({self.x1}, {self.y1})", "success")
            
            self.log("📍 Hover BOTTOM-RIGHT corner in 3 seconds...", "warning")
            time.sleep(3)
            self.x2, self.y2 = pyautogui.position()
            self.log(f"✓ Captured: ({self.x2}, {self.y2})", "success")
            
            self.log("📍 Hover ANSWER INPUT BOX in 3 seconds...", "warning")
            time.sleep(3)
            self.input_x, self.input_y = pyautogui.position()
            self.log(f"✓ Captured: ({self.input_x}, {self.input_y})", "success")
            
            self.region_set = True
            self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "success")
            self.log("🚀 Setup complete! Ready to cheat!", "success")
            self.toggle_btn.config(state=tk.NORMAL)
            self.setup_btn.config(state=tk.NORMAL)
            
            # Activate Start Button
            self.toggle_btn.config(bg="#059669")
            self.root.update()
            
        threading.Thread(target=setup_thread, daemon=True).start()
        
    def toggle_monitoring(self):
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        # Check if API key is configured
        if not self.api_key or not self.model:
            self.log("❌ Cannot start - API key not configured!", "error")
            self.log("Click 'Change API Key' to add your key", "warning")
            self.show_api_key_dialog()
            return
            
        self.monitoring = True
        self.pulse_status_on()
        self.status_label.config(text="Active")
        self.toggle_btn.config(text="⏸  Stop Monitoring", bg="#ef4444", activebackground="#dc2626")
        self.toggle_btn.bind("<Enter>", lambda e: self.toggle_btn.config(bg="#dc2626"))
        self.toggle_btn.bind("<Leave>", lambda e: self.toggle_btn.config(bg="#ef4444"))
        self.setup_btn.config(state=tk.DISABLED)
        
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "success")
        self.log("🔥 Monitoring activated! Let's go!", "success")
        
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        
    def stop_monitoring(self):
        self.monitoring = False
        self.status_indicator.config(fg="#ff3366")
        self.status_label.config(text="Idle")
        self.toggle_btn.config(text="▶  Start Monitoring", bg="#10b981", activebackground="#059669")
        self.toggle_btn.bind("<Enter>", lambda e: self.toggle_btn.config(bg="#059669"))
        self.toggle_btn.bind("<Leave>", lambda e: self.toggle_btn.config(bg="#10b981"))
        self.setup_btn.config(state=tk.NORMAL)
        
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "warning")
        self.log("⏸ Monitoring paused", "warning")
        
    def pulse_status_on(self):
        """Animate status indicator with pulse effect"""
        def pulse():
            colors = ["#10b981", "#059669", "#047857", "#059669", "#10b981"]
            idx = 0
            while self.monitoring:
                self.status_indicator.config(fg=colors[idx % len(colors)])
                idx += 1
                time.sleep(0.3)
        threading.Thread(target=pulse, daemon=True).start()
        
    def monitor_loop(self):
        x = min(self.x1, self.x2)
        y = min(self.y1, self.y2)
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)
        
        while self.monitoring:
            try:
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                text = self.extract_text(screenshot)
                
                if text and text != self.last_text and len(text) > 5:
                    self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "info")
                    self.log(f"📝 Question: {text[:60]}...", "info")
                    
                    tense, subject, verb = self.parse_conjugation(text)
                    
                    if tense and subject and verb:
                        self.log(f"✓ Parsed → {tense} | {subject} | {verb}", "success")
                        
                        conjugated = self.conjugate(tense, subject, verb)
                        
                        # Check if there was an error - don't type errors into the box!
                        if conjugated.startswith("Error:") or "error" in conjugated.lower() or len(conjugated) > 50:
                            self.log(f"❌ API Error: {conjugated}", "error")
                            self.log("⚠️  Skipping typing - check API quota", "warning")
                        else:
                            self.log(f"✨ Answer: {conjugated}", "success")
                            
                            # Type
                            time.sleep(0.2)
                            pyautogui.click(self.input_x, self.input_y)
                            time.sleep(0.2)
                            pyautogui.hotkey('ctrl', 'a')
                            time.sleep(0.1)
                            
                            try:
                                keyboard.write(conjugated, delay=0.08)
                            except:
                                pyautogui.typewrite(conjugated, interval=0.08)
                            
                            self.log("⌨️  Typed successfully!", "success")
                            pyperclip.copy(conjugated)
                    else:
                        missing = []
                        if not tense: missing.append("tense")
                        if not subject: missing.append("subject")
                        if not verb: missing.append("verb")
                        self.log(f"✗ Parse failed - missing: {', '.join(missing)}", "error")
                    
                    self.last_text = text
                    
                time.sleep(0.5)
            except Exception as e:
                self.log(f"⚠️  Error: {str(e)}", "error")
                time.sleep(1)
                
    def extract_text(self, image):
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        text = pytesseract.image_to_string(image, config='--psm 6')
        return text.strip()
        
    def parse_conjugation(self, text):
        print(f"  [DEBUG] === Monitoring Start ===")
        original_text = ' '.join(text.split())
        
        print(f"  [DEBUG] Original text: '{original_text}'")
        
        # Clean text for pattern matching
        text = original_text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        print(f"  [DEBUG] Cleaned text: '{text}'")
        
        tense_patterns = {
            'present perfect': ['present perfect', 'presentperfect'],
            'present': ['present'],
            'preterite': ['preterite', 'preterit'],
            'imperfect': ['imperfect'],
            'future': ['future'],
            'conditional': ['conditional'],
            'subjunctive': ['subjunctive', 'present subjunctive'],
            'past perfect': ['past perfect', 'pluperfect'],
            'future perfect': ['future perfect']
        }
        
        subject_patterns = {
            'ustedes': ['ustedes', 'uds'],
            'nosotros': ['nosotros', 'nosotras'],
            'vosotros': ['vosotros', 'vosotras'],
            'usted': ['usted', 'ud'],
            'ellos': ['ellos', 'ellas'],
            'yo': ['yo', 'yо'],
            'tú': ['tu', 'tú', 'td', 't0', 'tii'],
            'él': ['el', 'él', 'e1'],
            'ella': ['ella', 'efla']
        }
        
        name_and_yo_pattern = r'\w+ y yo'
        name_and_tu_pattern = r'\w+ y t[uú]'
        plural_name_pattern = r'\w+ y \w+'
        
        found_tense = None
        found_subject = None
        found_verb = None
        
        for tense_name, patterns in sorted(tense_patterns.items(), key=lambda x: -len(x[0])):
            for pattern in patterns:
                if pattern in text:
                    found_tense = tense_name
                    break
            if found_tense:
                break
        
        if re.search(name_and_yo_pattern, text):
            found_subject = 'nosotros'
        elif re.search(name_and_tu_pattern, text):
            found_subject = 'ustedes'
        elif re.search(plural_name_pattern, text):
            found_subject = 'ellos'
        
        if not found_subject:
            for subject_name, patterns in subject_patterns.items():
                for pattern in patterns:
                    if pattern in text:
                        found_subject = subject_name
                        print(f"  [DEBUG] Found subject '{found_subject}' from pattern '{pattern}'")
                        break
                if found_subject:
                    break
        
        # Check for standalone names
        if not found_subject:
            # Look for capitalized words that could be names
            words_list = original_text.split()
            tense_keywords = ['Present', 'Perfect', 'Preterite', 'Imperfect', 'Future', 'Conditional', 'Subjunctive', 'Past']
            
            for word in words_list:
                # Skip punctuation and tense keywords
                clean_word = word.strip('»,.:;!?')
                if not clean_word or clean_word in tense_keywords:
                    continue
                    
                # Check if it's a capitalized word (likely a name)
                if clean_word[0].isupper() and len(clean_word) > 1:
                    found_subject = 'él'
                    print(f"  [DEBUG] Detected standalone name '{clean_word}' → using 'él' (3rd person singular)")
                    break

        words = text.split()
        if 'to' in words:
            to_index = words.index('to')
            verb_words = []
            for i in range(to_index + 1, len(words)):
                word = words[i]
                # Stop at common indicators of end of verb phrase
                if word in ['reflexive', 'pronominal', 'irregular', 'stem', 'changing', 'not', 'no']:
                    break
                # Stop at parentheses content
                if '(' in word or ')' in word:
                    break
                verb_words.append(word)
            
            if verb_words:
                found_verb = ' '.join(verb_words[:3])
        
        if not found_verb and len(words) > 0:
            stopwords = ['the', 'a', 'an', 'to', 'and', 'or', 'but', 'reflexive', 'pronominal', 'not', 'no']
            potential_verbs = [w for w in words if w not in stopwords and len(w) > 1]
            
            for tense_patterns_list in tense_patterns.values():
                potential_verbs = [v for v in potential_verbs if v not in tense_patterns_list]
            
            for subject_patterns_list in subject_patterns.values():
                potential_verbs = [v for v in potential_verbs if v not in subject_patterns_list]
            
            if potential_verbs:
                found_verb = potential_verbs[-1]
        
        return found_tense, found_subject, found_verb
        
    def conjugate(self, tense, subject, verb):
        prompt = f"""You are a Spanish conjugation expert. Conjugate the verb '{verb}' in {tense} tense for the subject '{subject}'.

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
        
        try:
            response = self.model.generate_content(prompt)
            conjugated = response.text.strip()
            conjugated = re.sub(r'["\'\*\.]', '', conjugated).strip()
            conjugated = ' '.join(conjugated.split())
            return conjugated
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        pytesseract.get_tesseract_version()
    except:
        print("ERROR: Tesseract OCR is not installed.")
        print("\nPlease install it:")
        print("- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("- Mac: brew install tesseract")
        print("- Linux: sudo apt-get install tesseract-ocr")
        exit(1)
    
    app = ConjugationUI()
    app.run()