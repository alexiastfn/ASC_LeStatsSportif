# Compiler collection setup
NVCC     ?= nvcc
CC_FLAGS ?=
CPPFLAGS ?=
LDFLAGS  ?=
LIBS     ?=
EXECS    ?=

# Cluster setup
PARTITION  ?= ucsx
RUN_TIME   ?= 00:01:00
BUILD_TIME ?= 00:01:00
IMG        ?= docker://gitlab.cs.pub.ro:5050/asc/asc-public/cuda-labs:1.9.1
# IMG        ?= docker://gitlab.cs.pub.ro:5050/asc/asc-public/cuda-labs:1.11.4

# Logged into your fep8.grid.pub.ro user, employ the following two
ifndef LOCAL

compile:
	sbatch                       \
		--partition $(PARTITION) \
		--gres gpu:1             \
		--time $(BUILD_TIME)     \
		--wrap="apptainer exec --nv $(IMG) make LOCAL=y"

run:
	@for exec in $(EXECS);                                \
	do                                                    \
		test -f $${exec} &&                               \
		sbatch                                            \
			--partition $(PARTITION)                     \
			--gres gpu:1                                  \
			--time $(RUN_TIME)                           \
			--wrap="apptainer exec --nv $(IMG) ./$${exec}"; \
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
	rm -f $(EXECS)
