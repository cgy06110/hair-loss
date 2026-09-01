// ============================================================
// 脱发影响因素分析系统 - 前端可视化
// 数据来源：Flask 后端 API
// ============================================================

console.log("script.js 已加载");

console.log("Chart.js：", typeof Chart);

// ============================================================
// Flask 后端地址
// ============================================================

const API_BASE = "http://127.0.0.1:5000/api";


// ============================================================
// 页面切换
// ============================================================

function showPage(pageId, button) {

    // 隐藏所有页面
    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active");
    });

    // 显示目标页面
    const targetPage = document.getElementById(pageId);

    if (targetPage) {
        targetPage.classList.add("active");
    }

    // 修改菜单选中状态
    document.querySelectorAll(".menu-item").forEach(item => {
        item.classList.remove("active");
    });

    if (button) {
        button.classList.add("active");
    }

    // 修改标题
    const titles = {
        overview: "总体概况",
        distribution: "脱发程度分布",
        sleep: "熬夜因素分析",
        pressure: "压力因素分析",
        coffee: "咖啡摄入分析",
        hair: "头发护理分析",
        ranking: "影响因素排名"
    };

    const title = document.getElementById("page-title");

    if (title && titles[pageId]) {
        title.innerText = titles[pageId];
    }
}


// ============================================================
// 从 Flask API 获取数据
// ============================================================

async function loadData(apiName) {

    const response = await fetch(
        API_BASE + "/" + apiName
    );

    if (!response.ok) {
        throw new Error(
            "API 请求失败：" + apiName
        );
    }

    const data = await response.json();

    // 后端返回错误
    if (data.error) {
        throw new Error(data.error);
    }

    return data;
}


// ============================================================
// 通用：获取字段
// ============================================================

function getField(item, fields) {

    for (const field of fields) {

        if (
            item[field] !== undefined &&
            item[field] !== null &&
            item[field] !== ""
        ) {
            return item[field];
        }
    }

    return null;
}


// ============================================================
// 1. 脱发程度分布
// ============================================================

async function initDistributionChart() {

    try {

        const data = await loadData("hair-loss");

        console.log("脱发程度数据：", data);

        const labels = data.map(item =>
            getField(item, [
                "hair_loss",
                "脱发程度"
            ])
        );

        const values = data.map(item =>
            Number(
                getField(item, [
                    "总人数",
                    "total",
                    "count",
                    "人数"
                ]) || 0
            )
        );


        // 环形图
        const distributionCanvas =
            document.getElementById("distributionChart");

        if (distributionCanvas) {

            new Chart(
                distributionCanvas,
                {
                    type: "doughnut",

                    data: {
                        labels: labels,

                        datasets: [{
                            label: "人数",
                            data: values
                        }]
                    },

                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                }
            );
        }


        // 柱状图
        const hairLossCanvas =
            document.getElementById("hairLossChart");

        if (hairLossCanvas) {

            new Chart(
                hairLossCanvas,
                {
                    type: "bar",

                    data: {
                        labels: labels,

                        datasets: [{
                            label: "人数",
                            data: values
                        }]
                    },

                    options: {
                        responsive: true,
                        maintainAspectRatio: false,

                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                }
            );
        }

    } catch (error) {

        console.error(
            "脱发程度图表加载失败：",
            error
        );
    }
}


// ============================================================
// 2. 压力因素
// ============================================================

async function initPressureChart() {

    try {

        const data = await loadData("pressure");

        console.log("压力数据：", data);

        const labels = data.map(item =>
            item.pressure_level
        );

        const values = data.map(item =>
            Number(
                item["中高程度脱发比例"] || 0
            )
        );

        const canvas =
            document.getElementById("pressureChart");

        if (!canvas) return;

        new Chart(
            canvas,
            {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [{
                        label: "中高程度脱发比例 (%)",
                        data: values
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            }
        );

    } catch (error) {

        console.error(
            "压力图表加载失败：",
            error
        );
    }
}


// ============================================================
// 3. 熬夜因素
// ============================================================

async function initSleepChart() {

    try {

        const data = await loadData("sleep");

        console.log("熬夜数据：", data);

        const labels = data.map(item =>
            item.stay_up_late
        );

        const values = data.map(item =>
            Number(
                getField(item, [
                    "中高程度脱发比例",
                    "rate",
                    "ratio"
                ]) || 0
            )
        );

        const canvas =
            document.getElementById("sleepChart");

        if (!canvas) return;

        new Chart(
            canvas,
            {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [{
                        label: "中高程度脱发比例 (%)",
                        data: values
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            }
        );

    } catch (error) {

        console.error(
            "熬夜图表加载失败：",
            error
        );
    }
}


// ============================================================
// 4. 咖啡摄入
// ============================================================

async function initCoffeeChart() {

    try {

        const data = await loadData("coffee");

        console.log("咖啡数据：", data);

        const labels = data.map(item =>
            item.coffee_consumed
        );

        const values = data.map(item =>
            Number(
                getField(item, [
                    "中高程度脱发比例",
                    "rate",
                    "ratio"
                ]) || 0
            )
        );

        const canvas =
            document.getElementById("coffeeChart");

        if (!canvas) return;

        new Chart(
            canvas,
            {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [{
                        label: "中高程度脱发比例 (%)",
                        data: values
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            }
        );

    } catch (error) {

        console.error(
            "咖啡图表加载失败：",
            error
        );
    }
}


// ============================================================
// 5. 因素影响排名
// ============================================================

async function initRankingChart() {

    try {

        const data = await loadData("factors");

        console.log("因素排名数据：", data);

        const labels = data.map(item =>
            getField(item, [
                "factor",
                "因素"
            ])
        );

        const values = data.map(item =>
            Number(
                getField(item, [
                    "组间差异",
                    "difference",
                    "差异",
                    "score"
                ]) || 0
            )
        );

        const canvas =
            document.getElementById("rankingChart");

        if (!canvas) return;

        new Chart(
            canvas,
            {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [{
                        label: "因素差异程度",
                        data: values
                    }]
                },

                options: {
                    indexAxis: "y",

                    responsive: true,
                    maintainAspectRatio: false,

                    scales: {
                        x: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );

    } catch (error) {

        console.error(
            "因素排名图表加载失败：",
            error
        );
    }
}


// ============================================================
// 初始化所有图表
// ============================================================

async function initCharts() {

    console.log("开始加载数据分析结果...");

    await initDistributionChart();

    await initPressureChart();

    await initSleepChart();

    await initCoffeeChart();

    await initRankingChart();

    console.log("所有图表加载完成！");
}


// ============================================================
// 页面加载
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initCharts();

    }
);