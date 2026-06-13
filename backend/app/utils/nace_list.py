"""
NACE Rev.2 doğrulama yardımcısı.

AI'nın önerdiği NACE kodunun en azından geçerli bir NACE bölümüne (2 haneli
kısım) ait olup olmadığını kontrol eder. Böylece halüsinasyon kodlar (örn.
"00.00" veya var olmayan bölümler) yakalanır.
"""
import re

# NACE Rev.2 geçerli 2 haneli bölümler (divisions)
VALID_NACE_DIVISIONS: set[str] = {
    "01", "02", "03",                                  # Tarım, ormancılık, balıkçılık
    "05", "06", "07", "08", "09",                      # Madencilik
    *[f"{n:02d}" for n in range(10, 34)],              # 10–33 İmalat
    "35",                                              # Elektrik, gaz
    "36", "37", "38", "39",                            # Su, atık
    "41", "42", "43",                                  # İnşaat
    "45", "46", "47",                                  # Ticaret
    "49", "50", "51", "52", "53",                      # Ulaştırma, depolama
    "55", "56",                                        # Konaklama, yiyecek
    "58", "59", "60", "61", "62", "63",                # Bilgi ve iletişim
    "64", "65", "66",                                  # Finans, sigorta
    "68",                                              # Gayrimenkul
    "69", "70", "71", "72", "73", "74", "75",          # Mesleki, bilimsel, teknik
    "77", "78", "79", "80", "81", "82",                # İdari ve destek hizmetleri
    "84",                                              # Kamu yönetimi
    "85",                                              # Eğitim
    "86", "87", "88",                                  # Sağlık, sosyal hizmet
    "90", "91", "92", "93",                            # Kültür, sanat, eğlence
    "94", "95", "96",                                  # Diğer hizmetler
    "97", "98",                                        # Hane halkı
    "99",                                              # Uluslararası kuruluşlar
}

_NACE_RE = re.compile(r"^\s*(\d{2})(?:\.(\d{1,2}))?\s*$")


def normalize_nace(code: str) -> str | None:
    """'62.1' → '62.01' biçimine normalize eder; geçersizse None."""
    if not code:
        return None
    m = _NACE_RE.match(code)
    if not m:
        return None
    division, sub = m.group(1), m.group(2)
    if division not in VALID_NACE_DIVISIONS:
        return None
    if sub is None:
        return division
    return f"{division}.{int(sub):02d}"


def is_valid_nace(code: str) -> bool:
    return normalize_nace(code) is not None
