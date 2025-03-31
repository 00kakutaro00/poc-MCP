from mcp.server.fastmcp import FastMCP
import sqlite3

mcp = FastMCP("EmployeeSearch")

DB_PATH = "employees.db"

@mcp.tool()
def find_department_by_name(name: str) -> str:
    """
    指定した名前の従業員が所属する部署を返します。
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT department FROM employees WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()

    if row:
        return f"{name} さんの部署は {row[0]} です。"
    else:
        return f"{name} さんはデータベースに見つかりませんでした。"

@mcp.tool()
def save_file(file_name: str, content: str) -> str:
    """
    指定されたファイル(file_name)に、contentの文字列を追記します。
    存在しない場合はファイルを新規作成します。

    例: save_file(file_name="output.txt", content="書き込みたいテキスト")
    """
    # セキュリティ対策として、許容するディレクトリを限定するなど本来は推奨
    # ここでは簡単のため無制限に書き込みます。
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"{file_name} に書き込みました。"
    except Exception as e:
        return f"ファイル書き込みエラー: {e}"


@mcp.tool()
def add_employee(name: str, department: str) -> str:
    """
    従業員テーブルに新しいレコードを追加します。
    例: add_employee(name="山田太郎", department="営業")
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        # employeesテーブルに (name, department) をINSERT
        cur.execute("INSERT INTO employees (name, department) VALUES (?, ?)", (name, department))
        new_id = cur.lastrowid  # 挿入した行のIDを取得
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return f"データ追加時にエラーが発生しました: {e}"
    conn.close()
    return f"新しい従業員 (ID={new_id}, 名前={name}, 部署={department}) を追加しました。"



# データベースのスキーマを文字列として定義
SCHEMA_DESCRIPTION = """
このデータベースには1つのテーブルがあります：

employees(id INTEGER, name TEXT, department TEXT)

- id: 社員ID（整数）
- name: 社員の名前（文字列）
- department: 所属部署名（文字列）
"""
@mcp.tool()
def query_employees(natural_language_query: str) -> str:
    """
    従業員データベースに対して自然言語のクエリを受け取り、対応するSQLを生成し、結果を返します。
    """
    import openai

    # OpenAIのAPIキーは環境変数または別セルで設定してください
    system_prompt = f"""
    以下のデータベーススキーマに基づいて、ユーザーの自然言語の質問に対するSQLクエリを生成してください。
    SQLはSQLite3形式で、複数行に分けず、1行で書いてください。
    
    スキーマ:
    {SCHEMA_DESCRIPTION}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": natural_language_query}
        ]
    )

    sql_query = response["choices"][0]["message"]["content"]

    # SQL実行
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
    except Exception as e:
        return f"SQL実行エラー: {e}"
    finally:
        conn.close()

    if not rows:
        return "結果が見つかりませんでした。"
    
    # 結果を文字列で整形
    return "\n".join(str(row) for row in rows)





if __name__ == "__main__":
    mcp.run(transport="stdio")
