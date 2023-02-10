films_msg = """*🎪 Мировые шедевры литературы и кинематографа.*\n
В вашем распоряжении тысячи трейлеров и тизеров книг об удивительных историях самых разных людей о том,
 как они идут свой путь к заветным мечтам и добиваются амбицизных целей."""

films = []
trailers = []
message = ''
f = open('client/media/messages_for_kb/films_messages', 'r')
i = 0
for line in f:
    if '🎥' in line and i>0:
        films.append(message)
        message = line.replace('1.', "")
        message = message.replace('**', "*")

    elif 'Трейлер:' in line:
        continue

    elif '[' in line:
        trailers.append(line[1:line.find(']')])
    else:

        message += line.replace('1.', "")
        message = message.replace("\n\n\n", "\n")

    i +=1


