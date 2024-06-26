FROM python:3.11.6-alpine

WORKDIR /home/application

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./CourseManagementService api/

COPY ./CourseManagementService/manage.py .

COPY ./CourseManagementService .

COPY ./entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
