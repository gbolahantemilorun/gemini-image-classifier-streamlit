FROM python:3.11.4
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run app.py