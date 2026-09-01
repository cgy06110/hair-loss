import pandas as pd
import numpy as np
import os
import subprocess
from io import StringIO


# ============================================================
# 基础路径
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESULT_DIR = os.path.join(
    BASE_DIR,
    "results"
)

os.makedirs(RESULT_DIR, exist_ok=True)


# ============================================================
# HDFS 配置
# ============================================================

HDFS_BIN = "/home/hadoop/software/hadoop-3.1.3/bin/hdfs"

HDFS_PATH = "/hair-loss/data/Luke_hair_loss_documentation.csv"


# ============================================================
# 从 HDFS 读取数据
# ============================================================

def read_from_hdfs():

    print("\n正在连接 HDFS...")
    print("HDFS 地址：hdfs://localhost:9000")
    print("数据路径：" + HDFS_PATH)

    try:

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

    except Exception as e:

        print("\nHDFS 命令执行失败：")
        print(e)

        return None


    if result.returncode != 0:

        print("\nHDFS 数据读取失败：")
        print(result.stderr)

        return None


    try:

        df = pd.read_csv(
            StringIO(result.stdout)
        )

        return df

    except Exception as e:

        print("\nCSV 数据解析失败：")
        print(e)

        return None


# ============================================================
# 数据读取
# ============================================================

print("=" * 60)
print("脱发影响因素分析系统")
print("=" * 60)


print("\n[1/8] 正在从 HDFS 读取数据...")


df = read_from_hdfs()


if df is None:

    print("\nHDFS 数据读取失败，程序终止。")

    exit()


print("\nHDFS 数据读取成功！")

print(
    f"数据规模：{df.shape[0]} 行 × {df.shape[1]} 列"
)

print("\n原始字段：")

print(
    df.columns.tolist()
)


# ============================================================
# 字段清理
# ============================================================

print("\n[2/8] 正在进行字段清理...")


df.columns = (
    df.columns
    .str.strip()
)


print("字段清理完成。")


# ============================================================
# 数据质量检查
# ============================================================

print("\n[3/8] 正在检查数据质量...")


print("\n缺失值：")

print(
    df.isnull().sum()
)


duplicate_count = df.duplicated().sum()


print(
    f"\n重复数据：{duplicate_count} 条"
)


df = df.drop_duplicates()


print(
    f"去重后数据量：{len(df)} 条"
)


# ============================================================
# 数据清洗
# ============================================================

print("\n[4/8] 正在清洗数据...")


# ------------------------------------------------------------
# 数值字段
# ------------------------------------------------------------

numeric_columns = [
    "pressure_level",
    "stress_level",
    "swimming",
    "hair_washing",
    "hair_grease"
]


for column in numeric_columns:

    if column not in df.columns:
        continue

    # 如果字段是数值型
    if pd.api.types.is_numeric_dtype(df[column]):

        missing_count = df[column].isnull().sum()

        if missing_count > 0:

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )

            print(
                f"{column}：使用中位数 {median_value} 填充缺失值"
            )


# ============================================================
# 检查缺失比例
# ============================================================

print("\n[5/8] 检查缺失严重字段...")


missing_ratio = (
    df.isnull().mean() * 100
)


high_missing_columns = (
    missing_ratio[
        missing_ratio > 50
    ]
)


if len(high_missing_columns) > 0:

    print(
        "以下字段缺失比例超过 50%，暂不参与主要分析："
    )

    for column, ratio in high_missing_columns.items():

        print(
            f"  {column}: {ratio:.2f}%"
        )

else:

    print(
        "没有字段的缺失比例超过 50%。"
    )


# ============================================================
# 保存清洗后的数据
# ============================================================

print("\n[6/8] 保存清洗后的数据...")


cleaned_path = os.path.join(
    RESULT_DIR,
    "cleaned_data.csv"
)


df.to_csv(
    cleaned_path,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"清洗数据已保存：{cleaned_path}"
)


# ============================================================
# 开始数据分析
# ============================================================

print("\n[7/8] 正在进行数据分析...")


# ============================================================
# 1. 总体概况
# ============================================================

overview = pd.DataFrame({

    "指标": [
        "总人数",
        "平均熬夜次数",
        "平均咖啡摄入量",
        "平均脑力工作时间",
        "平均头发油脂程度",
        "平均libido"
    ],

    "数值": [

        len(df),

        df["stay_up_late"].mean()
        if "stay_up_late" in df.columns
        else np.nan,

        df["coffee_consumed"].mean()
        if "coffee_consumed" in df.columns
        else np.nan,

        df["brain_working_duration"].mean()
        if "brain_working_duration" in df.columns
        else np.nan,

        df["hair_grease"].mean()
        if "hair_grease" in df.columns
        else np.nan,

        df["libido"].mean()
        if "libido" in df.columns
        else np.nan
    ]
})


overview.to_csv(
    os.path.join(
        RESULT_DIR,
        "overview.csv"
    ),
    index=False,
    encoding="utf-8-sig"
)


print("已完成：overview")


# ============================================================
# 2. 脱发程度分布
# ============================================================

