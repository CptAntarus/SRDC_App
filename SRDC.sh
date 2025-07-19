#!/bin/bash


echo "Script Activated"

export SRDC_CREDS_PATH="/c/VS_Code/Python/Kivy_Testing/SRDC_Creds.json"

source /c/VS_Code/Python/Kivy_Testing/KivEnv/Scripts/activate

python /c/VS_Code/Python/Kivy_Testing/SRDC_main.py
