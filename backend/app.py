from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

# PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ============================================================
# Flask
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# 路径
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESULT_DIR = os.path.join(
    BASE_DIR,
    "..",
    "analysis",
    "results"
)

RESULT_DIR = os.path.abspath(RESULT_DIR)


# ============================================================
# 注册中文字体
# ============================================================

def register_chinese_font():

    font_paths = [
        # Windows
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",

        # Linux
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]

    for font_path in font_paths:

        if os.path.exists(font_path):

            try:

                pdfmetrics.registerFont(
                    TTFont(
                        "ChineseFont",
                        font_path
                    )
                )

                return "ChineseFont"

            except Exception:
                continue

    return "Helvetica"


PDF_FONT = register_chinese_font()


# ============================================================
# 通用 CSV 读取函数
# ============================================================

def read_csv(filename):

    file_path = os.path.join(
        RESULT_DIR,
        filename
    )

    if not os.path.exists(file_path):

        return {
            "error": f"文件不存在：{filename}"
        }

    try:

        df = pd.read_csv(file_path)

        df = df.where(
            pd.notnull(df),
            None
        )

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# 首页
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "system": "脱发影响因素分析系统",
        "status": "running"
    })


# ============================================================
# 1. 总体数据
# ============================================================

@app.route("/api/overview")
def overview():

    return jsonify(
        read_csv("overview.csv")
    )


# ============================================================
# 2. 脱发程度分布
# ============================================================

@app.route("/api/hair-loss")
def hair_loss():

    return jsonify(
        read_csv(
            "hair_loss_distribution.csv"
        )
    )


# ============================================================
# 3. 熬夜
# ============================================================

@app.route("/api/sleep")
def sleep():

    return jsonify(
        read_csv(
            "sleep_analysis.csv"
        )
    )


# ============================================================
# 4. 压力水平
# ============================================================

@app.route("/api/pressure")
def pressure():

    return jsonify(
        read_csv(
            "pressure_analysis.csv"
        )
    )


# ============================================================
# 5. 压力等级
# ============================================================

@app.route("/api/stress")
def stress():

    return jsonify(
        read_csv(
            "stress_analysis.csv"
        )
    )


# ============================================================
# 6. 咖啡摄入
# ============================================================

@app.route("/api/coffee")
def coffee():

    return jsonify(
        read_csv(
            "coffee_analysis.csv"
        )
    )


# ============================================================
# 7. 脑力工作时间
# ============================================================

@app.route("/api/brain-work")
def brain_work():

    return jsonify(
        read_csv(
            "brain_work_analysis.csv"
        )
    )


# ============================================================
# 8. 洗发水品牌
# ============================================================

@app.route("/api/shampoo")
def shampoo():

    return jsonify(
        read_csv(
            "shampoo_analysis.csv"
        )
    )


# ============================================================
# 9. 游泳
# ============================================================

@app.route("/api/swimming")
def swimming():

    return jsonify(
        read_csv(
            "swimming_analysis.csv"
        )
    )


# ============================================================
# 10. 洗头习惯
# ============================================================

@app.route("/api/hair-washing")
def hair_washing():

    return jsonify(
        read_csv(
            "hair_washing_analysis.csv"
        )
    )


# ============================================================
# 11. 头发油脂
# ============================================================

@app.route("/api/grease")
def grease():

    return jsonify(
        read_csv(
            "grease_analysis.csv"
        )
    )


# ============================================================
# 12. libido
# ============================================================

@app.route("/api/libido")
def libido():

    return jsonify(
        read_csv(
            "libido_analysis.csv"
        )
    )


# ============================================================
# 13. 因素排名
# ============================================================

@app.route("/api/factors")
def factors():

    return jsonify(
        read_csv(
            "factor_ranking.csv"
        )
    )


# ============================================================
# PDF 辅助函数
# ============================================================

def create_table(data, col_widths=None):

    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#eeeeee")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                PDF_FONT
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    return table


