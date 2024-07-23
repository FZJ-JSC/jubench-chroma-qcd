#!/bin/bash
source ./env.sh

cmake -S ${SRCDIR}/llvm-project/llvm-${llvm_vers}.src -B ${BUILDDIR}/build_llvm \
-DLLVM_ENABLE_TERMINFO="OFF" \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_INSTALL_PREFIX=${LLVM_INSTALLDIR} \
-DLLVM_TARGETS_TO_BUILD="${QDPJIT_HOST_ARCH}" \
-DLLVM_ENABLE_ZLIB="OFF" \
-DBUILD_SHARED_LIBS="OFF" \
-DLLVM_ENABLE_RTTI="ON"  \
${SRCDIR}/llvm-project/llvm

cmake --build  ${BUILDDIR}/build_llvm ${CMAKE_MAKE_OPTS}
cmake --install  ${BUILDDIR}/build_llvm   
