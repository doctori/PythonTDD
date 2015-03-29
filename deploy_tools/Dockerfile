FROM debian
 RUN apt-get update
 RUN apt-get install -y python3.2
 RUN apt-get install -y python3-pip
 RUN apt-get clean all
 RUN pip-3.2 install django==1.7.4
 RUN pip-3.2 install gunicorn==18.0
 RUN pip-3.2 install wsgiref==0.1.2
 
