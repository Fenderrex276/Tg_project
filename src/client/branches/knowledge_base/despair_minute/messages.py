tips = []

start_msg = ("""*🙃 Открой это, когда станет трудно.*\n\n
Читай и слушай ободряющие советы от живых пользователей и смотри легендарные лекции с международной конференции TED о продуктивности, прокрастинации, мотивации, успехах и поражениях людей, кто падает, но встаёт и продолжает идти.""")

message = ''
f = open('client/media/messages_for_kb/dp_messages', 'r')
i = 0
for line in f:
    if '☝️' in line and i>0:
        tips.append(message)
        message = line.replace('1.', "")
        message = message.replace('**', "*")
    else:
        message += line
    i +=1