### 1. 透過 AWS Console 建立一個 Lambda Function
取得建立的 Lambda Function 的名稱 - `pulumi-practice-lambda`

### 2. 將現有的 AWS Lambda 匯入 (Import) 到 Pulumi
使用 `pulumi import` 指令將雲端上的資源納入 Pulumi local state 中：
```bash
pulumi import aws:lambda/function:Function pulumi-practice-lambda pulumi-practice-lambda --yes
```
- **參數說明**：
  - `aws:lambda/function:Function`：指定要 import 的資源型別（AWS Lambda）。
  - 第一個 `pulumi-practice-lambda`：指定 Pulumi 在這份程式碼中給它取的變數名稱（Logical Name）。
  - 第二個 `pulumi-practice-lambda`：對應 AWS 上實際的 Function Name（Physical Name）。
- **原理**：Pulumi 會連上 AWS 抓取這個 Lambda 的現有設定檔，並把這份設定紀錄到本地端（`~/.pulumi/...`）的 state.json 裡。同時它會在終端機印出一份 `__main__.py` 的標準定義檔供複製貼上。

### 3. 將自動產生的定義檔轉為「從本地部署」
匯入成功後，把 Pulumi 產生的程式碼貼到 `__main__.py` 中。
原先產生的程式碼會有特徵屬性：
```python
code_sha256="HAPq9EReJVEC...==", # 雲端上現有的 ZIP 檔案 hash
handler="lambda_function.lambda_handler", # 雲端原先的 handler
# ... 省略
opts = pulumi.ResourceOptions(protect=True) # 防止資源被意外刪除
```

**為了能從本地更新 `index.py`，做以下修改：**
1. 將原本寫死的 `code_sha256` 移除，改使用 `pulumi.AssetArchive`，並對應到當前目錄的 `./index.py`。
2. 將 `handler` 改成與本地 Python 對齊的 `index.handler`。

修改後的特徵片段如下：
```python
pulumi_practice_lambda = aws.lambda_.Function("pulumi-practice-lambda",
    code=pulumi.AssetArchive({"index.py": pulumi.FileAsset("./index.py")}),
    handler="index.handler",
    # ... 省略其餘屬性
    opts=pulumi.ResourceOptions(protect=True))
```
- **背後原理**：當我們設定 `code=pulumi.AssetArchive(...)` 後，Pulumi 就接管了這段程式碼。在下次執行時，它會自動將 `./index.py` 壓縮成 ZIP，並計算其 Hash，發現與 AWS 上現有的 Hash 不同，就會執行打包與上傳的更新行為。

### 4. 執行部署驗證（Deploy）
最後透過以下指令執行部署更新：
```bash
pulumi up --yes
```

### 5. 從 state 中移除資源
執行指令：
```bash
pulumi stack --show-urns #取得Lambda的URN
pulumi state delete <Lambda的URN> --yes #移除Lambda的URN  
```

### 6. 透過 Pulumi 重構 Lambda
1. 手動刪除 AWS Console 上的 Lambda
2. 執行 `pulumi preview` 預覽變更
3. 執行 `pulumi up` 執行變更

### 7. 刪除 Stack
執行指令：
```bash
pulumi destroy --stack dev --yes
pulumi stack rm --stack dev
```

---