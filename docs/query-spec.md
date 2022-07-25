# Query Spec File: `query-spec.yaml`

(to be moved to https://github.com/getsentry/test-factory-utils/tree/main/stats-collector)

Query specification file (`query-spec.yaml`) is used to define aggregations queries to run at the end of the test, and as used as input for the [stats-collector script](https://github.com/getsentry/test-factory-utils/tree/main/stats-collector).

While the test is running, all sorts of runtime data is collected: system metrics like CPU and RAM, but also custom metrics emitted by the load tester or by the app under load. All those metrics are stored in [InfluxDB](https://github.com/influxdata/influxdb) (a time series database), and can be checked after the test via Grafana. However, having too much raw data might be unwieldy for final reports that are generated at the end of the tests. Since most of the time users care mostly about data aggregations (mean, max, percentiles), it is now possible to specify and calculate those aggregations via the query spec file.

[stats-collector](https://github.com/getsentry/test-factory-utils/tree/main/stats-collector) takes the query-spec file as input, renders query templates, executes the queries, and then saves the output which later becomes the part of the run report.

## Fields

| Option                               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metrics`                            | A dictionary where keys are user-specified metric/query IDs, and values are query descriptors.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `metrics.<METRIC_ID>`                | A dictionary that defines a set of aggregation queries to generate for a certain metric ID.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `metrics.<METRIC_ID>.flux_query`     | A query template, written with [Flux query language](https://docs.influxdata.com/influxdb/v2.3/query-data/flux/). The following placeholders (variables) can be used: <br><ul><li>`{bucket}` - will be replaced with the relevant InfluxDB bucket. </li> <li>`{start}, {stop}` - will be replaced with the start and stop timestamp of the test.</li> <li>`{filters}` - all generated filters will come here. Do not remove it unless you're now what you're doing!</li> <li>`{quantiles}` - quantile/aggregation-specific generated code will go here.</li></ul> |
| `metrics.<METRIC_ID>.args`           | A dictionary definings query template inputs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `metrics.<METRIC_ID>.args.filters`   | A dictionary that defines a set of string key-value filters to be applied as part of the query.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `metrics.<METRIC_ID>.args.quantiles` | A list of aggregations and quantiles to be applied. One query will be generated and executed for every specified aggregations. Allowed list values: `min`, `max`, `median`, `mean`, and also floating point values between 0.0 and 1.0 to represent quantiles.                                                                                                                                                                                                                                                                                                    |


## Example

```yaml
metrics:
  # We want to aggregate CPU usage for
  cpu_usage:
    args:
      # 4 queries (one for each aggregation) will be generated for this query
      quantiles:
        - mean
        - 0.5
        - 0.9
        - 1.0
      # Filters allow you to specify what measurement you want to query exactly
      filters:
        _measurement: "kubernetes_pod_container"
        _field: "cpu_usage_nanocores"
    flux_query: |
       from(bucket: "{bucket}")
            |> range(start: {start}, stop: {stop})
            |> {filters}
            |> toFloat()
            |> map(fn: (r) => ({{
                r with
                _value: r._value / 1000000000.0
                }})
            )
            |> {quantile}
```
