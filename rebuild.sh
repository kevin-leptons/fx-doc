#!/usr/bin/env bash

set -e

rm -rf dest
fx-doc build doc dest
fx-doc serve dest