import pandas as pd
import numpy as np
import os


# ============================================================
# 1. 路径配置
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "Luke_hair_loss_documentation.csv"
)

RESULT_DIR = os.path.join(
    BASE_DIR,
    "results"
)

os.makedirs(RESULT_DIR, exist_ok=True)


# ============================================================
# 2. 读取数据
# ============================================================

print("=" * 60)
print("脱发影响因素分析系统")
print("=" * 60)

print("\n[1/8] 正在读取数据...")

df = pd.read_csv(DATA_PATH)

print(
    f"数据规模：{df.shape[0]} 行 × {df.shape[1]} 列"
)

print("\n原始字段：")
print(df.columns.tolist())


# ============================================================
# 3. 字段清理
# ============================================================

print("\n[2/8] 正在进行字段清理...")

# 去除字段名前后的空格
df.columns = df.columns.str.strip()

# 修正字段拼写
if "school_assesssment" in df.columns:

    df.rename(
        columns={
            "school_assesssment": "school_assessment"
        },
        inplace=True
    )

print("字段清理完成。")


# ============================================================
# 4. 数据质量检查
# ============================================================

print("\n[3/8] 正在检查数据质量...")

print("\n缺失值：")
print(df.isnull().sum())

duplicate_count = df.duplicated().sum()

print(
    f"\n重复数据：{duplicate_count} 条"
)


# ============================================================
# 5. 删除重复数据
# ============================================================

if duplicate_count > 0:

    df = df.drop_duplicates()

print(
    f"去重后数据量：{len(df)} 条"
)


# ============================================================
# 6. 日期处理
# ============================================================

if "date" in df.columns:

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )


# ============================================================
# 7. 数据清洗
# ============================================================

print("\n[4/8] 正在清洗数据...")


# ------------------------------------------------------------
# 7.1 hair_grease 是真正的数值变量
# ------------------------------------------------------------

if "hair_grease" in df.columns:

    df["hair_grease"] = pd.to_numeric(
        df["hair_grease"],
        errors="coerce"
    )

    if df["hair_grease"].isnull().sum() > 0:

        median_value = df["hair_grease"].median()

        df["hair_grease"] = (
            df["hair_grease"]
            .fillna(median_value)
        )

        print(
            f"hair_grease："
            f"使用中位数 {median_value} "
            f"填充缺失值"
        )


# ------------------------------------------------------------
# 7.2 分类变量保持原始数据
# ------------------------------------------------------------

categorical_columns = [
    "hair_loss",
    "stay_up_late",
    "pressure_level",
    "coffee_consumed",
    "brain_working_duration",
    "school_assessment",
    "stress_level",
    "shampoo_brand",
    "swimming",
    "hair_washing",
    "dandruff",
    "libido"
]

for column in categorical_columns:

    if column in df.columns:

        # 只清理字符串前后空格
        df[column] = df[column].apply(
            lambda x:
            x.strip()
            if isinstance(x, str)
            else x
        )


# ============================================================
# 8. 删除缺失比例过高的字段
# ============================================================

print("\n[5/8] 检查缺失严重字段...")

drop_columns = []

for column in df.columns:

    missing_ratio = df[column].isnull().mean()

    if missing_ratio > 0.5:

        drop_columns.append(column)


if drop_columns:

    print(
        "以下字段缺失比例超过 50%，"
        "暂不参与主要分析："
    )

    for column in drop_columns:

        print(
            f"  {column}: "
            f"{df[column].isnull().mean() * 100:.2f}%"
        )

    df.drop(
        columns=drop_columns,
        inplace=True
    )


# ============================================================
# 9. 保存清洗后的数据
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
# 10. 总体脱发情况
# ============================================================

print("\n[7/8] 正在进行数据分析...")


# ------------------------------------------------------------
# 10.1 总体数据
# ------------------------------------------------------------

