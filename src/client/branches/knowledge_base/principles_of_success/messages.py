principles_of_success_msg = ("*🍎 Принципы успеха*\n\n"
                             "Читайте принципы успеха великих "
                             "людей о том, как сохранять мотивацию и добиваться любых целей. Отправляй"
                             " мемы себе в избранное ❤️ делись с друзьями и получай поддержку \n\n"
                             "Рубрика постоянно обновляется.\n"
                             "Чтобы получать мемы мотивации раз "
                             "в день сразу послерепорта, нажми 🔔 "
                             "и подпишись на обновления")

tips = []

message = ''
f = open('client/media/messages_for_kb/success_messages', 'r')
i = 0
for line in f:
    if '📗' in line and i > 0:
        tips.append(message)
        message = line.replace('1.', "")
        message = message.replace('**', "*")
    else:
        message += line.replace('1.', "")
    i += 1
