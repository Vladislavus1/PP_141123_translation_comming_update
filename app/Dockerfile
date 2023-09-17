FROM python
WORKDIR /app
COPY . .
RUN apt update
RUN apt install nano
RUN pip install -r requirements.txt
EXPOSE 8000