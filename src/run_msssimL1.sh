#!/usr/bin/env sh
set -e

~/Desktop/caffe-no-cudnn/build/tools/caffe train --solver=./solver_msssimL1.prototxt $@
