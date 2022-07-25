# SDK Performance Measurements: Documentation <!-- omit in toc -->

This documentation is also available on [GitHub Pages](https://getsentry.github.io/sdk-measurements/).

## Table of Contents <!-- omit in toc -->

- [Preparing Environment](#preparing-environment)
  - [Environment: Structure and Contents](#environment-structure-and-contents)
  - [Test Cases: Discovery, Format, and Execution](#test-cases-discovery-format-and-execution)
  - [What services can be used by the test?](#what-services-can-be-used-by-the-test)
- [Anatomy of a Test Run](#anatomy-of-a-test-run)
- [Starting a New Run](#starting-a-new-run)
- [Links](#links)

## Preparing Environment

A testing environment is basically a set of container images that run together, plus a set of tests that run in one of the containers. For example, the simplest Python environment may consist of a Python-based image and a set of Python test scripts, where each script runs to completion. More specifically, each environment is a [`docker-compose`](https://docs.docker.com/compose/)-based project with some additional rules on how to discover tests and aggregate the results.

### Environment: Structure and Contents

Every environment is defined in a separate directory, and belongs to a platform. For example, all Python environments are located in [/platforms/python](/platforms/python/) directory.

Important files in the environment directory:

* [`env-spec.yaml`](./env-spec.md) - **required** Environment specification file that contains various environments settings, e.g. those that control test discovery. Find more about it [on a dedicated page](./env-spec.md).
* `docker-compose.yaml` -- [Compose](https://docs.docker.com/compose/compose-file/) configuration file where you define images/containers for your environment. If does not exist, a basic `docker-compose` file will be implicitly created and used for building the environment, and the system will expect a Dockerfile in the root of the environment. By default, the first service (container) listed in the Compose file will be used as the "main" container that will be controlling the test flow, i.e., the test will be considered as finished when the main container finishes.
* [`query-spec.yaml`](./query-spec.md) - Query/report specification file, controls what kind of InfluxDB aggregation queries will be run over the data after the test(s).

### Test Cases: Discovery, Format, and Execution

Test discovery is the process of finding test entry points in the environment. Two types of test formats are currently supported: file-based and directory-based tests.

1. **File-based tests**

    All *files* that start with `test-` prefix in the environment root are treated as file-based tests. This type of tests is suitable e.g. for simple run-to-completion tests that don't have too many dependencies.

    To know how to execute the given test, the system should figure out *the entrypoint command*. To do that, the system takes [`test_file_cmd` attribute](./env-spec.md#fields) from the env spec, treats as a template, and replaces `${test_file}` variable with the base name of the discovered test. By default, `./${test_file}` value of `test_file_cmd` is used, which allows to run executable files with a valid shebang.


2. **Directory-based tests**

    All *directories* that start with `test-` prefix in the environment root are treated as file-based tests. This type of tests allows the user, for example, to set up a performance test for a webapp with a non-trivial file structure.

    The execution entrypoint is built via [`test_dir_cmd` attribute](./env-spec.md#fields), with the default value of `./${test_dir}/test-entrypoint.sh`. `${test_dir}` will be replaced with the base name of the discovered test directory.

### What services can be used by the test?

**Build time**

The following environment variables can be used in `docker-compose.yaml` file:

* `SENTRY_SDK_VERSION` - Contains the SDK version that was passed as the run input by the user.

**Execution time**

The following environment variables can be used in the tests:

* `SENTRY_DSN` - Sentry DSN that points to a local relay-compatible ingestion endpoint. Can be used as a sink when sending events from the SDK.
* `STATSD_HOST` - Hostname (IP address is also allowed) a local Statsd server, where you can send custom metrics from your test.
* `STATSD_PORT` - Port of the Statsd server.


## Anatomy of a Test Run

A run for the given environment consists of the three main stages:

1. Preparing the environment

   The system will build all container images specified in `docker-compose.yaml` and push them to the internal registry, and also [discover the tests](#test-cases-discovery-and-format) in the environment.

2. Running tests

   For every discovered tests, all containers specified in `docker-compose.yaml` will be started, and then the test entrypoint is executed.

3. Collecting results

   After every test, the system aggregates runtime metrics (e.g. CPU, memory) based on the queries specified in the [query spec](./query-spec.md) file. Also, links to InfluxDB dashboards (that basically contain the raw test data) will be printed in one of the final steps.

## Starting a New Run

Assuming your environment is ready, let's start a new run.


1. Make sure that the files of the environment(s) you want to test are pushed to this repository. It doesn't have to be the `main` branch, though: if you're iterating on seomthing, feel free to push your changes to a new branch, just don't forget to specify it in the workflow parameters in the next step.

2. Go to https://run.testa.getsentry.net/ (it is our self-hosted instance of Argo Workflows), click on `+ Submit New Workflow` button, and pick the workflow called `sdk-measurements`.
   About the parameters you can configure:

   * `sdk_measurements_revision` - If you want to use a non-default branch of the `sdk-measurements` repository, you can set `sdk_measurements_revision` parameter to the revision of your choice.

   * `platform` - Platform of the environment(s) you want to test, e.g. "python".

   * `sentry_sdk_version` - The version (revision) of the SDK you want to test. It will be passed to the environment's build stage and can be used to e.g. install a specific SDK version into your testing image.

   * `environments` - A comma separated list of environments that you want to test. If `__all__` is given, the workflow will execute for all enviroments.

   * `comment` - Additional comment for informational purposes: who/why starts the workflow, optional.

    After you update the parameters, it’ll look like this:

    <p align="center">
    <img src="https://user-images.githubusercontent.com/1120468/180484993-c4f44cfc-519c-423e-9c7b-bef94ad9f2b3.png" width="80%">
    </p>

1. Click `+ Submit`. The workflow will start, triggering a redeployment of relevant components first, using the configuration from your branch. Then, when everything is redeployed, the test will start. Argo will display an execution graph that might looks like this:

    <p align="center">
    <img src="https://user-images.githubusercontent.com/1120468/180477872-aab0680b-de08-4b26-8d14-f541ca573fbd.png" width="80%">
    </p>

    You can click on any node to get more info about the steps, read standard output, etc.


1. After the test is done, you can find the link to the InfluxDB dashboard (containing raw time series data of the run) in the "collect-results" step:


    <p align="center">
    <img src="https://user-images.githubusercontent.com/1120468/180487371-ced4f6a5-82ab-4b39-9f56-03ce6b8e8039.png" width="80%">
    </p>

    If you follow the link, here's how the dashboard might look like:

    <p align="center">
    <img src="https://user-images.githubusercontent.com/1120468/180487466-9f287809-1b2b-48f1-ad69-b0661be704ac.png" width="80%">
    </p>


1. You can also get a static report with aggregated stats. At the moment we generate an HTML report and upload it to Google Cloud Storage. To find the link of the report, check the output of the "generate-html-report" step:

    <p align="center">
    <img src="https://user-images.githubusercontent.com/1120468/180487570-c2dc2d6c-f30d-49db-bb97-933ef0b68058.png" width="80%">
    </p>

## Links
* [Environment specification file](./env-spec.md)
* [Query specification file](./query-spec.md)
