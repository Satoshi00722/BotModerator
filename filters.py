BAD_WORDS = [
    "порно", "porn", "sex", "xxx", "onlyfans", "escort", "эскорт",
    "проститутка", "проституция", "шлюха", "девочки", "массаж",
    "cam", "webcam", "cams", "nude", "nudes", "nsfw",
    "hooker", "brothel", "strip", "striptease",
    "интим", "интим услуги", "sex service", "vip girls",
    "нарк", "drug", "drugs", "weed", "marijuana", "cannabis", "ganja", "hash", "hashish", "hemp",
    "kush", "skunk", "dope", "420", "thc", "cbd",
    "cocaine", "coke", "snow", "crack", "amphetamine", "speed", "meth", "ice",
    "mdma", "ecstasy", "xtc", "molly", "mephedrone", "4-mmc",
    "heroin", "opium", "morphine", "fentanyl", "tramadol",
    "lsd", "acid", "dmt", "ketamine", "shrooms", "psilocybin",
    "spice", "k2", "noids",
    "трава", "марихуана", "конопля", "шишки", "бошка", "ганжа", "гандж",
    "меф", "амф", "фен", "героин", "гашиш", "анаша", "косяк", "индивидуалка","escort service","эскорт услуги",
    "обмен", "обменник", "exchange", "crypto exchange",
    "usdt", "btc", "bitcoin", "ethereum",
    "нал", "кеш", "cash", "без верификации", "no kyc",
    "быстрый обмен", "анонимно",
    "собрать", "предоставлю", "темка",
    "забираешь", "рублей", "выплата"

]

def bad_words_check(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in BAD_WORDS)
