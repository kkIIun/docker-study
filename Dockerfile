FROM python:3.8

# 이미지 생성 과정에서 실행할 명령어
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
COPY . /usr/src/app

WORKDIR ./apiStudy

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

# 이미지 생성 명령어 (현 파일과 같은 디렉토리에서)
# docker build -t {이미지명} .

# 컨테이너 생성 & 실행 명령어
# docker run --name {컨테이너명} -v $(pwd):/usr/src/app -p 5000:5000 {이미지명}