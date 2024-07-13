
. ./env.sh


mkdir ${SRCDIR}

cd ${SRCDIR}

echo ${SRCDIR}



cd ${SRCDIR}

echo ${SRCDIR}




#get llvm if you do not already have nvptx-enabled llvm
git clone --depth=1 --branch  llvmorg-14.0.6 https://github.com/llvm/llvm-project.git

#get llvm if you do not already have it
#git clone --branch v2.9.14 https://github.com/GNOME/libxml2.git

#QMP is ususlly a a wrapper for MPI
git clone --branch qmp2-5-4 https://github.com/usqcd-software/qmp.git
#checkout specific commit
cd qmp/
git checkout fac2e9b9db2448994d338786b211ec67ff9553b2
cd ${SRCDIR}


#QDP-JIT
git clone --recursive --branch devel https://github.com/JeffersonLab/qdp-jit.git 
cd qdp-jit/

git checkout b743cb2f7c6823189d560640463dde1c6e80fcd6

cd ${SRCDIR}

#QUDA
git clone --branch develop https://github.com/lattice/quda.git # c04150e
cd quda
git checkout 32bb266ca3aa49618f84e0d1866b1057104b6ca6

cd ${SRCDIR}



#CHROMA
git clone --branch devel --recursive https://github.com/JeffersonLab/chroma.git 
cd chroma

git checkout 4b2e1171ac307b7f4273186543afad5b25b7bc00



#Patch chroma to supress saving gauge configuration on hmc exit (want timing without big I/O)
#Equivalent to commenting out "saveState" call on line 659 of mainprogs/main/const_hmc.cc and line 648 of mainprogs/main/hmc.cc
cp  ${TOPDIR}/const_hmc.patch ./
cp  ${TOPDIR}/hmc.patch ./

patch mainprogs/main/const_hmc.cc < const_hmc.patch 
patch mainprogs/main/hmc.cc < hmc.patch 


cd ${BASEDIR}
