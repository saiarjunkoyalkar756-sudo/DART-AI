import uvicorn, webbrowser, threading, time

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    print("\n\033[95m  DarkAI is starting...\033[0m")
    print("\033[96m  → http://localhost:8000\033[0m\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
