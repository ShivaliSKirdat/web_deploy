FROM python:3.9
#MAINTAINER Shivam Mitra "shivamm389@gmail.com" # Change the name and email address
COPY . /app/
#COPY main.py definition.py /app/
WORKDIR /app
RUN pip install flask pytest flake8 # This downloads all the dependencies
CMD ["python", "main.py"]
