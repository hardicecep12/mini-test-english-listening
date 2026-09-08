import os
import sys
import json
import time
import socket
import threading
import subprocess
import webbrowser

# Tambahkan import modul tersembunyi Streamlit di sini
import streamlit.web.cli as stcli
import streamlit.runtime.scriptrunner.magic_funcs
import streamlit.runtime.caching.storage.dummy_cache_storage

PORT = 8501

def wait_and_open_app():
    url = f"http://localhost:{PORT}"
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', PORT)) == 0:
                break
        time.sleep(0.5)
    
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    opened = False
    for path in edge_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f"--app={url}"])
            opened = True
            break
            
    if not opened:
        webbrowser.open(url)

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_dir = getattr(sys, '_MEIPASS', os.path.join(os.path.dirname(sys.executable), "_internal"))
        if not os.path.exists(os.path.join(base_dir, "app.py")):
            base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    os.chdir(base_dir)
    app_path = os.path.join(base_dir, "app.py")

    threading.Thread(target=wait_and_open_app, daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        f"--server.port={PORT}",
        "--server.headless=true",
        "--server.fileWatcherType=none",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false"
    ]
    sys.exit(stcli.main())
