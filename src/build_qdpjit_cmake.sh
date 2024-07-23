#!/bin/bash
source ./env.sh

cmake -S ${SRCDIR}/qdp-jit -B ${BUILDDIR}/build_qdp-jit \
      -DCMAKE_INSTALL_PREFIX=${QDPJIT_INSTALLDIR} \
      -DCMAKE_PREFIX_PATH=${PREFIX_PATH} \
      -DBUILD_SHARED_LIBS=ON \
      -DQDP_ENABLE_BACKEND=CUDA \
      -DQDP_ENABLE_COMM_SPLIT_DEVICEINIT=OFF \
      -DQDP_ENABLE_LLVM16=ON \
      -DQDP_PROP_OPT=OFF \
      -DLLVM_DIR=${LLVM_INSTALLDIR}/lib/cmake/llvm \
      -DQMP_DIR=${QMP_INSTALLDIR}/lib/cmake/QMP \
      -DCMAKE_CXX_FLAGS=${ARCHFLAGS}

cmake --build ${BUILDDIR}/build_qdp-jit ${CMAKE_MAKE_OPTS}
cmake --install ${BUILDDIR}/build_qdp-jit
