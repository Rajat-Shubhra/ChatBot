import tkinter as tk
import google.generativeai as genai
import threading

## Gemini API
genai.configure(api_key="AIzaSyCyDN1raGh7WK2wUrt9fgMcywxypHlQMK4")

path = 'Crustdata_Documentation.txt'
with open(path, "r+", encoding="utf-8") as f:
    content = f.read()

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {"role": "user", "parts": content},
    ]
)
#

## Tkinter UI for Chat Bot
root = tk.Tk()
root.title("Crustdata Chat Bot")
root.resizable(width=False, height=False)
root.config(bg="#171717")

conversation_text = tk.Text(root, wrap="word", height=20, width=70)
conversation_text.pack(padx=10, pady=10)
conversation_text.config(bg="#232423", fg="white")

user_input = tk.Entry(root, width=70)
user_input.pack(padx=10, pady=(0, 10))
user_input.config(bg="#232423", fg="white")
user_input.config(insertbackground="white")
#

def display_loading():
    conversation_text.insert(tk.END, "Bot: Loading...\n", "loading")
    conversation_text.see(tk.END)

def send_message():
    user_text = user_input.get().strip()
    if not user_text:
        return
    
    conversation_text.insert(tk.END, f"User: {user_text}\n", "user")
    user_input.delete(0, tk.END)
    conversation_text.see(tk.END)
    
    display_loading()
    
    def get_response():
        b = "\n if the above Question is not related to the documentation then please say 'Sorry, I can only answer questions related to Crustdata services.', but if it is any kind of greatings great them and ask how may i help you"
        
        response = chat_session.send_message(user_text + b)
        
        conversation_text.delete("end-2l", "end-1c")  # Remove loading message
        conversation_text.insert(tk.END, f"Bot: {response.text}\n\n", "bot")
        conversation_text.see(tk.END)
    
    threading.Thread(target=get_response).start()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=(0, 10))
send_button.config(bg="#232423", fg="white")

root.bind("<Return>", lambda event: send_message())

root.mainloop()
