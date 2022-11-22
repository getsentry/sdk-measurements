FROM europe-west3-docker.pkg.dev/sentry-st-testing/public/sentry-vegeta:cd30862833bc1d7aa3403b694393935f5a3aa4b9

WORKDIR /work

# We only care about tests, but this is just easier for now
COPY . .
