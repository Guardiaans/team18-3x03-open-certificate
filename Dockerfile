# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}
ARG INSTALL_NODE_VERSION=${INSTALL_NODE_VERSION:-NODE_VERSION_NOT_SET}

FROM node:${INSTALL_NODE_VERSION}-buster-slim AS node
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster AS builder

ARG FLASK_APP
ARG FLASK_DEBUG
ARG FLASK_ENV
ARG DATABASE_URL
ARG GUNICORN_WORKERS
ARG LOG_LEVEL
ARG SEND_FILE_MAX_AGE_DEFAULT
ARG SECRET_KEY
ARG SECURITY_PASSWORD_SALT
ARG JWT_KEY
ARG RECAPTCHA_SITE_KEY
ARG RECAPTCHA_SECRET_KEY
ARG RECAPTCHA_VERIFY_URL
ARG MAIL_DEFAULT_SENDER
ARG MAIL_PASSWORD

WORKDIR /app

COPY --from=node /usr/local/bin/ /usr/local/bin/
COPY --from=node /usr/lib/ /usr/lib/
# See https://github.com/moby/moby/issues/37965
RUN true
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY requirements requirements
RUN pip install --no-cache -r requirements/prod.txt

COPY package.json ./
RUN npm install

COPY webpack.config.js autoapp.py ./
COPY opencert opencert
COPY assets assets
RUN npm run-script build

# ================================= PRODUCTION =================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster as production

ARG FLASK_APP
ARG FLASK_DEBUG
ARG FLASK_ENV
ARG DATABASE_URL
ARG GUNICORN_WORKERS
ARG LOG_LEVEL
ARG SEND_FILE_MAX_AGE_DEFAULT
ARG SECRET_KEY
ARG SECURITY_PASSWORD_SALT
ARG JWT_KEY
ARG RECAPTCHA_SITE_KEY
ARG RECAPTCHA_SECRET_KEY
ARG RECAPTCHA_VERIFY_URL
ARG MAIL_DEFAULT_SENDER
ARG MAIL_PASSWORD

WORKDIR /app
RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid
ENV PATH="/home/sid/.local/bin:${PATH}"

COPY --from=builder --chown=sid:sid /app/opencert/static /app/opencert/static
COPY requirements requirements
RUN pip install --no-cache --user -r requirements/prod.txt

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

COPY . .



USER root
RUN chown -R sid:sid /app/opencert/metadataUploads
RUN chown -R sid:sid /app/opencert/uploads
USER sid


RUN flask db init
RUN flask db migrate
RUN flask db upgrade

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]


# ================================= DEVELOPMENT ================================
FROM builder AS development
RUN pip install --no-cache -r requirements/dev.txt
EXPOSE 2992
EXPOSE 5000
CMD [ "npm", "start" ]
