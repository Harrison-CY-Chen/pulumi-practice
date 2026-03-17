import unittest
import json
from index import handler

class TestLambdaHandler(unittest.TestCase):
    
    def test_handler_with_custom_name(self):
        """測試：當 Event 包含自訂名稱時，是否正確回傳對應訊息"""
        # 模擬傳入的 Event 與 Context
        mock_event = {"name": "Cloud Native"}
        mock_context = {} 
        
        # 執行 handler
        response = handler(mock_event, mock_context)
        body = json.loads(response["body"])
        
        # 斷言 (Assertions)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["message"], "Hello, Cloud Native! This Lambda is managed by Pulumi.")
        self.assertEqual(body["status"], "success")

    def test_handler_with_empty_event(self):
        """測試：當 Event 為空時，是否正確使用預設值"""
        mock_event = {}
        mock_context = {}
        
        response = handler(mock_event, mock_context)
        body = json.loads(response["body"])
        
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["message"], "Hello, World! This Lambda is managed by Pulumi.")