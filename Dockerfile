# Usa un'immagine base di Python
FROM python:3.8

# Imposta una directory di lavoro
WORKDIR /app

# Copia i file necessari nell'immagine
COPY . /app

# Installa le dipendenze
RUN pip install -r requirements.txt

# Espone la porta 8501 (porta predefinita di Streamlit)
EXPOSE 8501

# Comando per eseguire l'applicazione
CMD ["streamlit", "run", "app.py"]

