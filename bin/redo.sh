#!/bin/bash

for s in app app2 lb db; do
    echo "deleting $s..."
    nova delete $s
    sleep 2
done
