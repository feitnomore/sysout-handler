FROM python:2.7

LABEL maintainer="Marcelo Feitoza Parisi (marcelo@feitoza.com.br)"

# Copy Helpers
RUN mkdir -p /usr/src/app/helpers
COPY helpers/__init__.py /usr/src/app/helpers/
COPY helpers/globalholders.py /usr/src/app/helpers/
COPY helpers/kubeclient.py /usr/src/app/helpers/

# Copy Application
WORKDIR /usr/src/app
COPY sysout-handler.py ./

# Install Deps
RUN pip install kubernetes
RUN pip install urllib3

CMD [ "python", "-u", "./sysout-handler.py" ]
