import json

def handler(event, context):
    """
    AWS Lambda 的進入點 (Entry Point)。
    負責接收外部觸發的事件 (Event)，執行簡易邏輯後回傳結果。
    
    參數:
    - event: 觸發此 Lambda 的事件資料 (例如 API Gateway 傳入的 payload)。
    - context: 包含 Lambda 執行環境的運行時資訊 (Runtime information)。
    """
    # 嘗試從 event 中提取 'name' 欄位，若無則預設為 'World'
    name = event.get("name", "World")

    # 構建回傳結構，此格式相容於 AWS API Gateway 的預設整合回應
    response_body = {
        "message": f"Hello, {name}!! This Lambda is managed by Pulumi.",
        "status": "success"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_body)
    }