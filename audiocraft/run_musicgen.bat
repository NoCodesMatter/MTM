@echo off
set HF_HOME=E:\MTMusic\hf_cache
set TORCH_HOME=E:\MTMusic\torch_cache
set TEMP=E:\MTMusic\temp
set TMP=E:\MTMusic\temp

call conda activate MusicGenEnv
python test_musicgen.py
pause
