# LQCD Chroma

## Purpose

This Lattice quantum-chromodynamics (LQCD) benchmark is based on the Chroma QCD software system and supported by the QUDA library for GPU accelerators. Chroma is a library for simulating the interaction of quarks and gluons in order to calculate the properties of hadrons from first principles.

LQCD simulations generally have two main components: 

- Generating a Markov chain of lattice gauge field configurations through a Hybrid Monte-Carlo (HMC) algorithm
- Performing calculations on the gauge field configurations, such as calculating the spectrum of hadron masses

This package contains representative benchmarks for the HMC component.

## Source

**The JUBE script does _not_ download or build the Chroma source code and its dependencies. The application must be built manually as described below.**

In the `src/` directory, we provide a suite of scripts to both download the needed sources and compile Chroma and its dependencies. These scripts are tested on the JUWELS Booster machine at JSC in its software environment. Users in other environments will potentially need to edit these scripts subject to the constraints of the rules of the procurement procedure.

### Dependencies

Efficient running of Chroma requires linking against the [USQCD software stack](https://www.usqcd.org/software.html). This includes:

- [QMP](http://usqcd-software.github.io/qmp/), handling message-passing (MPI wrappers),
- [QDP-JIT](https://github.com/JeffersonLab/qdp-jit), handling data-parallelism with JIT functionality to permit additional GPU offloading,
- an optimized LQCD linear solver library like [QUDA](http://lattice.github.io/quda/).

Additionally you must be able to link to:

- CUDA
- MPI
- GMP
- Eigen
- libxml2 (scripts provided)
- nvptx-capable LLVM for QDP-JIT (scripts provided)

The build procedure requires CMake and Ninja.

`QUDA` is a specialized library of algorithms to solve large sparse linear systems of the type found in LQCD problems. It is optimized for GPUs. Similarly, the `qdp-jit` framework generates compute kernels which are compiled to efficient GPU machine code by the JIT compiler. `QUDA` and `qdp-jit` are designed to be compatible with both NVIDIA and AMD GPUs. We provide a build algorithm for and have tested only the CUDA/PTX build. For non-NVIDIA architectures we recommend referring to the [`qdp-jit` wiki](https://github.com/JeffersonLab/qdp-jit/wiki) and the relevant section of the [`QUDA` wiki](https://github.com/lattice/quda/wiki/Building-QUDA-With-HIP).

In the `src/` directory, find scripts to download and build (in order) LLVM, QMP, QDP-JIT, QUDA, and Chroma. We strongly recommend **using `get_sources.sh`** to download the source, check out the proper commit ID, and patch the source files.

### Versions

**We require that the benchmarks are performed with the commits specified in the `get_sources.sh` scripts. The exception to this requirement is if you are building a non-CUDA based build.** The required versions are

* LLVM: 14.0.6
* QMP: fac2e9b9
* QDP-JIT: b743cb2f
* QUDA: 32bb266c
* Chroma: 4b2e1171

### Modified Chroma Source for HMC Benchmark

The HMC benchmark standard is defined as the time required for the _post-tuning_ HMC trajectories _without gauge configuration I/O_. As the default, the Chroma `hmc` executable checkpoints the state of the gauge configuration at the end of a run. To suppress this _the Chroma source code must be modified_. Specifically, the `saveState()` call on line 659 of `mainprogs/main/const_hmc.cc` and line 648 of `mainprogs/main/hmc.cc` must be commented out as:

```
//      saveState<UpdateParams>(update_params, mc_control, cur_update, gauge_state.getQ());
```

Patches `const_hmc.patch` and `hmc.patch` are provided and the `get_sources.sh` scripts should automatically modify the source accordingly.

## Building

**NOTE: The Chroma library requires as much as 1 hour to compile.**

In the `src` directory you **must edit the files `env.sh` and `env-MODULES.sh`** to specify compile options and the software environment, respectively. Then execute `./build_all-jit.sh` to launch the individual build steps (`build_*.sh`).

Compilation takes approximately one hour for the benchmark. At the completion of a successful install, the required libraries and executables will be in sub-directories of `$INSTALLDIR/` as defined via `env.sh`.

## Execution

This benchmark comes in two variants

* **TCO Baseline Variant**: A small-scale benchmark used in the TCO evaluation of the procurement, the baseline value is specified at the end of this description; the reference run on JUWELS Booster is on 8 nodes
* **High-Scale Variant**: A large-scale benchmark to probe the scaling behavior between a 50 PFLOP/s sub-partition of JUWELS Booster and a 1000 PFLOP/s sub-partition of the Exascale system. Due to algorithm-internal constraints, the 50 PFLOP/s case is actually run at 512 nodes. For informational purposes, also a configuration for the 1000 PFLOP/s sub-partition is prepared.

The following table gives an overview of the variants of the benchmark, including important parameters. Note that in all cases, `sMass` is set to -0.01 and `cMass` is set to 0.01.

|      **Name**     |   **JUBE Tag**          |  **Volume (nx^3 * nt)**  | **Updates** | **GPU Memory (A100)** |
| ------------------| ----------------------- | ------------------------ | ----------- |  --------------------- |
|    TCO Baseline   |        ---              | 64^3 * 128               |      5      |           100%         |
| |
| High Scale Large  | `highscale_large`       | 256^3 * 256              |      2      |   100%                  |
| High Scale Medium | `highscale_medium`      | 256^3 * 128              |      2      |  80%                   |
| High Scale Small  | `highscale_small`       | 256^3 * 64               |      2      |  72%                   |
| |
| Exa Large         | `exa_large`             | 512^3 * 512              |      2      | 100% expected         |
| Exa Medium        | `exa_medium`            | 512^3 * 256              |      2      | 80% expected          |
| Exa Small         | `exa_small`             | 512^3 * 128              |      2       | 70% expected          |


The TCO Baseline variant and High-Scaling variant are outlined in the following sub-sections. Since the TCO Baseline variant is also the conceptual basis for the High-Scaling variant, we explain this in detail first. We strongly suggest to employ the prepared JUBE scripts for execution of the benchmarks.

### TCO Baseline Variant

In this benchmark, a random _weak field_ gauge configuration is initialized (not read in) and the `hmc` executable performs Hybrid Monte Carlo trajectories of updates of gauge field and pseudofermion variables. At the beginning of the run, `QUDA` performs an auto-tuning cycle to optimize the solver. The auto-tuning data and some JIT functions are saved in a local directory.  
In subsequent runs, if the auto-tuning database is present, the auto-tuning cycle is skipped.  The auto-tuning time is not counted in the benchmark metric.

Measurements on the evolved configuration are stored in XML format in `out.xml`. The HMC algorithm parameters are fixed in the the input file and should not be changed.

The relevant benchmark quantity is the total HMC trajectory time _without_ the first trajectory. The HMC trajectory times can be extracted from the standard output with: `grep "After HMC trajectory call: time"`  
This time is reported in the result table in seconds. At completion of the run, a Python script compares values of the plaquette (product of gauge field link matrices around a closed square path) against reference values in `hmc_ref_5traj_m-0.01m0.01_x64t128.xml` (located in `benchmark/jube/REFERENCE_FILES`).

The executable for the HMC benchmark, `hmc`, is found in the install directory: `CHROMA/bin/hmc`.

#### Manual

Running Chroma requires careful attention to the runtime environment and parameters. We suggest examining the working Slurm batch script provided for reference in:

```
benchmark/jube/BATCH_TEMPLATES/submit.job
```

Usually, the required input file (`-i`) is automatically generated by JUBE from a template and can be found in the benchmark directories, e.g.:

```
bench_run_hmc/000010/000000_submit/work/input_hmc_TEMPLATE_LW_QUDA-rsd.xml
```

For non-JUBE users, a copy of the complete input file needed for the standard TCO baseline benchmark can be found in 

```
lqcd-chroma/benchmark/jube/INPUT_TEMPLATES/EXAMPLE_INPUT/input_hmc_x64t128_5traj_LW_QUDA-rsd-default.xml
```

##### Command Line

The launcher line for the `hmc` benchmark might look like:

```
srun --cpu-bind=none ${INSTALL_DIR}/hmc -gpudirect -ptxdb ./QRP//qdp_ptxdb -i input_hmc_x64t128_5traj_LW_QUDA-rsd-default.xml -o hmc_5traj_m-0.2m0.2_x64t128.xml -l log.xml -geom 1 1 4 8 -iogeom 1 1 1 1

```

#### JUBE

The HMC benchmark requires:

- the JUBE script `lqcd_hmc_benchmark.xml` 
- the input template `INPUT_TEMPLATES/input_hmc_TEMPLATE_LW_QUDA-rsd.xml` 
- reference file `REFERENCE_FILES/hmc_ref_5traj_m-0.01m0.01_x64t128.xml` for the validation test

To run, use

```
jube run lqcd_hmc_benchmark.xml
```

and after completion of the job, type:

```
jube continue -r bench_run_hmc
```

### High-Scaling Variant

For illustrative purposes, the JUBE version of this variant is explained first.

#### JUBE

The High-Scaling variant of the benchmark can be executed from the same JUBE script as the TCO Baseline variant by specifying a `highscale_MEM` tag:

```
jube run lqcd_hmc_benchmark.xml --tag highscale_large
```

The three high-scaling versions, **highscale_large**, **highscale_medium**, and **highscale_small** each run a benchmark on 512 nodes of JUWELS Booster at JSC, with varying GPU memory usage, as shown in the table above. The GPU memory usage is somewhat difficult to predict _a priori_, as the QUDA auto-tuner may produce different results on different hardware. 

#### Manual

To run without JUBE, one needs the appropriate input file and reference file from `lqcd-chroma/benchmark/jube/INPUT_TEMPLATES/EXAMPLE_INPUT/` and `lqcd-chroma/benchmark/jube/REFERENCE_FILES/` respectively.

| **Variant** |                        **Input File**                       |            **Reference File**            |
|-------------|-------------------------------------------------------------|------------------------------------------|
| large       | `input_hmc_x256t64_2traj_LW_QUDA-rsd-highscale_small.xml`   | `hmc_ref_2traj_m-0.01m0.01_x256t256.xml` |
| medium      | `input_hmc_x256t128_2traj_LW_QUDA-rsd-highscale_medium.xml` | `hmc_ref_2traj_m-0.01m0.01_x256t128.xml` |
| small       | `input_hmc_x256t64_2traj_LW_QUDA-rsd-highscale_small.xml`   | `hmc_ref_2traj_m-0.01m0.01_x256t64.xml`  |

To verify correctness, run the verification script as with the default benchmark, _but with the tolerance `1e-08`_:
```
python compare_plaqs.py  ${xml_output_file}  ${reference_file} 1e-8
```

### Exascale Configuration

In addition to the High-Scaling variant for a 50 PFLOP/s sub-partition of JUWELS Booster, we provide also a JUBE configuration for a 1000 PFLOP/s sub-partition of the Exascale system; the _Exascale Configuration_. Also this configuration is embedded into the JUBE script `lqcd_hmc_benchmark.xml` and is activated by the according tags, for example:

```
jube run lqcd_hmc_benchmark.xml --tag exa_large
```

See table able above for implemented configurations.

The tag can be useful, even on a smaller system, as it will generate an appropriate input file and sample batch file in the JUBE benchmark directory. The batch file can then be edited by hand to explore optimizations applicable to your system. _The XML input file should not be modified._

## Modification of Run-Time Parameters

For the TCO Baseline Variant, the number of nodes (and with it, the number of GPUs), is a free parameter and may be adapted.  
For the High-Scaling Variant, the number of GPUs is a fixed parameter to accommodate the 1000 PFLOP/s condition as well as algorithm-internal constraints; a number of 4096 nodes (containing in total 16384 GPUs) are to be used for execution on the Exascale system. In case of other numbers of GPUs per node, the amount of nodes which contain 16384 GPUs is to be selected. The High-Scaling Variant basis execution on JUWELS Booster (50 PFLOP/s) was conducted on 512 nodes (2048 GPUs). The number of MPI tasks should be equal to the number of GPUs in both Variants.

The problem parameters, as specified in the input files, are fixed and _may not be modified_. Nor may the tolerance values for the validation tests be modified. That is, the workload of the problem may not be altered.

Run time variables may be modified, including OpenMP threads. Controlling how the workload is divided among the compute resources may be modified in the JUBE script or, if running without JUBE, in the batch script directly. 

It is important that the 4-dimensional LQCD problem can be divided evenly among the available MPI tasks. The problem has a 4-dimensional volume `Nx*Nx*Nx*Nt`; in the three spatial dimensions, `x`,`y`, and `z`, the problem has the same size but in the time direction `t`, the extent may be different. In loops over the 4-dimensional volume (or sub-volumes, after slicing) `x` is the fastest dimension, followed by `y`, `z`, and `t`. It is therefore sometimes advantageous to have the slices across the t-dimension be disproportionately thinner. 

The performance and runtime of Chroma is dependent on runtime parameters controlling the amount of resources and the problem layout. 
In the batch files, the parameters `xtasks`, `ytasks`, `ztasks`, and `ttasks` are passed to the executable via the flag `-geom $xtasks $ytasks $ztasks $ttasks`, and control the number of slices in each respective dimension. 

When adjusting the total number of MPI tasks applied to the problem, you must then adjust `xtasks`, `ytasks`, `ztasks`, and `ttasks`, satisfying the constraints:

-  The product of all slices must be equal to the total number of MPI tasks: `xtasks * ytasks * ztasks * ttasks = ntasks`
-  Each of the four dimensions must be evenly divisible by the number of tasks corresponding to that dimension; i.e., `Nx%xtasks =0 `, `Nx%ytasks=0`, `Nx%nztasks=0` and `Nt%nttasks=0`
-  The extent of the local sub-volume assigned to each MPI task must be _even_ in each dimension.

To re-iterate, a problem of size `Nx^3*Nt`, run with `-geom $xtasks $ytasks $ztasks $ttasks` will have a local volume of:

```
 (Nx/xtasks) * (Nx/ytasks) * (Nx/nztasks) * (Nt/nttasks)
```

assigned to each MPI task.

We _strongly suggest_ trying different slicings of the problem to determine what is optimal for your system.

The user may in some cases find improved performance by controlling the logical topology from the above default ordering with the arguments `-qmp-logic-map` and `-qmp-alloc-map`. See the [wiki](https://github.com/lattice/quda/wiki/Chroma-with-QUDA) for an example.

We find that on multi-GPU/multi-NIC nodes, peak performance depends on carefully optimizing the CPU/GPU/NIC affinity. It is up to the user to tune this on their system. We provide for example (but do not use in this benchmark) an example of a script used to optimize this affinity on JUWELS Booster:

```
lqcd-chroma/benchmark/jube/BATCH_TEMPLATES/runbooster.sh
```

On systems with InfiniBand networks and CUDA 11 (or later) QUDA can use NVSHMEM for communication to reduce communication overheads and improve scaling. Please refer to the [QUDA wiki](https://github.com/lattice/quda/wiki/Multi-GPU-with-NVSHMEM).


## Results

The LQCD Chroma benchmark performs a number of HMC updates of a lattice gauge field with different dimensions. The number of updates is 5 for the TCO Baseline configuration, using a gauge field of volume 64^3x128. See table above for more details and the parameters for the High-Scaling Variant. Additionally, the JUBE script populates the XML input file with physical parameters (such as quark masses) and algorithmic parameters (such as solver precision and residuals). These should not be altered.

The relevant metric for this benchmark is the **trajectory time** -- the time spent in HMC update trajectories -- minus the time of the first update, as it includes tuning. This is reported as _**traj. time**_ in the results table (12th column), like in the following (abbreviated):

| ID |  Nt | Nx | Nodes | Tsk | Cut dims | Tk_t | Tk_z | Tk_y | Tk_x | Iters | traj. time (s) | runtime (s) | Max rel. diff |
|----|-----|----|-------|-----|----------|------|------|------|------|-------|----------------|-------------|---------------|
|  0 | 128 | 64 |     8 |  32 |        2 |    8 |    4 |    1 |    1 |  1066 |          432.5 |       712.3 |       1.8e-15 |


Note that the timing comes from the standard output of the Chroma `hmc` execution and _not_ from  from a shell command like `time`. To verify the HMC update trajectory timing one can:

```
> grep "After HMC trajectory call: time" out.txt

```

to get output like:

```
After HMC trajectory call: time= 249.031811 secs
After HMC trajectory call: time= 104.715705 secs
After HMC trajectory call: time= 107.18859 secs
After HMC trajectory call: time= 109.343631 secs
After HMC trajectory call: time= 111.253191 secs
```

The metric time in this case is obtained by summing the second through fifth update times, i.e. `104.715705 + 107.18859 + 109.343631 + 111.253191 = 432.501117`.

Here, `out.txt` contains the standard output of a successful execution of the Chroma `hmc` executable.

## Verification

The last two columns in the table above indicate whether the benchmark has passed the validation tests. There are two validation tests. The first, more stringent test compares the output file to a reference output file produced at JSC on JUWELS Booster. The second checks parameters in the output file to ensure they have not been altered for artificial runtime reduction.

JUBE performs this verification automatically.

To verify results without JUBE, one needs to employ two provided Python scripts `compare_plaqs.py` and `verify_weakscale.py` by hand. The scripts are to be found in `benchmark/jube/BATCH_TEMPLATES/`an require a reference output file, `hmc_ref_5traj_m-0.01m0.01_x64t128.xml` located in `benchmark/jube/REFERENCE_FILES/hmc_ref_5traj_m-0.01m0.01_x64t128.xml`.

### Plaquette

The execution of the plaquette verification script is as follows:

```
xmloutput_file=${PATH_TO_YOUR_OUTPUT}/hmc_5traj_m-0.01m0.01_x64t128.xml
hmc_reference_file=lqcd-chroma/benchmark/jube/BATCH_TEMPLATES/hmc_ref_5traj_m-0.01m0.01_x64t128.xml
valid_tolerance=1e-10
python compare_plaqs.py ${hmc_reference_file} ${xmloutput_file} ${valid_tolerance}  >> $textoutput_file
```

With `hmc_5traj_m-0.01m0.01_x64t128.xml` being the output XML file produced by your run. The tolerance requirement is `1e-10` for the default benchmark and `1e-08` for the high-scale benchmarks. _This must not be changed._

| Variant      | Tolerance |
| ------------ | --------- |
| TCO Baseline | 1e-10     |
| High-Scaling | 1e-08     |

A successful run produces the output:
```
CHECKVALID: PASS
```

### Parameter

The parameter verification script is run as:

```
python verify_weakscale.py ${xmloutput_file} $smass $cmass 1e-10 $updates  $nx $nt  
```

with the parameters `smass`, `cmass`, `updates`, `nx` and `nt` given in the table above in the high-scaling variants section of this Description. A successful run produces the output:

```
INPUT VALIDATION: PASS
```

## Commitment

### TCO Baseline

The baseline configuration of the benchmark should be chosen such that the trajectory time is less than 432.5 seconds. This was achieved on JUWELS Booster with 8 nodes (4 NVIDIA A100 GPUs each) and `ttasks=8`, `ztasks=4`, `ytasks=1` and `xtasks=1`. 

| Nodes | Tasks per Node | Threads per Task | GPUs per Task | Trajectory Time/s |
|-------|----------------|------------------|---------------|-------------------|
|     8 |              4 |               24 |             1 |             432.5 |

### High-Scaling

| Nodes | Tasks per Node | Threads per Task | GPUs per Task | Memory Variant | Trajectory Time/s |
|-------|----------------|------------------|---------------|----------------|-------------------|
|   512 |              4 |               24 |             1 | large          |            1534.6 |
|   512 |              4 |               24 |             1 | medium         |             246.8 |
|   512 |              4 |               24 |             1 | small          |             149.1 |

