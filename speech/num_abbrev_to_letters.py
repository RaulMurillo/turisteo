from num2words import num2words
import re, string

# numero_romano debe ser un String
def roman_to_arabic(number_roman):
    # Resultado de la transformacion
    result = 0

    # Usamos un diccionario, ya que se adapta al concepto
    # de que a cada letra le corresponde un valor
    values = {
        'M' : 1000,
        'D' : 500,
        'C' : 100,
        'L' : 50,
        'X' : 10,
        'V' : 5,
        'I' : 1
    }
	

    if len(number_roman) > 0:
        # Con esto, siempre sumamos el primer numero
        value_before = 0

    # Por cada letra en el numero romano (string)
    for letter in number_roman:

        # Si la letra se encuentra en el diccionario
        if letter in values:
            # Obtenemos su valor
            value_act = values[letter]
        else:
            # Si no, la letra es invalida
            print('Valor invalido:' + letter)
            return 'NaN' # NaN: Not A Number

        # Si el valor anterior es mayor o igual que el
        # valor actual, se suman
        if value_before >= value_act:
            result += value_act
        # Si no, se restan
        else:
            # Esto equivale a:
            # resultado = (resultado - valor_anterior) + (valor_actual - valor_anterior)
            result += value_act - (2 * value_before)

        # El valor actual pasa a ser el anterior, para analizar
        # la siguiente letra en el numero romano
        value_before = value_act

    # Al terminar, retorna el numero resultante
    return result

def abbrevations(ab):
    values = {
        'km' : 'kilometers',
        'mi' : 'miles',
        'm' : 'meters',
        'BC' : 'before Christ'
    }
	
    return values[ab]
	
	
f = open ('results_en.txt','r', encoding="utf-8")
file = f.read()
list_numbers = []
for element in re.finditer('[0-9]+([.][0-9]+)?', file):
    s = element.start()
    e = element.end()
    if (re.search('[.]', file[s:e]) == None):
        str_to_number = (int) (file[s:e])
    else:
        str_to_number = (float) (file[s:e])

    list_numbers.append(str_to_number)
list_numbers.sort(reverse=True)
file_n = file
for i in list_numbers:
    i = (str) (i)
    number = num2words(i)
    file_n = file_n.replace(i, number)
	
list_numbers = []
for element in re.finditer('[a-z|A-Z]*[\s][M|D|C|L|X|V|I]+[\s | .]', file_n):
    s = element.start()
    e = element.end()
    expression = file_n[s:e]
    print(expression)
    if (re.search('^[year|century]', expression) == None):
        for iter in re.finditer('[M|D|C|L|X|V|I]+[\s | .]', expression):
            s1 = iter.start()
            e1 = iter.end()
            list_numbers.append(expression[s1:e1-1] + ' o')
    else:
        for iter in re.finditer('[M|D|C|L|X|V|I]+[\s | .]', expression):
            s1 = iter.start()
            e1 = iter.end()
            list_numbers.append(expression[s1:e1-1] + ' c')
	   
file_nn = file_n
list_numbers.sort(reverse=True)
for i in list_numbers:
    i = i.split()
    number = roman_to_arabic(i[0])
    number = (str) (number)
    if i[1] == 'o':
	    number = num2words(number, ordinal=True)
    else:
        number = num2words(number)
    file_nn = file_nn.replace(i[0] + ' ', number + ' ')
    file_nn = file_nn.replace(i[0] + '.', number + '.')


list_numbers = []
for element in re.finditer('[\s][km|mi|m|BC]+[\s|.|)]', file):
    s = element.start()
    e = element.end()
    list_numbers.append(file[s+1:e-1])
list_numbers.sort(reverse=True)
file_def = file_nn
for i in list_numbers:
    abbrevation = abbrevations(i)
    file_def = file_def.replace(i, abbrevation)

f.close()
file_w = open('text_numbers_letters.txt','w', encoding="utf-8")
file_w.write(file_def)
file_w.close()
print("It has been successfully saved in the file: \"text_numbers_letters.txt\"")