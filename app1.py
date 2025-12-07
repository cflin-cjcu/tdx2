"""
台鐵列車即時動態資訊系統 - PyEcharts 版本
使用 Flask + PyEcharts 建立互動式網頁介面
"""

from flask import Flask, render_template_string, jsonify
from pyecharts import options as opts
from pyecharts.charts import Bar, Page
import json
from datetime import datetime
from tdx_service import get_train_data

app = Flask(__name__)

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚂 台鐵列車即時動態資訊系統 - PyEcharts</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft JhengHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .controls {
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .btn {
            background: #0066cc;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .btn:hover {
            background: #0052a3;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .status-info {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .status-badge {
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
        }
        
        .status-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .update-time {
            color: #6c757d;
            font-size: 14px;
        }
        
        .legend-card {
            margin: 20px 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }
        
        .legend-card h3 {
            color: #0066cc;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .legend-items {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        
        .legend-green {
            background: #d4edda;
            color: #155724;
        }
        
        .legend-yellow {
            background: #fff3cd;
            color: #856404;
        }
        
        .legend-orange {
            background: #ffe5cc;
            color: #cc5200;
        }
        
        .legend-red {
            background: #f8d7da;
            color: #721c24;
        }
        
        .chart-container {
            padding: 30px;
        }
        
        #barChart {
            width: 100%;
            height: 500px;
        }
        
        .table-container {
            padding: 30px;
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        th {
            background: #0066cc;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .delay-0 {
            background: #d4edda !important;
            color: #155724;
            font-weight: bold;
        }
        
        .delay-light {
            background: #fff3cd !important;
            color: #856404;
            font-weight: bold;
        }
        
        .delay-medium {
            background: #ffe5cc !important;
            color: #cc5200;
            font-weight: bold;
        }
        
        .delay-severe {
            background: #f8d7da !important;
            color: #721c24;
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            font-size: 18px;
            color: #6c757d;
        }
        
        .loading::after {
            content: '...';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60%, 100% { content: '...'; }
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .status-info {
                flex-direction: column;
                align-items: stretch;
            }
            
            table {
                font-size: 12px;
            }
            
            th, td {
                padding: 8px 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚂 台鐵列車即時動態資訊系統</h1>
            <p>PyEcharts 互動式圖表版本</p>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="refreshData()">🔄 重新整理</button>
            <div class="status-info">
                <div id="statusBadge" class="status-badge status-success">準備就緒</div>
                <div id="updateTime" class="update-time">等待載入資料...</div>
            </div>
        </div>
        
        <div class="legend-card">
            <h3>📊 延遲狀態標示</h3>
            <div class="legend-items">
                <span class="legend-item legend-green">🟢 準點 (0 分鐘)</span>
                <span class="legend-item legend-yellow">🟡 輕微延遲 (1-5 分鐘)</span>
                <span class="legend-item legend-orange">🟠 中度延遲 (6-10 分鐘)</span>
                <span class="legend-item legend-red">🔴 嚴重延遲 (>10 分鐘)</span>
            </div>
        </div>
        
        <div class="chart-container">
            <h3 style="color: #0066cc; margin-bottom: 20px; font-size: 1.5em;">📈 列車延遲時間圖表</h3>
            <div id="barChart"></div>
        </div>
        
        <div class="table-container">
            <h3 style="color: #0066cc; margin-bottom: 20px; font-size: 1.5em;">📋 列車詳細資訊</h3>
            <div id="dataTable"></div>
        </div>
    </div>
    
    <script>
        let autoRefreshInterval;
        
        // 取得延遲狀態的 CSS 類別
        function getDelayClass(delay) {
            if (delay === 0) return 'delay-0';
            if (delay <= 5) return 'delay-light';
            if (delay <= 10) return 'delay-medium';
            return 'delay-severe';
        }
        
        // 更新資料
        async function refreshData() {
            try {
                const statusBadge = document.getElementById('statusBadge');
                statusBadge.className = 'status-badge status-warning';
                statusBadge.textContent = '載入中...';
                
                const response = await fetch('/api/train-data');
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // 更新圖表
                updateChart(data.trains);
                
                // 更新表格
                updateTable(data.trains);
                
                // 更新狀態
                statusBadge.className = 'status-badge status-success';
                statusBadge.textContent = `✅ ${data.trains.length} 筆資料`;
                
                document.getElementById('updateTime').textContent = 
                    `最後更新: ${new Date().toLocaleString('zh-TW')}`;
                    
            } catch (error) {
                console.error('錯誤:', error);
                const statusBadge = document.getElementById('statusBadge');
                statusBadge.className = 'status-badge status-error';
                statusBadge.textContent = '❌ 載入失敗';
            }
        }
        
        // 更新 ECharts 圖表
        function updateChart(trains) {
            const chart = echarts.init(document.getElementById('barChart'));
            
            const trainNos = trains.map(t => t.車次);
            const delays = trains.map(t => t.延遲時間);
            
            // 根據延遲時間設定顏色
            const colors = delays.map(delay => {
                if (delay === 0) return '#28a745';
                if (delay <= 5) return '#ffc107';
                if (delay <= 10) return '#fd7e14';
                return '#dc3545';
            });
            
            const option = {
                title: {
                    text: '各車次延遲時間統計',
                    left: 'center',
                    textStyle: {
                        color: '#0066cc',
                        fontSize: 20,
                        fontWeight: 'bold'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: function(params) {
                        const data = params[0];
                        const trainInfo = trains[data.dataIndex];
                        return `
                            <strong>車次:</strong> ${trainInfo.車次}<br/>
                            <strong>列車類型:</strong> ${trainInfo.列車類型}<br/>
                            <strong>即將到達:</strong> ${trainInfo.即將到達}<br/>
                            <strong>延遲時間:</strong> ${trainInfo.延遲時間} 分鐘
                        `;
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: trainNos,
                    axisLabel: {
                        rotate: 45,
                        interval: 0,
                        fontSize: 10
                    },
                    name: '車次',
                    nameLocation: 'middle',
                    nameGap: 60,
                    nameTextStyle: {
                        fontSize: 14,
                        fontWeight: 'bold'
                    }
                },
                yAxis: {
                    type: 'value',
                    name: '延遲時間 (分鐘)',
                    nameTextStyle: {
                        fontSize: 14,
                        fontWeight: 'bold'
                    }
                },
                series: [{
                    name: '延遲時間',
                    type: 'bar',
                    data: delays,
                    itemStyle: {
                        color: function(params) {
                            return colors[params.dataIndex];
                        }
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{c}'
                    }
                }]
            };
            
            chart.setOption(option);
            
            // 響應式調整
            window.addEventListener('resize', function() {
                chart.resize();
            });
        }
        
        // 更新表格
        function updateTable(trains) {
            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>序號</th>
                            <th>車次</th>
                            <th>列車類型</th>
                            <th>即將到達</th>
                            <th>延遲時間</th>
                            <th>更新時間</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            trains.forEach(train => {
                const delayClass = getDelayClass(train.延遲時間);
                html += `
                    <tr>
                        <td>${train.序號}</td>
                        <td>${train.車次}</td>
                        <td>${train.列車類型}</td>
                        <td>${train.即將到達}</td>
                        <td class="${delayClass}">${train.延遲時間} 分鐘</td>
                        <td>${train.更新時間}</td>
                    </tr>
                `;
            });
            
            html += `
                    </tbody>
                </table>
            `;
            
            document.getElementById('dataTable').innerHTML = html;
        }
        
        // 頁面載入時執行
        window.onload = function() {
            refreshData();
            
            // 每 30 秒自動更新
            autoRefreshInterval = setInterval(refreshData, 30000);
        };
        
        // 頁面關閉時清除定時器
        window.onbeforeunload = function() {
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
            }
        };
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """主頁面"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/train-data')
def get_train_data_api():
    """API 端點：取得列車資料"""
    try:
        trains = get_train_data()
        return jsonify({
            'success': True,
            'trains': trains,
            'count': len(trains),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚂 台鐵列車即時動態資訊系統 (PyEcharts 版本)")
    print("=" * 60)
    print("正在啟動服務...")
    print("請在瀏覽器開啟: http://127.0.0.1:5000")
    print("按 Ctrl+C 可停止服務")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
