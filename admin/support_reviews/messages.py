start_review_msg = """Сюда поступают новые вопросы пользователей со страниц "Поддержка" и "FAQ":"""


def getQuestions(numQuest, id_dispute, in_game, question):
    msg = f"""Вопрос #{numQuest}\n
Диспут #{id_dispute}
Цель: Брошу курить никотин
В игре: {in_game} дней\n
Вопрос:
{question}"""
    return msg

