FROM node:lts-alpine

ENV NDOE_ENV production

ARG SENTRY_SDK_VERSION=master
ENV SENTRY_SDK_VERSION=$SENTRY_SDK_VERSION

ARG SENTRY_PORT_BACKEND=3000
ENV SENTRY_PORT_BACKEND=$SENTRY_PORT_BACKEND

ARG SENTRY_DSN=""
ENV SENTRY_DSN=$SENTRY_DSN

WORKDIR /express-simple

COPY . .

RUN yarn install

EXPOSE ${SENTRY_PORT_BACKEND}

CMD ["npm", "start"]
# ENTRYPOINT ["sh", "-c", "echo 'Heeyyyy, sleeping'; while true; do echo yo; sleep 1; done"]
