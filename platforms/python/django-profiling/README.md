# Environment: django-profiling

Env spec: [`env-spec.yaml`](./env-spec.yaml)

This environment allows to compare overhead of an added profiling middleware in a Django app that uses a Postgres database.

There are two tests that we run here:

* [`test-run-vegeta-disable-profiling.sh`](./test-run-vegeta-disable-profiling.sh) - profiling is disabled.
* [`test-run-vegeta-enable-profiling.sh`](test-run-vegeta-enable-profiling.sh) - profiling is enabled.
