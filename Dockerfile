FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

RUN curl -o mupdf.tar.gz https://mupdf.com/downloads/mupdf-1.11-source.tar.gz
RUN tar -xf mupdf.tar.gz
COPY ./mupdf/Makefile /app/mupdf-1.11-source
RUN cd mupdf-1.11-source && make HAVE_X11=no HAVE_GLFW=no prefix=/usr/local install
RUN cd ..
RUN git clone https://github.com/rk700/PyMuPDF.git --depth 1 -b 1.11.0
COPY ./mupdf/setup.py /app/PyMuPDF/
RUN cd PyMuPDF && python setup.py install

COPY ./app /app
COPY ./resources/nginx/nginx.conf /etc/nginx/conf.d/

RUN pip3 install -U setuptools pip
RUN pip3 install -r /app/requirements.txt
