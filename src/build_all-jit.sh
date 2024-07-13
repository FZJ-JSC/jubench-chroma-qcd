#!/usr/bin/env bash

./build_llvm.sh
./build_qmp.sh

./build_qdpjit_cmake.sh
./build_quda_qdp_double-cmake.sh
./build_chroma-double.sh

####./build_libxml2.sh
