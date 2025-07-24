#!/bin/bash

echo "Script Activated"

# Windows: $env:SRDC_CREDS_PATH = "C:\VS_Code\Python\Kivy_Testing\SRDC_Creds.json"
export SRDC_CREDS_PATH="/c/VS_Code/Python/Kivy_Testing/SRDC_Creds.json"

echo "Activating Env..."
source /c/VS_Code/Python/Kivy_Testing/KivEnv/Scripts/activate

echo "Beginning Clean..."
python /c/VS_Code/Python/Kivy_Testing/SRDC_ResetDBs.py