overview = pd.DataFrame({
    "指标": [
        "样本总数"
    ],
    "数值": [
        len(df)
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


# ------------------------------------------------------------
# 10.2 脱发程度分布
# ------------------------------------------------------------

hair_loss_distribution = (
    df["hair_loss"]
    .value_counts()
    .reset_index()
)

hair_loss_distribution.columns = [
    "脱发程度",
    "人数"
]

hair_loss_distribution["比例"] = (
    hair_loss_distribution["人数"]
    / len(df)
    * 100
).round(2)

hair_loss_distribution.to_csv(
    os.path.join(
        RESULT_DIR,
        "hair_loss_distribution.csv"
    ),
    index=False,
    encoding="utf-8-sig"
)

print(
    "已完成：hair_loss"
)


# ============================================================
# 11. 分类因素分析函数
# ============================================================

def analyze_factor(
    data,
    factor,
    filename
):

    if factor not in data.columns:
        return

    temp = data[
        [factor, "hair_loss"]
    ].dropna()

    if len(temp) == 0:
        return

    # 统计每个因素类别对应的脱发程度
    result = (
        temp
        .groupby(factor)["hair_loss"]
        .value_counts()
        .unstack(fill_value=0)
    )

    # 标准化脱发程度
    levels = [
        "Few",
        "Medium",
        "Many",
        "A lot"
    ]

    for level in levels:

        if level not in result.columns:

            result[level] = 0

    result = result[levels]

    # 总人数
    result["总人数"] = (
        result.sum(axis=1)
    )

    # 中高程度脱发
    result["中高程度脱发人数"] = (
        result["Medium"]
        + result["Many"]
        + result["A lot"]
    )

    # 中高程度脱发比例
    result["中高程度脱发比例"] = (
        result["中高程度脱发人数"]
        / result["总人数"]
        * 100
    ).round(2)

    result = result.reset_index()

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


# ============================================================
# 12. 影响因素分析
# ============================================================

factors = [
    ("stay_up_late", "sleep_analysis.csv"),
    ("pressure_level", "pressure_analysis.csv"),
    ("stress_level", "stress_analysis.csv"),
    ("coffee_consumed", "coffee_analysis.csv"),
    (
        "brain_working_duration",
        "brain_work_analysis.csv"
    ),
    ("shampoo_brand", "shampoo_analysis.csv"),
    ("swimming", "swimming_analysis.csv"),
    ("hair_washing", "hair_washing_analysis.csv"),
    ("hair_grease", "grease_analysis.csv"),
    ("libido", "libido_analysis.csv")
]


for factor, filename in factors:

    analyze_factor(
        df,
        factor,
        filename
    )


# ============================================================
# 13. 因素差异排名
# ============================================================

print(
    "\n正在计算因素差异排名..."
)

ranking = []

factor_names = [
    "stay_up_late",
    "pressure_level",
    "stress_level",
    "coffee_consumed",
    "brain_working_duration",
    "shampoo_brand",
    "swimming",
    "hair_washing",
    "hair_grease",
    "libido"
]


for factor in factor_names:

    if factor not in df.columns:
        continue

    temp = df[
        [factor, "hair_loss"]
    ].dropna()

    if len(temp) == 0:
        continue

    # 每个分组的中高程度脱发比例
    grouped = (
        temp
        .groupby(factor)["hair_loss"]
        .apply(
            lambda x:
            x.isin(
                [
                    "Medium",
                    "Many",
                    "A lot"
                ]
            ).mean()
            * 100
        )
    )

    if len(grouped) < 2:
        continue

    max_rate = grouped.max()

    min_rate = grouped.min()

    difference = (
        max_rate
        - min_rate
    )

    ranking.append({
        "因素": factor,
        "最高组脱发比例": round(
            max_rate,
            2
        ),
        "最低组脱发比例": round(
            min_rate,
            2
        ),
        "组间差异": round(
            difference,
            2
        )
    })


factor_ranking = pd.DataFrame(
    ranking
)


if len(factor_ranking) > 0:

    factor_ranking = (
        factor_ranking
        .sort_values(
            by="组间差异",
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
# 14. 输出结果
# ============================================================

print(
    "\n[8/8] 数据分析完成！"
)

print(
    "\n最终数据规模："
)

print(
    f"{df.shape[0]} 行 × "
    f"{df.shape[1]} 列"
)

print(
    "\n生成的结果文件："
)

for file in sorted(
    os.listdir(RESULT_DIR)
):

    print(
        "  └──",
        file
    )


print(
    "\n" + "=" * 60
)

print(
    "分析任务全部完成"
)

print(
    "=" * 60
)
