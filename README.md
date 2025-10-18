# llm-reviewer

PubMedから文献を検索してJSON形式でダウンロードするツールです。

## インストール

```bash
uv sync
```

## 使い方

uv環境では以下のように実行します:

```bash
# uv run で実行
uv run python main.py "machine learning AND medicine"

# または仮想環境を有効化してから実行
source .venv/bin/activate  # macOS/Linux
python main.py "machine learning AND medicine"
```

オプション付き:

```bash
# 最大100件取得（デフォルト）
uv run python main.py "COVID-19 treatment" -n 100

# 出力先ディレクトリを指定
uv run python main.py "cancer immunotherapy" -o ./data

# 両方のオプションを使用
uv run python main.py "deep learning healthcare" -n 50 -o ./output
```

## オプション

- `query`: 検索クエリ（必須）
  - PubMed検索構文をサポート（AND, OR, NOT など）
- `-n, --max-results`: 最大取得件数（デフォルト: 100）
- `-o, --output-dir`: 出力ディレクトリ（デフォルト: カレントディレクトリ）

## 出力形式

JSONファイルは以下の形式で保存されます:
- ファイル名: `pubmed_{検索クエリ}_{タイムスタンプ}.json`
- 各文献には以下の情報が含まれます:
  - `pubmed_id`: PubMed ID
  - `title`: タイトル
  - `abstract`: 要旨
  - `keywords`: キーワード
  - `journal`: ジャーナル名
  - `publication_date`: 出版日
  - `authors`: 著者リスト
  - `doi`: DOI
  - `conclusions`: 結論
  - `methods`: 方法
  - `results`: 結果
  - `copyrights`: 著作権情報

## 例

```bash
# AI医療に関する文献を50件取得
uv run python main.py "artificial intelligence AND healthcare" -n 50

# 2024年以降のCOVID-19研究を取得
uv run python main.py "COVID-19 AND 2024[PDAT]" -n 100
```
