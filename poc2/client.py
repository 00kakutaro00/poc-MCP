from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.chat_models import ChatOpenAI  # LangChainのOpenAIチャットモデル
from langchain.agents import initialize_agent, AgentType
import os

CURRENT_DIR = os.getcwd()
# OpenAIのGPT-3.5をチャットモデルとして使用（モデル名は必要に応じて変更可能）
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# MCPサーバーへの接続パラメータを設定（先ほどのmath_server.pyを指定）
server_params = StdioServerParameters(
    command="python",
    args=[f"{CURRENT_DIR}/employees_server.py"]  # math_server.pyのフルパスに置き換えてください
)


# 非同期でエージェントを実行する関数を定義
import asyncio
async def run_agent(input_txt):
    # MCPサーバーにstdio経由で接続（サーバーからの読み取りストリームと書き込みストリームを取得）
    async with stdio_client(server_params) as (read, write):
        # クライアントセッション開始
        async with ClientSession(read, write) as session:
            # セッション初期化（MCP接続のハンドシェイク）
            await session.initialize()
            # 利用可能なツール一覧を取得（MCPサーバー上の全ツールをLangChain用にロード）
            tools = await load_mcp_tools(session)

            # ツール付きでエージェントを作成（React方式のエージェントを利用）
            agent = initialize_agent(
                    tools, llm,
                    agent=AgentType.OPENAI_FUNCTIONS,
                    verbose=True
                    )
            # エージェントに質問を投げかけて実行（例: 計算式を与える）
            result = await agent.ainvoke(input_txt)  # ← 非同期実行でOK！
            return result

# 非同期関数を実行して結果を表示
if __name__ == "__main__":

    # DB読み込みを実施
    output = asyncio.run(run_agent("Bobはどこの部署にいる？"))
    print("####")
    print(output)
    print("####")

    # DB読み込み、ファイル作成の２つのtoolsを実施
    output = asyncio.run(run_agent("Bobはどこの部署にいる？結果をbob.txtに保存して。"))
    print("####")
    print(output)
    print("####")

    # DBに書き込み操作
    output = asyncio.run(run_agent("TaroをResearch部署に追加して。"))
    print("####")
    print(output)
    print("####")

    # MariはDBに存在しない。
    output = asyncio.run(run_agent("Mariはどこの部署にいる？結果をMari.txtに保存して。"))
    print("####")
    print(output)
    print("####")

    # LLMでは答えられないが正しい。
    output = asyncio.run(run_agent("今日の天気は？"))
    print("####")
    print(output)
    print("####")

    # toolsがなくてもLLMのみで動く
    output = asyncio.run(run_agent("1+1は？"))
    print("####")
    print(output)
    print("####")

    # 正しく動かないので、修正が必要。
    txt = "Marketing部門の社員の名前を一覧を出力してください。"
    output = asyncio.run(run_agent(txt))
    print("####")
    print(output)
    print("####")

