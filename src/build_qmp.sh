#!/bin/bash
source env.sh

cmake -S ${SRCDIR}/qmp -B ${BUILDDIR}/build_qmp \
-DCMAKE_INSTALL_PREFIX=${QMP_INSTALLDIR} \
-DQMP_MPI=ON \
-DBUILD_SHARED_LIBS=ON \
-DQMP_TESTING=OFF

cmake --build ${BUILDDIR}/build_qmp  ${CMAKE_MAKE_OPTS}
cmake --install ${BUILDDIR}/build_qmp 
