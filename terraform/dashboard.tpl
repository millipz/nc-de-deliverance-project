{
    "widgets": [
        {
            "height": 4,
            "width": 6,
            "y": 0,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/Lambda", "Errors", "FunctionName", "${env}-ingestion-function", { "id": "errors", "color": "#d13212", "region": "eu-west-2", "visible": false } ],
                    [ ".", "Invocations", ".", ".", { "id": "invocations", "visible": false, "region": "eu-west-2" } ],
                    [ { "expression": "100 - 100 * errors / MAX([errors, invocations])", "label": "Success rate (%)", "id": "availability", "yAxis": "right", "region": "eu-west-2" } ]
                ],
                "period": 60,
                "region": "eu-west-2",
                "title": "${env} Ingestion Lambda Success Rate",
                "yAxis": {
                    "right": {
                        "max": 100
                    },
                    "left": {
                        "min": 0,
                        "max": 100
                    }
                },
                "view": "gauge",
                "stacked": false,
                "stat": "Sum",
                "setPeriodToTimeRange": true,
                "sparkline": false,
                "trend": false
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 4,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "IF(m2>0,m1/m2)", "label": "execution time per row", "id": "e1", "color": "#e377c2", "region": "eu-west-2" } ],
                    [ "AWS/Lambda", "Duration", "FunctionName", "${env}-ingestion-function", { "label": "Duration average", "stat": "Average", "region": "eu-west-2", "id": "m1", "visible": false } ],
                    [ "ingestion_metrics", "${env}-ingestion_lambda_rows_ingested", { "region": "eu-west-2", "id": "m2", "visible": false } ]
                ],
                "period": 60,
                "region": "eu-west-2",
                "view": "timeSeries",
                "stacked": true,
                "title": "${env} Ingestion Duration per Row",
                "stat": "Maximum"
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 8,
            "x": 0,
            "type": "metric",
            "properties": {
                "period": 60,
                "metrics": [
                    [ "AWS/Lambda", "Duration", "FunctionName", "${env}-ingestion-function", { "label": "Duration minimum", "stat": "Minimum", "region": "eu-west-2" } ],
                    [ "...", { "label": "Duration average", "stat": "Average", "region": "eu-west-2" } ],
                    [ "...", { "label": "Duration maximum", "stat": "Maximum", "region": "eu-west-2" } ]
                ],
                "region": "eu-west-2",
                "view": "timeSeries",
                "stacked": false,
                "title": "${env} Ingestion Run Duration"
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 12,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "ingestion_metrics", "${env}-ingestion_lambda_rows_ingested", { "color": "#2ca02c" } ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "eu-west-2",
                "stat": "Sum",
                "period": 300,
                "title": "${env} Ingested Rows",
                "yAxis": {
                    "left": {
                        "label" : "rows"
                    }
                }
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 0,
            "x": 6,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/Lambda", "Errors", "FunctionName", "${env}-processing-function", { "id": "errors", "color": "#d13212", "region": "eu-west-2", "visible": false } ],
                    [ ".", "Invocations", ".", ".", { "id": "invocations", "visible": false, "region": "eu-west-2" } ],
                    [ { "expression": "100 - 100 * errors / MAX([errors, invocations])", "label": "Success rate (%)", "id": "availability", "yAxis": "right", "region": "eu-west-2" } ]
                ],
                "period": 60,
                "region": "eu-west-2",
                "title": "${env} Processing Lambda Success Rate",
                "yAxis": {
                    "right": {
                        "max": 100
                    },
                    "left": {
                        "min": 0,
                        "max": 100
                    }
                },
                "view": "gauge",
                "stacked": false,
                "stat": "Sum",
                "setPeriodToTimeRange": true,
                "sparkline": false,
                "trend": false
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 4,
            "x": 6,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "IF(m2>0,m1/m2)", "label": "execution time per row", "id": "e1", "color": "#e377c2", "region": "eu-west-2" } ],
                    [ "AWS/Lambda", "Duration", "FunctionName", "${env}-processing-function", { "label": "Duration average", "stat": "Average", "region": "eu-west-2", "id": "m1", "visible": false } ],
                    [ "ingestion_metrics", "${env}-processing_lambda_rows_processed", { "region": "eu-west-2", "id": "m2", "visible": false } ]
                ],
                "period": 60,
                "region": "eu-west-2",
                "view": "timeSeries",
                "stacked": true,
                "title": "${env} Processing Duration per Row",
                "stat": "Maximum"
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 8,
            "x": 6,
            "type": "metric",
            "properties": {
                "period": 60,
                "metrics": [
                    [ "AWS/Lambda", "Duration", "FunctionName", "${env}-processing-function", { "label": "Duration minimum", "stat": "Minimum", "region": "eu-west-2" } ],
                    [ "...", { "label": "Duration average", "stat": "Average", "region": "eu-west-2" } ],
                    [ "...", { "label": "Duration maximum", "stat": "Maximum", "region": "eu-west-2" } ]
                ],
                "region": "eu-west-2",
                "view": "timeSeries",
                "stacked": false,
                "title": "${env} Processing Run Duration"
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 12,
            "x": 6,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "ingestion_metrics", "${env}-processing_lambda_rows_processed", { "color": "#2ca02c" } ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "eu-west-2",
                "stat": "Sum",
                "period": 300,
                "title": "${env} Processed Rows",
                "yAxis": {
                    "left": {
                        "label" : "rows"
                    }
                }
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 0,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/Lambda", "Errors", "FunctionName", "${env}-loading-function", { "id": "errors", "color": "#d13212", "region": "eu-west-2", "visible": false } ],
                    [ ".", "Invocations", ".", ".", { "id": "invocations", "visible": false, "region": "eu-west-2" } ],
                    [ { "expression": "100 - 100 * errors / MAX([errors, invocations])", "label": "Success rate (%)", "id": "availability", "yAxis": "right", "region": "eu-west-2" } ]
                ],
                "period": 60,
                "region": "eu-west-2",
                "title": "${env} Loading Lambda Success Rate",
                "yAxis": {
                    "right": {
                        "max": 100
                    },
                    "left": {
                        "min": 0,
                        "max": 100
                    }
                },
                "view": "gauge",
                "stacked": false,
                "stat": "Sum",
                "setPeriodToTimeRange": true,
                "sparkline": false,
                "trend": false
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 4,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ { "expression": "IF(m2>0,m1/m2)", "label": "execution time per row", "id": "e1", "color": "#e377c2", "region": "eu-west-2" } ],
                    [ "AWS/Lambda", "Duration", "FunctionName", "${env}-loading-function", { "label": "Duration average", "stat": "Average", "region": "eu-west-2", "id": "m1", "visible": false } ],
                    [ "ingestion_metrics", "${env}-loading_lambda_rows_loaded", { "region": "eu-west-2", "id": "m2", "visible": false } ]
                ],
                "period": 60,
                "region": "eu-west-2",
                "view": "timeSeries",
                "stacked": true,
                "title": "${env} Loading Duration per Row",
                "stat": "Maximum"
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 8,
            "x": 12,
            "type": "metric",
            "properties": {
                "period": 60,
                "metrics": [
                    [ "AWS/Lambda", "Duration", "FunctionName", "${env}-loading-function", { "label": "Duration minimum", "stat": "Minimum", "region": "eu-west-2" } ],
                    [ "...", { "label": "Duration average", "stat": "Average", "region": "eu-west-2" } ],
                    [ "...", { "label": "Duration maximum", "stat": "Maximum", "region": "eu-west-2" } ]
                ],
                "region": "eu-west-2",
                "view": "timeSeries",
                "stacked": false,
                "title": "${env} Loading Run Duration"
            }
        },
        {
            "height": 4,
            "width": 6,
            "y": 12,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "ingestion_metrics", "${env}-loading_lambda_rows_loaded", { "color": "#2ca02c" } ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "eu-west-2",
                "stat": "Sum",
                "period": 300,
                "title": "${env} Loaded Rows",
                "yAxis": {
                    "left": {
                        "label" : "rows"
                    }
                }
            }
        }
    ]
}