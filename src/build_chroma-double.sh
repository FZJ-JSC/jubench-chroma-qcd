#!/bin/bash
source env.sh

cmake -S ${SRCDIR}/chroma -B ${BUILDDIR}/build_chroma \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_INSTALL_PREFIX=${CHROMA_INSTALLDIR}/ \
      -DCMAKE_PREFIX_PATH=${PREFIX_PATH}/ \
      -DBUILD_SHARED_LIBS=ON \
      -DLLVM_DIR=${LLVM_INSTALLDIR}/lib/cmake/llvm \
      -DQMP_DIR=${QMP_INSTALLDIR}/lib/cmake/QMP/ \
      -DQDPXX_DIR=${QDPJIT_INSTALLDIR}/lib/cmake/QDPXX \
      -DQUDA_DIR=${QUDA_INSTALLDIR}/lib/cmake/QUDA \
      -DChroma_ENABLE_JIT_CLOVER=ON \
      -DChroma_ENABLE_QUDA=ON \
      -DChroma_ENABLE_OPENMP=ON \
      -DCMAKE_CXX_FLAGS=${ARCHFLAGS}

cmake --build ${BUILDDIR}/build_chroma ${CMAKE_MAKE_OPTS}
cmake --install ${BUILDDIR}/build_chroma




if test -f "${CHROMA_INSTALLDIR}/bin/chroma"; then
    echo 
    echo "Build SUCCESSFUL"
    echo
    echo "INSTALL_DIR=$INSTALLDIR"

else
    echo "build UNSUCCESSFUL"
fi


