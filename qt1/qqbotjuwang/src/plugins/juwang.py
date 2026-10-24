# Copyright (c) 2026 陌酯秋_C2H8O4
# SPDX-License-Identifier: MIT
import sqlite3
from datetime import datetime
#依旧导入
import httpx
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment
from nonebot.rule import to_me
#这里是一些小游戏要的库
import random
from nonebot import on_command
#version:0.4.27
#这里写开发者和管理员权限..............
Boot_ID = 3669772451 #最高权限
Admin_ID = 3482687304,2056117867 #管理员权限
User_ID = 0 #内测用户ID
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
messagen = on_message(rule=to_me(),priority=10,block=False)
@messagen.handle()
async def handle(event):
  async with httpx.AsyncClient(timeout=300) as client:
    user_msg = event.get_plaintext().strip()
    if not user_msg:
      await messagen.finish("你可以@我加上你想说的话,这样就可以聊天了喵；或者@我并加上/猜数字,就可以玩猜数字游戏了喵")

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

#这里是小游戏层
#数字游戏1.0喵
#modelver:1.0
game_DATA = {}
game_numberBoom = on_command("猜数字",rule=to_me(),priority=1,block=True)

@game_numberBoom.handle()
async def handle_guess(event:MessageEvent):
  game_DATA[event.group_id] = random.randint(1,100)
  await game_numberBoom.send("开始猜数字游戏吧,从1-100里面猜数字,谁猜中了就可以向任意一个群友提条件喵")
  print(event.group_id,game_DATA[event.group_id],flush=True)
@game_numberBoom.got("guess")
async def cheakgroup_guess(event:MessageEvent):
  ccc = game_DATA[event.group_id]
  bbb = str(event.message).strip()

  if bbb.isdigit():
    aaa = int(bbb)
    if aaa>ccc:
      await game_numberBoom.send("猜大了喵,尝试猜小一点喵")
    elif aaa<ccc:
      await game_numberBoom.send("猜小了喵,尝试猜大一点喵")
    else:
      await game_numberBoom.finish(f"猜对了喵,答案就是{game_DATA[ccc]} 喵")
#写完ver 0.4.27的主要部分了