from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import random

MAX_LEN = 140
ALLOWED_KEYWORDS = ("Uber Eats", "出前館", "Wolt", "menu")


@dataclass(frozen=True)
class PostTemplate:
    category: str
    templates: tuple[str, ...]


POST_TEMPLATES: tuple[PostTemplate, ...] = (
    PostTemplate(
        category="稼働",
        templates=(
            "【稼働】雨上がりでUber Eatsの需要が上昇。安全第一で短距離を積み、ピーク前にオンライン準備します。",
            "【稼働】ランチ帯は出前館の鳴りが早め。駅前を中心に待機し、回転重視で効率よく配達します。",
            "【稼働】夜ピークはWoltとUber Eatsを見比べ、単価と距離のバランスが良い案件から丁寧に対応します。",
        ),
    ),
    PostTemplate(
        category="配達員",
        templates=(
            "【配達員】受け取り時の一言と笑顔で店舗連携がスムーズに。Uber Eatsでも基本対応の積み重ねが評価につながる。",
            "【配達員】置き配写真は明るく角度を統一。出前館の完了報告も正確に行うとトラブル予防に効果的。",
            "【配達員】焦る時間帯ほど安全運転を徹底。早さだけでなく、丁寧さが次の注文機会を増やしてくれる。",
        ),
    ),
    PostTemplate(
        category="注文",
        templates=(
            "【注文】今日はUber Eatsで温かい丼を注文。到着予定が見やすく、忙しい日でも食事の段取りが組みやすい。",
            "【注文】出前館で家族分をまとめて注文。クーポン活用でお得に、受け取り時間も合わせやすくて便利。",
            "【注文】雨の日はmenuの即配が助かる。外出せずに好きな店の味を楽しめるのがフードデリバリーの強み。",
        ),
    ),
    PostTemplate(
        category="予測",
        templates=(
            "【予測】今週は気温上昇で冷たいメニュー需要が増加見込み。Uber Eatsは夕方以降の注文が伸びそう。",
            "【予測】週末の出前館は家族注文が増える傾向。昼前の仕込み次第で配達効率に差が出そうです。",
            "【予測】雨予報の前後はWoltの即時注文が集中しやすい想定。待機場所を早めに調整して備えたい。",
        ),
    ),
)


def _is_food_delivery_related(text: str) -> bool:
    return any(keyword in text for keyword in ALLOWED_KEYWORDS)


def _normalize_length(text: str, limit: int = MAX_LEN) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def generate_posts(seed: int | None = None) -> list[str]:
    rng = random.Random(seed)
    posts: list[str] = []

    for template_group in POST_TEMPLATES:
        post = rng.choice(template_group.templates)
        post = _normalize_length(post)
        if not _is_food_delivery_related(post):
            raise ValueError(f"フードデリバリー関連外の投稿が検出されました: {post}")
        posts.append(post)

    return posts


def save_posts(posts: list[str], output_dir: str = ".") -> Path:
    today = datetime.now().strftime("%Y%m%d")
    output_path = Path(output_dir) / f"posts_{today}.txt"

    lines = [f"{idx}. {post}" for idx, post in enumerate(posts, start=1)]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
