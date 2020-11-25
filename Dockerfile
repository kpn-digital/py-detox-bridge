FROM kpndigital/tox:py27_py35

RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash

ENV NVM_DIR="/root/.nvm"

RUN bash -c ". $NVM_DIR/nvm.sh && nvm install 15.2.1"


WORKDIR /app

CMD ["tox"]
