from cgitb import small
import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.sizeof import sizeof
from dask.utils import format_bytes
from dask.datasets import timeseries

from ..utils_test import cluster_memory, timeseries_of_size, wait


def print_dataframe_info(df):
    p = df.partitions[0].compute(scheduler="threads")
    partition_size = sizeof(p)
    total_size = partition_size * df.npartitions
    print(
        f"~{len(p) * df.npartitions:,} rows x {len(df.columns)} columns, "
        f"{format_bytes(total_size)} total, "
        f"{df.npartitions:,} {format_bytes(partition_size)} partitions"
    )


def test_dataframe_align(small_client):
    memory = cluster_memory(small_client)  # 76.66 GiB

    df = timeseries_of_size(
        memory // 2,
        start="2020-01-01",
        freq="600ms",
        partition_freq="12h",
        dtypes={i: float for i in range(100)},
    )
    print_dataframe_info(df)
    # ~50,904,000 rows x 100 columns, 38.31 GiB total, 707 55.48 MiB partitions

    df2 = timeseries_of_size(
        memory // 4,
        start="2010-01-01",
        freq="600ms",
        partition_freq="12h",
        dtypes={i: float for i in range(100)},
    )
    print_dataframe_info(df2)
    # ~25,488,000 rows x 100 columns, 19.18 GiB total, 354 55.48 MiB partitions

    final = (df2 - df).mean()  # will be all NaN, just forcing alignment
    wait(final, small_client, 10 * 60)


def test_shuffle(small_client):
    memory = cluster_memory(small_client)  # 76.66 GiB

    df = timeseries_of_size(
        memory // 4,
        start="2020-01-01",
        freq="1200ms",
        partition_freq="24h",
        dtypes={i: float for i in range(100)},
    )
    print_dataframe_info(df)
    # ~25,488,000 rows x 100 columns, 19.18 GiB total, 354 55.48 MiB partitions

    shuf = df.shuffle(0, shuffle="tasks")
    result = shuf.size
    wait(result, small_client, 20 * 60)


def test_ddf_isin(small_client):
    """
    Checks the efficiency of serializing a large list for filtering
    a dask dataframe, and filtering the dataframe by column
    based on that list
    """
    n = 10_000_000
    rs = np.random.RandomState(42)
    ddf = timeseries(end="2000-05-01",dtypes={"A": float, "B": int}, seed=42)
    ddf.A = ddf.A.mul(1e7)
    ddf.A = ddf.A.astype(int).persist()
    a_column_unique_values = np.arange(1, n // 10)
    filter_values_list = sorted(
        rs.choice(a_column_unique_values, len(a_column_unique_values) // 2).tolist()
    )
    tmp_ddf = ddf.loc[ddf["A"].isin(filter_values_list)]
    wait(tmp_ddf, small_client, 20 * 60)
