#!/bin/bash
source /root/bot/Samurai-Sushi_bot/myenv/bin/activate
nohup python3 /root/bot/Samurai-Sushi_bot/bot.py > /dev/null 2>&1 &
