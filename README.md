# Local Development
* * *
image build commend

     docker build -t {이미지명} .

image run commend

    docker run --name {컨테이너명} -v $(pwd):/usr/src/app -p 5000:5000 {이미지명}