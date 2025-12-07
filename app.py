"""
台鐵列車即時動態資訊系統 - 主應用程式
使用 Plotly Dash 建立互動式網頁介面
"""

import dash
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import traceback
from tdx_service import get_train_data


# 初始化 Dash 應用程式
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="台鐵列車即時動態資訊系統"
)

# 定義延遲狀態的顏色樣式
def get_delay_style(delay_time):
    """
    根據延遲時間回傳對應的樣式
    
    Args:
        delay_time: 延遲分鐘數
        
    Returns:
        dict: 樣式字典
    """
    if delay_time == 0:
        return {
            'backgroundColor': '#d4edda',
            'color': '#155724',
            'fontWeight': 'bold'
        }
    elif delay_time <= 5:
        return {
            'backgroundColor': '#fff3cd',
            'color': '#856404',
            'fontWeight': 'bold'
        }
    elif delay_time <= 10:
        return {
            'backgroundColor': '#ffe5cc',
            'color': '#cc5200',
            'fontWeight': 'bold'
        }
    else:
        return {
            'backgroundColor': '#f8d7da',
            'color': '#721c24',
            'fontWeight': 'bold'
        }


# 應用程式布局
app.layout = dbc.Container([
    # 標題區域
    dbc.Row([
        dbc.Col([
            html.H1(
                "🚂 台鐵列車即時動態資訊系統",
                className="text-center my-4",
                style={'color': '#0066cc'}
            )
        ])
    ]),
    
    # 控制按鈕區域
    dbc.Row([
        dbc.Col([
            dbc.Button(
                "🔄 重新整理",
                id="refresh-button",
                color="primary",
                className="me-2"
            ),
            html.Span(
                id="last-update-time",
                className="text-muted ms-3"
            )
        ], className="mb-3")
    ]),
    
    # 狀態訊息區域
    dbc.Row([
        dbc.Col([
            html.Div(id="status-message")
        ])
    ]),
    
    # 延遲狀態說明
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("延遲狀態標示", className="card-title"),
                    html.Div([
                        html.Span("🟢 準點 (0 分鐘)", 
                                 style={'backgroundColor': '#d4edda', 
                                       'padding': '5px 10px', 
                                       'marginRight': '10px',
                                       'borderRadius': '3px'}),
                        html.Span("🟡 輕微延遲 (1-5 分鐘)", 
                                 style={'backgroundColor': '#fff3cd', 
                                       'padding': '5px 10px', 
                                       'marginRight': '10px',
                                       'borderRadius': '3px'}),
                        html.Span("🟠 中度延遲 (6-10 分鐘)", 
                                 style={'backgroundColor': '#ffe5cc', 
                                       'padding': '5px 10px', 
                                       'marginRight': '10px',
                                       'borderRadius': '3px'}),
                        html.Span("🔴 嚴重延遲 (>10 分鐘)", 
                                 style={'backgroundColor': '#f8d7da', 
                                       'padding': '5px 10px',
                                       'borderRadius': '3px'})
                    ])
                ])
            ], className="mb-3")
        ])
    ]),
    
    # 資料表格區域
    dbc.Row([
        dbc.Col([
            html.Div(id="train-table-container")
        ])
    ]),
    
    # 延遲時間圖表區域
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("列車延遲時間圖表", className="card-title mb-3"),
                    dcc.Graph(id="delay-bar-chart")
                ])
            ], className="mt-4")
        ])
    ]),
    
    # 自動更新組件 (每 30 秒)
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # 30 秒 (毫秒)
        n_intervals=0
    ),
    
    # 載入時觸發更新
    dcc.Store(id='trigger-on-load', data=0)
    
], fluid=True, style={'maxWidth': '1400px'})


