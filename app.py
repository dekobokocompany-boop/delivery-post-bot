from __future__ import annotations

from generate_post import generate_posts, save_posts


def main() -> None:
    posts = generate_posts()
    output_path = save_posts(posts)

    print("=== 生成されたX投稿（各140文字以内）===")
    for idx, post in enumerate(posts, start=1):
        print(f"{idx}. {post} ({len(post)}文字)")

    print(f"\n保存先: {output_path}")


if __name__ == "__main__":
    main()
