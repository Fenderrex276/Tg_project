principles_of_success_msg = ("*🍎 Принципы успеха*\n\n"
                             "Читайте принципы успеха великих "
                             "людей о том, как сохранять мотивацию и добиваться любых целей. Отправляй"
                             " мемы себе в избранное ❤️ делись с друзьями и получай поддержку \n\n"
                             "Рубрика постоянно обновляется.")

tips = []

message = ''
f = open('client/media/messages_for_kb/success_messages', 'r')
i = 0
for line in f:
    if '🎓' in line and i > 0:
        tips.append(message)
        message = line.replace('1.', "")
        message = message.replace('1. **', "*")
    else:
        message += line
    i += 1