@callback(
    [Output('train-table-container', 'children'),
     Output('status-message', 'children'),
     Output('last-update-time', 'children'),
     Output('delay-bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('refresh-button', 'n_clicks'),
     Input('trigger-on-load', 'data')]
)
def update_train_table(n_intervals, n_clicks, trigger):
    """
    更新列車資料表格和圖表
    
    Args:
        n_intervals: 自動更新計數
        n_clicks: 手動更新點擊次數
        trigger: 載入觸發
        
    Returns:
        tuple: (表格組件, 狀態訊息, 更新時間, 圖表)
    """
    try:
        # 取得列車資料
        train_data = get_train_data()
        
        if not train_data:
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title="目前沒有列車資料",
                xaxis_title="車次",
                yaxis_title="延遲時間 (分鐘)"
            )
            return (
                html.Div("目前沒有列車資料", className="alert alert-warning"),
                dbc.Alert("⚠️ 未取得列車資料", color="warning"),
                f"最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                empty_fig
            )
        
        # 建立 DataFrame
        df = pd.DataFrame(train_data)
        
        # 建立資料表格
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns],
            style_table={
                'overflowX': 'auto',
                'border': '1px solid #dee2e6'
            },
            style_header={
                'backgroundColor': '#0066cc',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'padding': '12px'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontSize': '14px',
                'fontFamily': 'Arial, sans-serif'
            },
            style_data={
                'border': '1px solid #dee2e6'
            },
            style_data_conditional=[
                # 根據延遲時間設定行樣式
                {
                    'if': {
                        'filter_query': '{延遲時間} = 0',
                        'column_id': '延遲時間'
                    },
                    **get_delay_style(0)
                },
                {
                    'if': {
                        'filter_query': '{延遲時間} > 0 && {延遲時間} <= 5',
                        'column_id': '延遲時間'
                    },
                    **get_delay_style(3)
                },
                {
                    'if': {
                        'filter_query': '{延遲時間} > 5 && {延遲時間} <= 10',
                        'column_id': '延遲時間'
                    },
                    **get_delay_style(8)
                },
                {
                    'if': {
                        'filter_query': '{延遲時間} > 10',
                        'column_id': '延遲時間'
                    },
                    **get_delay_style(15)
                }
            ],
            page_size=20,
            page_action='native',
            sort_action='native',
            filter_action='native'
        )
        
        # 建立 Bar Chart
        # 根據延遲時間設定顏色
        colors = []
        for delay in df['延遲時間']:
            if delay == 0:
                colors.append('#28a745')  # 綠色 - 準點
            elif delay <= 5:
                colors.append('#ffc107')  # 黃色 - 輕微延遲
            elif delay <= 10:
                colors.append('#fd7e14')  # 橘色 - 中度延遲
            else:
                colors.append('#dc3545')  # 紅色 - 嚴重延遲
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['車次'],
                y=df['延遲時間'],
                marker_color=colors,
                text=df['延遲時間'],
                textposition='outside',
                hovertemplate='<b>車次:</b> %{x}<br>' +
                              '<b>延遲時間:</b> %{y} 分鐘<br>' +
                              '<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '各車次延遲時間統計',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#0066cc'}
            },
            xaxis_title='車次',
            yaxis_title='延遲時間 (分鐘)',
            xaxis={
                'tickangle': -45,
                'tickfont': {'size': 10}
            },
            yaxis={
                'gridcolor': '#e0e0e0'
            },
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            height=500,
            margin=dict(t=80, b=100, l=60, r=40),
            hovermode='x unified'
        )
        
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return (
            table,
            dbc.Alert(f"✅ 成功載入 {len(train_data)} 筆列車資料", color="success"),
            f"最後更新: {update_time}",
            fig
        )
        
    except Exception as e:
        error_msg = str(e)
        print(f"錯誤: {error_msg}")
        print(traceback.format_exc())
        
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="資料載入失敗",
            xaxis_title="車次",
            yaxis_title="延遲時間 (分鐘)"
        )
        
        return (
            html.Div("資料載入失敗", className="alert alert-danger"),
            dbc.Alert(f"❌ 錯誤: {error_msg}", color="danger"),
            f"最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            empty_fig
        )


if __name__ == '__main__':
    print("=" * 60)
    print("🚂 台鐵列車即時動態資訊系統")
    print("=" * 60)
    print("正在啟動服務...")
    print("請在瀏覽器開啟: http://127.0.0.1:8050")
    print("按 Ctrl+C 可停止服務")
    print("=" * 60)
    
    app.run_server(debug=True, host='127.0.0.1', port=8050)
