"""Build the static legal pages from the shared, bilingual document source."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "legal/documents.json").read_text())


def filename(kind, language):
    return f"{kind}{'-en' if language == 'en' else ''}.html"


for language in ("ru", "en"):
    for kind in ("privacy", "terms"):
        document = DATA[language][kind]
        other_language = "en" if language == "ru" else "ru"
        other_kind = "terms" if kind == "privacy" else "privacy"
        sections = []
        for index, section in enumerate(document["sections"], 1):
            paragraphs = "".join(f"<p>{escape(p)}</p>" for p in section["body"].split("\n\n"))
            sections.append(f'<section id="section-{index}"><h2>{escape(section["title"])}</h2>{paragraphs}</section>')
        contents = "".join(
            f'<a href="#section-{i}">{escape(section["title"])}</a>'
            for i, section in enumerate(document["sections"], 1)
        )
        updated = "Последнее обновление: 6 сентября 2026" if language == "ru" else "Last updated: September 6, 2026"
        skip = "Перейти к тексту" if language == "ru" else "Skip to content"
        providers = (
            '<a href="https://supabase.com/privacy">Supabase Privacy</a>'
            '<a href="https://www.apple.com/legal/privacy/">Apple Privacy</a>'
            '<a href="https://www.microsoft.com/privacy/privacystatement">Microsoft Privacy</a>'
            '<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy</a>'
        ) if kind == "privacy" else '<a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Apple Standard EULA</a>'
        html = f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(document['title'])} | Walk With Me</title>
  <meta name="description" content="{escape(document['intro'], quote=True)}">
  <link rel="stylesheet" href="legal/style.css">
  <link rel="icon" href="assets/app-icon.jpg">
  <link rel="alternate" hreflang="{other_language}" href="{filename(kind, other_language)}">
</head>
<body>
<a class="skip" href="#document">{skip}</a>
<header>
  <a class="brand" href="index.html"><img src="assets/app-icon.jpg" width="44" height="44" alt="">Walk With Me</a>
  <nav aria-label="{'Документы и язык' if language == 'ru' else 'Documents and language'}">
    <a href="{filename(other_kind, language)}">{escape(DATA[language][other_kind]['title'])}</a>
    <a href="{filename(kind, other_language)}" lang="{other_language}">{'English' if language == 'ru' else 'Русский'}</a>
  </nav>
</header>
<main id="document">
  <div class="intro"><p class="eyebrow">Walk With Me: Daily Walks</p>
  <h1>{escape(document['title'])}</h1><p class="date">{updated}</p>
  <p>{escape(document['intro'])}</p></div>
  <details class="contents"><summary>{'Содержание' if language == 'ru' else 'Contents'}</summary>{contents}</details>
  {''.join(sections)}
  <aside class="resources">{providers}</aside>
</main>
<footer><span>Diana Kuchaeva · Walk With Me</span><a href="mailto:{DATA['contact']}">{DATA['contact']}</a></footer>
</body></html>
'''
        (ROOT / filename(kind, language)).write_text(html)

(ROOT / "index.html").write_text('''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Walk With Me — Documents & Support</title><link rel="stylesheet" href="legal/style.css">
<link rel="icon" href="assets/app-icon.jpg"></head><body>
<header><a class="brand" href="index.html"><img src="assets/app-icon.jpg" width="44" height="44" alt="">Walk With Me</a></header>
<main><div class="intro"><p class="eyebrow">Walk With Me: Daily Walks</p><h1>Документы и поддержка</h1>
<p lang="en">Documents & support</p></div>
<section><h2>Конфиденциальность / Privacy</h2><p><a href="privacy.html">Политика конфиденциальности</a> · <a href="privacy-en.html" lang="en">Privacy Policy</a></p></section>
<section><h2>Условия / Terms</h2><p><a href="terms.html">Условия использования</a> · <a href="terms-en.html" lang="en">Terms of Use</a></p></section>
<section><h2>Связаться / Contact</h2><p>Поддержка, вопросы о данных и удаление аккаунта:</p>
<p lang="en">Support, privacy requests and account deletion:</p>
<p><a href="mailto:dianakuchaeva@hotmail.com">dianakuchaeva@hotmail.com</a></p>
<p>Не отправляйте пароль или коды входа. / Do not send passwords or sign-in codes.</p></section></main>
<footer>Diana Kuchaeva · Walk With Me</footer></body></html>
''')
