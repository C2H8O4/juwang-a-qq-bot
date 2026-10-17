# Copyright (c) 2026 陌酯秋_C2H8O4
# SPDX-License-Identifier: MIT
import sqlite3
from datetime import datetime
#依旧导入
import httpx
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment
from nonebot.rule import to_me
#version:0.2.15
#疑似这里写配置?/
OLLAMA_URL = "http://127.0.0.1:11434/api/chat" #OLLAMA的地址喵
MODEL_NAME = "juwang:latest"#这是名字橘望
DB_PATH = r"C:\Users\win10\Desktop\qt1\moment.db"
#=================疑似配置写完了///
#开始写sqlite3建表吧
cx = sqlite3.connect(r"C:\Users\win10\Desktop\qt1\moment.db")
cu = cx.cursor()
cu.execute("""
    CREATE TABLE IF NOT EXISTS history(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT NOT NULL,
      group_id TEXT,
      message TEXT NOT NULL,
      reply TEXT NOT NULL,
      create_time TEXT NOT NULL
    )
""" )
cx.commit()
cx.close()
#NONEBot部分, 然后导入httpx进ollama>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<
messagen = on_message(rule=to_me())
@messagen.handle()
async def handle(event):
  async with httpx.AsyncClient(timeout=300) as client:
    user_msg = event.get_plaintext().strip()
    if not user_msg:
      await messagen.finish("你想说什么喵～")


    payload = {
    "model": MODEL_NAME,
    "messages": [{"role": "user", "content": user_msg}],
    "stream": False
}
      
    
    httpx1 = await client.post(OLLAMA_URL,json=payload)
    httpx2 = httpx1.json()["message"]["content"]
    httpx1.raise_for_status()

  #存库。。。。。。
  cx = sqlite3.connect(DB_PATH)
  cu = cx.cursor()
  cu.execute(
        "INSERT INTO history (user_id, group_id, message, reply, create_time) VALUES (?, ?, ?, ?, ?)",
        (str(event.user_id), str(event.group_id) if hasattr(event, 'group_id') else None, user_msg, httpx2, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
  cx.commit()
  cx.close()

  await messagen.finish(httpx2)