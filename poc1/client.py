from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.chat_models import ChatOpenAI  # LangChainのOpenAIチャットモデル
from langchain.agents import initialize_agent, AgentType

# OpenAIのGPT-3.5をチャットモデルとして使用（モデル名は必要に応じて変更可能）
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# MCPサーバーへの接続パラメータを設定（先ほどのmath_server.pyを指定）
server_params = StdioServerParameters(
    command="python",
    args=["/Users/kakusakitarou/work/llm-activity/poc-mcp/poc1/math_server.py"]  # math_server.pyのフルパスに置き換えてください
)

# 非同期でエージェントを実行する関数を定義
import asyncio
async def run_agent():
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
            result = await agent.ainvoke("What's (3 + 5) x 12?")  # ← 非同期実行でOK！
            return result

# 非同期関数を実行して結果を表示
if __name__ == "__main__":
    output = asyncio.run(run_agent())
    print("####")
    print(output)
    print("####")