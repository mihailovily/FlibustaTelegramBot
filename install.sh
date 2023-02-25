#!/bin/bash
# Ask the user for their name

echo Впиши токен telegram бота

read vartoken

echo $vartoken > settings/tken.txt

echo Токен записан

echo Впиши ID админа

read varadmin

echo $varadmin > settings/admn.txt

echo ID админа записан

echo Установка зависимостей

pip install -r requirements.txt

echo Зависимости установлены

echo Для запуска воспользуйтесь командойэ
echo python3 main.py
