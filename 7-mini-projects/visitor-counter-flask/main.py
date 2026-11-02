# app.py
from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime
import logging
import os

app = Flask(__name__)

DB = os.environ.get('VISIT_DB', 'visits.db')

# Настроим логирование в консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger("visits")

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_visit(ip, ua, ts):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (ip, user_agent, timestamp) VALUES (?, ?, ?)", (ip, ua, ts))
    conn.commit()
    conn.close()

def get_client_ip():
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr or ''

@app.route('/')
def index():
    ip = get_client_ip()
    ua = request.headers.get('User-Agent', '<unknown>')
    ts = datetime.utcnow().isoformat()
    save_visit(ip, ua, ts)
    logger.info(f"VISIT -> IP={ip} UA={ua} TIME={ts}")
    # сразу показываем IP, без уведомлений
    return render_template_string("""
        <h2>Ваш IP зафиксирован</h2>
        <p>IP: <b>{{ip}}</b></p>
        <p>Время (UTC): {{ts}}</p>
    """, ip=ip, ts=ts)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
