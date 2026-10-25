@echo off
echo Starting embedding generation...
python create_and_save_embeddings.py
echo.
echo Embedding generation complete!
echo.
echo You can now search using:
echo python search_embeddings.py "your query here"
pause
