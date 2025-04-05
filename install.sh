#!/bin/bash

echo Впиши токен telegram бота

read vartoken

mkdir settings

echo $vartoken >> settings/token.txt

echo Токен записан

echo Впиши ID админа

read varadmin

echo $varadmin >> settings/admin.txt

echo ID админа записан

echo Установка зависимостей

poetry update

echo Зависимости установлены

echo Для запуска воспользуйтесь командой
echo poetry run python3 main.py