def read_dataframe(filename):

    file_path = os.path.join(
        RESULT_DIR,
        filename
    )

    if not os.path.exists(file_path):

        return None

    try:

        return pd.read_csv(
            file_path
        )

    except Exception:

        return None


def dataframe_to_table(df, max_rows=15):

    if df is None or df.empty:

        return None

    temp = df.head(max_rows).copy()

    # 数字格式处理
    for column in temp.columns:

        temp[column] = temp[column].apply(
            lambda x:
            round(x, 2)
            if isinstance(x, float)
            else x
        )

    data = [
        list(temp.columns)
    ]

    for row in temp.itertuples(index=False):

        data.append(
            [
                "" if pd.isna(value)
                else str(value)
                for value in row
            ]
        )

    return create_table(data)


# ============================================================
# PDF 报告
# ============================================================

@app.route("/api/report")
def generate_report():

    try:

        # ----------------------------------------------------
        # 创建内存 PDF
        # ----------------------------------------------------

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ChineseTitle",
            parent=styles["Title"],
            fontName=PDF_FONT,
            fontSize=22,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=20
        )

        heading_style = ParagraphStyle(
            "ChineseHeading",
            parent=styles["Heading2"],
            fontName=PDF_FONT,
            fontSize=15,
            leading=22,
            spaceBefore=12,
            spaceAfter=10
        )

        body_style = ParagraphStyle(
            "ChineseBody",
            parent=styles["BodyText"],
            fontName=PDF_FONT,
            fontSize=10.5,
            leading=18,
            spaceAfter=8
        )

        small_style = ParagraphStyle(
            "ChineseSmall",
            parent=styles["BodyText"],
            fontName=PDF_FONT,
            fontSize=9,
            leading=15
        )


        story = []


        # ====================================================
        # 第一部分：标题
        # ====================================================

        story.append(
            Paragraph(
                "脱发影响因素分析报告",
                title_style
            )
        )

        story.append(
            Paragraph(
                "基于 Hadoop / HDFS 与 Python 数据分析",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                small_style
            )
        )

        story.append(
            Spacer(1, 20)
        )


        # ====================================================
        # 第二部分：数据概况
        # ====================================================

        story.append(
            Paragraph(
                "一、数据概况",
                heading_style
            )
        )

        cleaned_df = read_dataframe(
            "cleaned_data.csv"
        )

        if cleaned_df is not None:

            rows = len(cleaned_df)
            columns = len(cleaned_df.columns)

        else:

            rows = 400
            columns = 14

        overview_data = [
            ["指标", "结果"],
            ["数据来源", "HDFS"],
            ["样本数量", str(rows)],
            ["字段数量", str(columns)],
            ["分析方式", "Python 数据分析"],
        ]

        story.append(
            create_table(
                overview_data,
                [180, 260]
            )
        )

        story.append(
            Spacer(1, 15)
        )

        story.append(
            Paragraph(
                "本报告基于存储在 HDFS 中的脱发相关数据，通过 Python "
                "进行数据清洗、统计分析，并对不同因素与脱发程度之间的差异进行比较。",
                body_style
            )
        )


        # ====================================================
        # 第三部分：脱发程度
        # ====================================================

        story.append(
            Paragraph(
                "二、脱发程度总体分布",
                heading_style
            )
        )

        hair_df = read_dataframe(
            "hair_loss_distribution.csv"
        )

        table = dataframe_to_table(
            hair_df
        )

        if table:

            story.append(table)

        else:

            story.append(
                Paragraph(
                    "暂无脱发程度分布数据。",
                    body_style
                )
            )


        # ====================================================
        # 第四部分：因素排名
        # ====================================================

        story.append(
            Paragraph(
                "三、脱发影响因素排名",
                heading_style
            )
        )

        factor_df = read_dataframe(
            "factor_ranking.csv"
        )

        table = dataframe_to_table(
            factor_df,
            max_rows=20
        )

        if table:

            story.append(table)

        else:

            story.append(
                Paragraph(
                    "暂无因素排名数据。",
                    body_style
                )
            )


        story.append(
            Spacer(1, 15)
        )


        # ====================================================
        # 自动生成主要结论
        # ====================================================

        if factor_df is not None and len(factor_df) > 0:

            factor_df = factor_df.copy()

            # 根据你的实际结果字段
            factor_column = None
            difference_column = None

            for col in factor_df.columns:

                if str(col) in [
                    "因素",
                    "factor"
                ]:

                    factor_column = col

                if str(col) in [
                    "组间差异",
                    "difference",
                    "差异"
                ]:

                    difference_column = col

            if factor_column is None:

                factor_column = factor_df.columns[0]

            if difference_column is None and len(factor_df.columns) >= 2:

                difference_column = factor_df.columns[-1]

            try:

                factor_df[difference_column] = pd.to_numeric(
                    factor_df[difference_column],
                    errors="coerce"
                )

                factor_df = factor_df.dropna(
                    subset=[difference_column]
                )

                if len(factor_df) > 0:

                    top_factor = factor_df.iloc[0][factor_column]
                    top_difference = factor_df.iloc[0][difference_column]

                    story.append(
                        Paragraph(
                            "主要发现",
                            heading_style
                        )
                    )

                    story.append(
                        Paragraph(
                            f"根据因素差异排名，当前数据中差异最大的因素为 "
                            f"<b>{top_factor}</b>，其最高组与最低组之间的脱发比例差异约为 "
                            f"<b>{float(top_difference):.2f}</b> 个百分点。",
                            body_style
                        )

                    )

            except Exception:
                pass


        # ====================================================
        # 第五部分：主要因素分析
        # ====================================================

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "四、主要影响因素分析",
                heading_style
            )
        )


        analysis_files = [
            (
                "压力水平",
                "pressure_analysis.csv"
            ),
            (
                "熬夜情况",
                "sleep_analysis.csv"
            ),
            (
                "压力等级",
                "stress_analysis.csv"
            ),
            (
                "咖啡摄入",
                "coffee_analysis.csv"
            ),
            (
                "脑力工作时间",
                "brain_work_analysis.csv"
            ),
            (
                "洗发水品牌",
                "shampoo_brand_analysis.csv"
            ),
            (
                "游泳情况",
                "swimming_analysis.csv"
            ),
            (
                "洗头习惯",
                "hair_washing_analysis.csv"
            ),
            (
                "头发油脂",
                "grease_analysis.csv"
            ),
            (
                "libido",
                "libido_analysis.csv"
            )
        ]


        for title, filename in analysis_files:

            df = read_dataframe(filename)

            if df is None:

                continue

            story.append(
                Paragraph(
                    title,
                    ParagraphStyle(
                        f"sub_{filename}",
                        parent=heading_style,
                        fontSize=12
                    )
                )
            )

            table = dataframe_to_table(
                df,
                max_rows=10
            )

            if table:

                story.append(table)
                story.append(
                    Spacer(1, 10)
                )


        # ====================================================
        # 第六部分：分析说明
        # ====================================================

        story.append(
            Paragraph(
                "五、分析说明",
                heading_style
            )
        )

        story.append(
            Paragraph(
                "本报告中的结果来自当前数据集的统计分析。"
                "因素排名主要用于比较不同因素分组之间的脱发比例差异，"
                "差异较大的因素可作为进一步研究和风险评估的重点。"
                "需要注意的是，统计关联不等同于因果关系，"
                "本报告结果不能直接作为医学诊断依据。",
                body_style
            )
        )


        # ====================================================
        # 生成 PDF
        # ====================================================

        doc.build(story)

        buffer.seek(0)

        filename = (
            "hair_loss_analysis_report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".pdf"
        )

        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf"
        )


    except Exception as e:

        print("PDF 报告生成失败：")
        print(e)

        return jsonify({
            "error": "PDF报告生成失败",
            "detail": str(e)
        }), 500


# ============================================================
# 启动服务器
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("脱发影响因素分析系统 Flask 后端")
    print("=" * 60)

    print("分析结果目录：")
    print(RESULT_DIR)

    print("PDF报告接口：")
    print("http://localhost:5000/api/report")

    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )