# A/B testing

It's possible to run the Coiled Runtime benchmarks on A/B comparisons,
highlighting performance differences between different released versions
of dask, distributed, or any of the dependencies and/or between different
dask configs.

To run an A/B test:

### 1. Create a new branch

Branch from main, on the coiled repo itself. Preferably, call the branch
something meaningful, e.g. `AB/jobstealing`.
You *must* create the branch on the Coiled repo (`coiled/coiled-runtime`); CI
workflows will not work on a fork (`yourname/coiled-runtime`).

### 2. Create files in AB_environments/

Open the `AB_environments/` directory and rename/create files as needed.
Each A/B runtime is made of exactly two files:
- `AB_<name>.conda.yaml` (a conda environment file)
- `AB_<name>.dask.yaml` (a dask configuration file)

You may create as many A/B runtime configs as you want in a single `coiled-runtime`
branch.

The conda environment file can contain whatever you want, as long as it can run the
tests; e.g.

```yaml
channels:
  - conda-forge
dependencies:
    - python=3.9
    - coiled-runtime=0.1.0
    - pip:
      - dask==2022.8.1
      - distributed=2022.8.1
```
In this example it's using `coiled-runtime` as a base, but it doesn't have to. If you do
use `coiled-runtime` though, you must install any conflicting packages with pip; in the
example above, `coiled-runtime-0.1.0` pins `dask=2022.6.0` and `distributed=2022.6.0`,
so if you want to install a different version you need to use pip to circumvent the pin.

Instead of published packages, you could also used arbitrary git hashes of
arbitrary forks, e.g.

```yaml
    - pip:
      - dask==2022.8.1
      - git+https://github.com/yourname/distributed@dd81b424971e81616e1a52fa09ce4698a5002d41
```
The second file in each pair is a dask config file. If you don't want to change the
config, you must create an empty file.

e.g.
```yaml
distributed:
  scheduler:
    work-stealing: False
```

### 3. Create baseline files
If you create *any* files in `AB_environments/`, you *must* create the baseline environment:

- `AB_baseline.conda.yaml`
- `AB_baseline.dask.yaml`

#### Complete example
We want to test the impact of disabling work stealing. We create 4 files:

- `AB_environments/AB_baseline.conda.yaml`:
```yaml
channels:
  - conda-forge
dependencies:
    - python=3.9
    - coiled-runtime=0.1.0
    - pip:
      - dask==2022.8.1
      - distributed=2022.8.1
```
- `AB_environments/AB_baseline.dask.yaml`: (empty file)
- `AB_environments/AB_no_steal.conda.yaml`: (same as baseline)
- `AB_environments/AB_no_steal.dask.yaml`:
```yaml
distributed:
  scheduler:
    work-stealing: False
```

### 4. Run CI
- `git push`. Note: we are *not* creating a PR. 
- Open https://github.com/coiled/coiled-runtime/actions/workflows/ab_tests.yml and wait
  for the run to complete.
- Open the run from the link above. In the Summary tab, scroll down and download the
  `static-dashboard` artifact. 
  Note: artifacts will appear only after the run is complete.
- Decompress `static-dashboard.zip` and open `index.html` in your browser.

### 5. Clean up
Remember to delete the branch once you're done.