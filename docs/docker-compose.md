# `docker-compose`: Overview and Best Practices


## Special Labels

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

#### ⚠️ Note: this label is not implemented yet! ⚠️

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
