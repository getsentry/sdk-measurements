# Environment Spec File: `env-spec.yaml`

The environment spec file is the place where you can control things like test discovery mechanism, metric reporting strategies, remote environments, and so on.

The file should be located at the root directory of the given environment, and is named `env-spec.yaml`.

## Fields

| Option                 | Description                                                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                 | Environment name                                                                                                                     |
| `test_file_cmd`        | **optional**. Template defining how to run a discovered file-based test. Defaults to `./${test_file}`.                               |
| `test_dir_cmd`         | **optional**. Template defining how to run a discovered directory-based test. Defaults to `./${test_dir}/test-entrypoint.sh`.        |
| `watch_containers`     | **optional**. A mapping between test names and a list of container names that we want to include in the report after the test.       |
| `remote`               | **optional**. [Remote environment](#remote-environments) specification.                                                              |
| `remote.repo`          | Git-clonable URL of the remote repository.                                                                                           |
| `remote.revision`      | **optional**. Repository revision (can be a branch, tag, or a commit SHA). If nothing is specified, the default branch will be used. |
| `remote.path`          | **optional**. Environment path inside the reporitory, defaults to `/`                                                                |
| `grafana.org_id`       | **optional**. Grafana organization ID (string), defaults to `1`                                                                      |
| `grafana.dashboard_id` | **optional**. Grafana dashboard ID (string). An environment might have a separate dashboard in Grafana, here you can specify its ID. |


### Example: Python Environment

```yaml
---
# Environment name
name: django-react-app

# Every discovered file will be treated as a Python script
test_file_cmd: "python ${test_file}"

# We will expect a "test-entrypoint.py" script in every discovered test directory
test_dir_cmd: "python ${test_dir}/test-entrypoint.py"

# We'll be generating dashboard links in the given tests for the given containers
watch_containers:
  # Test name
  "test-run-vegeta-rate-1.0.sh":
    # Container name that will be "watched" for the given test
    - django-rate-1p0
  "test-run-vegeta-rate-0.1.sh":
    - django-rate-0p1

# This environment has a custom dashboard
grafana:
  org_id: '234'
  dashboard_id: 'cJ7GvAC7k'
```


## Remote Environments


Sometimes it's preferred to store the environment files in a separate repository, and the remote environment feature can help here. If `remote` attribute is present in the env spec, the repository specified in `remote.repo` will be checked out and used as the testing environment.

### Example: Remote Environment

```yaml
---
name: sdk-remote

remote:
  # Cloneable URL
  repo: https://github.com/getsentry/sentry-python
  # Revision (branch/tag/commit SHA)
  revision: test/sdk-measurements
  # Path inside the repository
  path: ./perf-measurements
```
