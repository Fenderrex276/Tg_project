tips = []

start_msg = ("""*Не сдавайся*\n\n
Читай ободряющие советы и смотрите легендарные лекции с международной конференции TED о продуктивности, прокрастинации, внутренней мотивации, успехах и поражениях""")

message = ''
f = open('client/media/messages_for_kb/dp_messages', 'r')
i = 0
for line in f:
    if '📗' in line and i>0:
        tips.append(message)
        message = line.replace('1.', "")
        message = message.replace('**', "*")
    else:
        message += line.replace('1.', "")
    i +=1