books = []

message = ''
f = open('client/media/messages_for_kb/book_messages', 'r')
i = 0
for line in f:
    if '📗' in line and i>0:
        books.append(message)
        message = line.replace('1.', "")
        message = message.replace('**', "*")
    else:
        message += line.replace('1.', "")
    i +=1