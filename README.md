# poc-MCP
MCPのpocコード

## 環境構築
- condaでPython環境を準備
conda create --name mcp python=3.11 -y

- モジュールのインストール
pip install numpy pandas matploblib jupyterlab
pip install langchain langchain-mcp-adapters mcp
pip install langchain-community

- open-aiの環境変数をexport
export OPENAI_API_KEY="sk-proj-*****************"

## poc用のコード
- poc1 : 足し算と掛け算
- poc2 : sqlite3でDBを操作

### poc1 : 足し算と掛け算
- `source activate mcp` : python環境をactivete
- `cd poc1`
- 別ターミナルで　`python math_server.py` を実行する
- `python client.py` を実行しMCPクライアントが動くことを確認

### poc2 : DBの操作
- `source activate mcp` : python環境をactivete
- `cd poc2`
- `python mk_employees.py`を実行しemployees.dbが出来たことを確認
- 別ターミナルで　`python employee_server.py` を実行
- `python client.py` を実行しMCPクライアントが動くことを確認


