
# Функция для создания листа из переменных, предварительно создай пустой объект list_data
def make_list(*args,**kwargs):
    for i in range(len(args)):
        kwargs.append(args[i])

