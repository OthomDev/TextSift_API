FROM python:3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
RUN python -m spacy download en_core_web_sm
EXPOSE 5000
CMD ["python", "app.py"]