if "hair_loss" in df.columns:

    hair_loss_distribution = (
        df["hair_loss"]
        .value_counts()
        .reset_index()
    )

    hair_loss_distribution.columns = [
        "hair_loss",
        "总人数"
    ]

    hair_loss_distribution.to_csv(
        os.path.join(
            RESULT_DIR,
            "hair_loss_distribution.csv"
        ),
        index=False,
        encoding="utf-8-sig"
    )

    print("已完成：hair_loss")


# ============================================================
# 通用因素分析函数
# ============================================================

def analyze_factor(
    df,
    factor,
    filename
):

    if factor not in df.columns:
        return None


    temp = df[
        [factor, "hair_loss"]
    ].copy()


    temp = temp.dropna()


    if len(temp) == 0:
        return None


    # 各组人数
    group_count = (
        pd.crosstab(
            temp[factor],
            temp["hair_loss"]
        )
        .reset_index()
    )


    # 中高程度脱发
    high_loss_levels = [
        "Many",
        "A lot"
    ]


    result = (
        temp.groupby(factor)["hair_loss"]
        .apply(
            lambda x:
            x.isin(
                high_loss_levels
            ).sum()
            /
            len(x)
            * 100
        )
        .reset_index()
    )


    result.columns = [
        factor,
        "中高程度脱发比例"
    ]


    # 总人数
    total_count = (
        temp.groupby(factor)
        .size()
        .reset_index(
            name="总人数"
        )
    )


    # 中高程度脱发人数
    high_loss_count = (
        temp.groupby(factor)["hair_loss"]
        .apply(
            lambda x:
            x.isin(
                high_loss_levels
            ).sum()
        )
        .reset_index(
            name="中高程度脱发人数"
        )
    )


    # 合并
    result = result.merge(
        total_count,
        on=factor
    )


    result = result.merge(
        high_loss_count,
        on=factor
    )


    # 调整列顺序
    result = result[
        [
            factor,
            "总人数",
            "中高程度脱发人数",
            "中高程度脱发比例"
        ]
    ]


    result.to_csv(
        os.path.join(
            RESULT_DIR,
            filename
        ),
        index=False,
        encoding="utf-8-sig"
    )


    print(
        f"已完成：{factor}"
    )


    return result


# ============================================================
# 各影响因素分析
# ============================================================

analyze_factor(
    df,
    "stay_up_late",
    "sleep_analysis.csv"
)


analyze_factor(
    df,
    "pressure_level",
    "pressure_analysis.csv"
)


analyze_factor(
    df,
    "stress_level",
    "stress_analysis.csv"
)


analyze_factor(
    df,
    "coffee_consumed",
    "coffee_analysis.csv"
)


analyze_factor(
    df,
    "brain_working_duration",
    "brain_work_analysis.csv"
)


analyze_factor(
    df,
    "shampoo_brand",
    "shampoo_brand_analysis.csv"
)


analyze_factor(
    df,
    "swimming",
    "swimming_analysis.csv"
)


analyze_factor(
    df,
    "hair_washing",
    "hair_washing_analysis.csv"
)


analyze_factor(
    df,
    "hair_grease",
    "grease_analysis.csv"
)


analyze_factor(
    df,
    "libido",
    "libido_analysis.csv"
)


# ============================================================
# 因素差异排名
# ============================================================

print("\n正在计算因素差异排名...")


factors = [

    "libido",

    "coffee_consumed",

    "hair_grease",

    "stay_up_late",

    "stress_level",

    "brain_working_duration",

    "pressure_level",

    "shampoo_brand",

    "swimming",

    "hair_washing"
]


ranking = []


for factor in factors:

    if factor not in df.columns:
        continue


    temp = df[
        [factor, "hair_loss"]
    ].dropna()


    if len(temp) == 0:
        continue


    group_rates = (
        temp.groupby(factor)["hair_loss"]
        .apply(
            lambda x:
            x.isin(
                [
                    "Many",
                    "A lot"
                ]
            ).mean()
            * 100
        )
    )


    if len(group_rates) < 2:
        continue


    max_rate = group_rates.max()

    min_rate = group_rates.min()

    difference = (
        max_rate -
        min_rate
    )


    ranking.append({

        "因素": factor,

        "最高组脱发比例":
            round(
                max_rate,
                2
            ),

        "最低组脱发比例":
            round(
                min_rate,
                2
            ),

        "组间差异":
            round(
                difference,
                2
            )
    })


factor_ranking = pd.DataFrame(
    ranking
)


factor_ranking = (
    factor_ranking
    .sort_values(
        "组间差异",
        ascending=False
    )
)


factor_ranking.to_csv(
    os.path.join(
        RESULT_DIR,
        "factor_ranking.csv"
    ),
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 完成
# ============================================================

print("\n[8/8] 数据分析完成！")


print("\n最终数据规模：")

print(
    f"{df.shape[0]} 行 × {df.shape[1]} 列"
)


print("\n生成的结果文件：")


for filename in sorted(
    os.listdir(RESULT_DIR)
):

    if filename.endswith(".csv"):

        print(
            f"  └── {filename}"
        )


print("\n" + "=" * 60)

print("分析任务全部完成")

print("=" * 60)