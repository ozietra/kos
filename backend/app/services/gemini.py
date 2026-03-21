"""
Gemini 2.5 Flash ile NACE kodu önerisi
"""
import json
import re
from google import genai
from app.config import settings

_client: genai.Client | None = None


def get_gemini_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


NACE_SUGGEST_PROMPT = """
Kullanıcının sektör açıklamasına en uygun NACE Rev.2 kodunu bul.
Yanıt SADECE geçerli bir JSON objesi olmalı, başka hiçbir şey içermemeli:
{{
  "nace_code": "XX.XX",
  "nace_description": "Türkçe açıklama",
  "is_kosgeb_eligible": true veya false,
  "confidence": "high" veya "medium" veya "low",
  "alternative_codes": [
    {{"code": "XX.XX", "description": "Türkçe açıklama"}},
    {{"code": "XX.XX", "description": "Türkçe açıklama"}}
  ]
}}

KOSGEB uygun sektörler için referans:
- C (10-33): İmalat — UYGUN
- 61: Telekomünikasyon — UYGUN
- 62: Bilgisayar programlama ve danışmanlık — UYGUN
- 63: Bilişim altyapısı ve veri işleme — UYGUN
- 72: Bilimsel araştırma ve geliştirme — UYGUN
- F (41-43): İnşaat — UYGUN DEĞİL (genel kural)
- G (45-47): Toptan/Perakende — UYGUN DEĞİL
- I (55-56): Konaklama/Restoran — UYGUN DEĞİL

Kullanıcının açıklaması: {description}
"""


async def suggest_nace(description: str) -> dict:
    """Gemini 2.5 Flash ile NACE kodu öner"""
    client = get_gemini_client()
    prompt = NACE_SUGGEST_PROMPT.format(description=description)

    response = await client.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    raw = response.text.strip()

    # JSON çıkar (markdown code block varsa temizle)
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        # Fallback: JSON parse edilemezse minimal yanıt
        data = {
            "nace_code": "62.01",
            "nace_description": "Bilgisayar programlama faaliyetleri",
            "is_kosgeb_eligible": True,
            "confidence": "low",
            "alternative_codes": [],
        }

    return data


async def generate_text(prompt: str) -> str:
    """Genel metin üretimi için Gemini çağrısı"""
    client = get_gemini_client()
    response = await client.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )
    return response.text
