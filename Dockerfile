FROM python:3.8
ENV PYTHONUNBUFFERED 1

# 이미지 생성 과정에서 실행할 명령어
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# 이미지 내에서 명령어를 실행할(현 위치로 잡을) 디렉토리 설정
COPY . code
WORKDIR code

CMD ["python3", "manage.py", "runserver"]

# 이미지 생성 명령어 (현 파일과 같은 디렉토리에서)
# docker build -t {이미지명} .

# 컨테이너 생성 & 실행 명령어
# docker run --name {컨테이너명} -v $(pwd):/usr/src/app -p 5000:5000 {이미지명}