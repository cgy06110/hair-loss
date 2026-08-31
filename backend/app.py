from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

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

    df = pd.read_csv(
        file_path
    )

    # NaN 转成 None
    df = df.where(
        pd.notnull(df),
        None
    )

    return df.to_dict(
        orient="records"
    )


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
# 启动服务器
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
