principles_fm_success_msg = """*🎪 Мировые шедевры литературы и кинематографа.*\n\n
В вашем распоряжении тысячи трейлеров и тизеров книг об удивительных историях самых разных людей о том,
 как они идут свой путь к заветным мечтам и добиваются амбицизных целей."""

tips = []

message = ''
f = open('client/media/messages_for_kb/films_messages', 'r')
i = 0
for line in f:
    if '📗' in line and i>0:
        tips.append(message)
        message = line.replace('1.', "")
        message = message.replace('**', "*")
    elif '[' in line:
        pass
    else:
        message += line.replace('1.', "")
    i +=1