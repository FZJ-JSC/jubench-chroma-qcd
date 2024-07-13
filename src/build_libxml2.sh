#!/bin/bash
source ./env.sh

cmake -S ${SRCDIR}/libxml2 -B ${BUILDDIR}/build_libxml2 \
-DCMAKE_BUILD_TYPE=RELEASE \
-DLIBXML2_WITH_PYTHON=OFF \
-DLIBXML2_WITH_LZMA=OFF \
-DCMAKE_INSTALL_PREFIX=${INSTALLDIR} 

cmake --build ${BUILDDIR}/build_libxml2 ${CMAKE_MAKE_OPTS}
cmake --install ${BUILDDIR}/build_libxml2
