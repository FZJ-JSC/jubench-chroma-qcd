# Download and build instructions

This is the install instructions for building Chroma with the QUDA library. This version uses the "jit" QDP-JIT library which does additional offloads to the GPU.


**Note: Source download and build time can be approximately 1 hour.** 

It may be useful to build on a compute node or reduce the number of CMake processes, `export CMAKE_MAKE_OPTS="-- -j$(nproc)` in `env.sh`.

# Prepare the environment:

The supplied file env-JIT-JWBOOST-GCC11.2-CUDA11.5-PS.sh contains a list of software modules one would load on the JSC juwels-booster system before compiling, as well as a variable indicating the model of Nvidia GPU to be supported. These must be modified to suit the target system.


## Required dependencies
The build requires:
- QUDA
- MPI
- GMP
- Eigen
- libxml2 (scripts provided)
- nvptx-capable LLVM for QDP-JIT (scripts provided)
- CMake
- Ninja
- Python



# Download the source:

Executing:
```
./get_sources.sh
```

will download the source code for:
- `llvm`
- `qmp`
- `qdp-jit`
- `quda`
- `chroma`

For fairness, we insist on checking out the commits specified in the download script.
If your system does not have a `libxml2` installation, you must download and install it as well.

The `get_sources.sh` script also patches the Chroma source code so no gauge configuration file is written at the end of the HMC updates.



# Build CHROMA
With the source downloaded, one can execute
```
./build_all_jit.sh
```
which will build
- `llvm`
- `qmp`
- `qdpxx`
- `quda`
- `chroma`

If the build is successful, the Chroma and HMC executables will exist on completion in the Chroma install directory:
- `INSTALL/CHROMA/bin/chroma` 
- `INSTALL/CHROMA/bin/hmc` 

Without alteration of the directory structure of this benchmark, the install directories and the `lib/` directories of CHROMA and its dependencies will be correctly represented in the JUBE scripts:
- `benchmark/jube/lqcd_hmc_benchmark.xml`
- `benchmark/jube/lqcd_hmc_benchmark.xml`

**If you install CHROMA anywhere else, you will need to alter the JUBE benchmarking scripts.**

As this recipe builds dynamical libraries, you must have the `lib/` directories of QMP, QDPXX, QUDA, and CHROMA in your `LD_LIBRARY_PATH` at runtime.


# Further reading
More information about building QUDA and CHROMA can be found here:
[https://github.com/lattice/quda/wiki/Chroma-with-QUDA](https://github.com/lattice/quda/wiki/Chroma-with-QUDA)
[https://github.com/lattice/quda/wiki](https://github.com/lattice/quda/wiki)

The above recipe builds a CUDA-based version of QUDA. For hints about building a HIP-ified version of QUDA, see:
[https://github.com/lattice/quda/wiki/Building-QUDA-With-HIP](https://github.com/lattice/quda/wiki/Building-QUDA-With-HIP)

