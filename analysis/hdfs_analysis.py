import subprocess
import pandas as pd
from io import StringIO


HDFS_PATH = "/hair-loss/data/Luke_hair_loss_documentation.csv"

HADOOP_HOME = "/home/hadoop/software/hadoop-3.1.3"

HDFS_BIN = HADOOP_HOME + "/bin/hdfs"


def read_from_hdfs():

    print("=" * 60)
    print("HDFS 数据读取测试")
    print("=" * 60)

    print("\n数据来源：")
    print("HDFS:", HDFS_PATH)

    result = subprocess.run(
        [
            HDFS_BIN,
            "dfs",
            "-cat",
            HDFS_PATH
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:

        print("\nHDFS 数据读取失败！")

        print(result.stderr)

        return None

    data = result.stdout

    df = pd.read_csv(
        StringIO(data)
    )

    print("\nHDFS 数据读取成功！")

    print(
        f"数据规模：{df.shape[0]} 行 × {df.shape[1]} 列"
    )

    print("\n数据字段：")

    print(
        list(df.columns)
    )

    print("\n前5条数据：")

    print(
        df.head()
    )

    return df


if __name__ == "__main__":

    df = read_from_hdfs()

    if df is not None:

        print("\n" + "=" * 60)
        print("HDFS 数据读取测试完成")
        print("=" * 60)