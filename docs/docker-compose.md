# `docker-compose`: Overview and Best Practices

Generally, [`docker-compose`](https://docs.docker.com/compose/) is a tool for defining and running multi-container applications. We use `docker-compose` format to define our testing environments because its development-centric approach allows us to test/run apps both locally and in the cloud.

Links:
* [More about `docker-compose`](https://docs.docker.com/compose/)
* [Compose file reference](https://docs.docker.com/compose/compose-file/)

## How We Run Compose-based Loads

We currently use Kubernetes to run our workloads. To convert `docker-compose` services to Kubernetes resources, we use a tool called [`kompose`](https://kompose.io/) when preparing a test run.

Because of the conversion, not all Compose features are currently supported, see the conversion/compatibility matrix for more details:  https://kompose.io/conversion/

## Special Labels

Our testing infrastructure supports a set of custom (non-standard) labels that can be put on the service definitions in Compose files.

### `sdk-measurements.sentry.io/main`

This label is used to mark the container (service) as the "main" one for the given environment. The main container for a test is the one that controls the lifetime of the test: as soon as the main container terminates, the whole test terminates. It is also watched directly by Argo Workflows, meaning that the container's logs can be directly watched from the Argo's UI.

A valid value is `"1"` (as a string), which is considered as a "true" value. Any other value will be interpreted as "false".

**Example:**

```yaml
services:
  # This service/container is marked as the main one
  vegeta:
    labels:
      sdk-measurements.sentry.io/main: "1"
```

### `sdk-measurements.sentry.io/only-for-tests`

This label can be used to signal the system that the corresponding service should be started only for a specific set of tests in the environment. For example, if a certain service is used only for one test out of ten in the environment, it would be reasonable to indicate that using this label to save some resources.

A valid value is a comma-separated list of test names.

**Example:**

```yaml
services:
  # This container will only be started for two tests: "test-profiling-enabled.sh" and "test-profiling-enabled-with-crash.sh".
  django-enable-profiling:
    labels:
      sdk-measurements.sentry.io/only-for-tests: "test-profiling-enabled.sh,test-profiling-enabled-with-crash.sh"
```

## Computing Resources

You can specify how much resources (CPU and memory) you want to allocate for your service ("reservations"), and what would be the limit ("limits") for the resource in question.

More information about computing resources can be found here: https://docs.docker.com/compose/compose-file/deploy/#resources

**Example:**

```yaml
services:
  vegeta:
    deploy:
      resources:
        # These are guaranteed (reserved) resources
        reservations:
          cpus: '0.5'
          memory: '50M'
        # These are the limits: the container won't be able to use more than that
        limits:
          cpus: '1'
          memory: '100M'
```
