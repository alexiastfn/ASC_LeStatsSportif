# Compiler collection setup
NVCC      ?= nvcc
NVCCFLAGS ?=
CPPFLAGS  ?=
LDFLAGS   ?=
LIBS      ?=
EXECS     ?=

# Cluster setup
PARTITION  ?= xl
RUN_TIME   ?= 00:05:00
BUILD_TIME ?= 00:05:00
IMG        ?= docker://gitlab.cs.pub.ro:5050/asc/asc-public/cuda-labs:1.11.4
LOAD_CMD   ?= module load libraries/cuda-11.4;
BUILD_CMD  ?= make LOCAL=y
RUN_CMD    ?= ./$${exec}

# Alternatives
# PARTITION  ?= ucsx
# IMG        ?= docker://gitlab.cs.pub.ro:5050/asc/asc-public/cuda-labs:1.9.1
# LOAD_CMD   ?= apptainer exec --nv $(IMG)

# Logged into your fep8.grid.pub.ro user, employ the following two
ifndef LOCAL

compile:
	@sbatch                      \
		--partition $(PARTITION) \
		--gres gpu:1             \
		--time $(BUILD_TIME)     \
		--wrap="$(LOAD_CMD) $(BUILD_CMD)"

run:
	@for exec in $(EXECS);                                  \
	do                                                      \
		test -f $${exec} &&                                 \
		sbatch                                              \
			--partition $(PARTITION)                        \
			--gres gpu:1                                    \
			--time $(RUN_TIME)                              \
			--wrap="$(LOAD_CMD) $(RUN_CMD)";               \
	done

# To run on your local machine define LOCAL=y
else

# Default rule
build: $(EXECS)

# Build each executable
$(EXECS): %: %.cu
	$(NVCC) $(NVCCFLAGS) $(CPPFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

endif

clean:
	rm -f $(EXECS) slurm-*.out slurm-*.err
