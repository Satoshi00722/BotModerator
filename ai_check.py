from openai import OpenAI
from config import OPENAI_API_KEY

def ai_check(text: str) -> bool:
    if not OPENAI_API_KEY:
        return True  # ❗ если ключа нет — ВСЁ РАЗРЕШЕНО

    client = OpenAI(api_key=OPENAI_API_KEY)

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты модератор рекламы. "
                    "Запрещай ТОЛЬКО: наркотики, порно, проституцию, колл-центры, быстрые деньги. "
                    "Если нарушений нет — ответь строго словом OK"
                )
            },
            {"role": "user", "content": text}
        ]
    )

    return r.choices[0].message.content.strip() == "OK"
