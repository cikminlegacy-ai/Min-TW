#!/bin/bash
# Re-apply after every `python3 build_index.py` (it rewrites index.html).
export HYPERFRAMES_TELEMETRY=0
npx hyperframes media-treatment --project . --file index.html --selector '#talk-past' --grading '{"adjust":{"exposure":-0.12,"contrast":0.2,"highlights":-0.25,"shadows":-0.05,"blacks":-0.1,"temperature":-0.25,"tint":-0.03,"saturation":-0.2},"details":{"vignette":0.5,"grain":0.25}}' --apply --json | grep -m1 '"ok"'
npx hyperframes media-treatment --project . --file index.html --selector '#talk-now' --grading '{"adjust":{"exposure":0.12,"contrast":0.12,"highlights":-0.1,"shadows":0.08,"temperature":0.18,"vibrance":0.2,"saturation":0.05},"details":{"vignette":0.15}}' --apply --json | grep -m1 '"ok"'
