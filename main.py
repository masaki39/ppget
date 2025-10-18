import json
import argparse
from datetime import datetime
from pathlib import Path
from pymed_paperscraper import PubMed


def search_pubmed(query: str, max_results: int = 100) -> list[dict]:
    """
    PubMedから文献を検索してデータを取得する

    Args:
        query: 検索クエリ
        max_results: 最大取得件数

    Returns:
        文献データのリスト
    """
    pubmed = PubMed(tool="llm-reviewer", email="masa21gifus@gmail.com")

    results = pubmed.query(query, max_results=max_results)

    articles = []
    for article in results:
        article_data = {
            "pubmed_id": article.pubmed_id,
            "title": article.title,
            "abstract": article.abstract,
            "keywords": article.keywords,
            "journal": article.journal,
            "publication_date": str(article.publication_date) if article.publication_date else None,
            "authors": [
                {"firstname": author.get("firstname"), "lastname": author.get("lastname")}
                for author in (article.authors or [])
            ],
            "doi": article.doi,
            "conclusions": article.conclusions,
            "methods": article.methods,
            "results": article.results,
            "copyrights": article.copyrights,
        }
        articles.append(article_data)

    return articles


def save_to_json(data: list[dict], query: str, output_dir: Path = Path(".")):
    """
    文献データをJSON形式で保存する

    Args:
        data: 文献データのリスト
        query: 検索クエリ（ファイル名に使用）
        output_dir: 出力ディレクトリ
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # クエリからファイル名に使えない文字を除去
    safe_query = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in query)
    filename = f"pubmed_{safe_query}_{timestamp}.json"

    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ {len(data)} articles saved to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="PubMedから文献を検索してJSON形式でダウンロードする"
    )
    parser.add_argument(
        "query",
        type=str,
        help="検索クエリ（例: 'machine learning AND medicine'）"
    )
    parser.add_argument(
        "-n", "--max-results",
        type=int,
        default=100,
        help="最大取得件数（デフォルト: 100）"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("."),
        help="出力ディレクトリ（デフォルト: カレントディレクトリ）"
    )

    args = parser.parse_args()

    print(f"Searching PubMed for: '{args.query}'")
    print(f"Max results: {args.max_results}")

    try:
        articles = search_pubmed(args.query, args.max_results)
        print(f"Found {len(articles)} articles")

        if articles:
            output_path = save_to_json(articles, args.query, args.output_dir)
            print(f"Successfully downloaded articles to {output_path}")
        else:
            print("No articles found for the given query")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
