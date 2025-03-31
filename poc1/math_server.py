from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数の足し算"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """2つの数の掛け算"""
    return a * b

if __name__ == "__main__":
    # スタンダード入出力経由でサーバーを起動
    mcp.run(transport="stdio")


