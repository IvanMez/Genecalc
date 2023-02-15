import colorama
colorama.init()


def GenesRead(PNum):
    while True:
        GivenInput = input(f'Введите генотип P{PNum}: ').replace(' ','')
        if GivenInput=='':
            pass
        elif not GivenInput.isalpha():
            print('Ошибка ввода! Гены должны быть написаны буквами! \n')
        else:
            flag = 0
            for letter in GivenInput:
                if GivenInput.lower().count(letter.lower())!=2:
                    if flag == 0:
                        print('Ошибка ввода! Все гены должны иметь ровно 2 символа! \n')
                    flag = 1
            if flag == 0:
                return(GivenInput)



def FindGamets(AllGenes, CurrGamet=''):
    if len(AllGenes)>1: #Если осталось рассмотреть больше 1 гена
        if AllGenes[0][0] == AllGenes[0][1]: #Ген гомозиготен, рекурсия (Перебор) одной буквы
            return (FindGamets(AllGenes[1:],CurrGamet+AllGenes[0][0])) 
        else: #Ген гетерозиготен, рекурсия (Перебор) двух букв
            return (FindGamets(AllGenes[1:],CurrGamet+AllGenes[0][0]) + FindGamets(AllGenes[1:],CurrGamet+AllGenes[0][1])) 
    else: #Если осталось рассмотреть последний ген
        if AllGenes[0][0] == AllGenes[0][1]:
            FoundGamets = [CurrGamet + AllGenes[0][0]]
        else:
            FoundGamets = [CurrGamet + AllGenes[0][0]] + [CurrGamet + AllGenes[0][1]]
        return FoundGamets # Развёртка стэка
    


def FindNextGen(Gam1, Gam2):
    F = []
    for Gameta1 in Gam1:
        for Gameta2 in Gam2:
                    Gene = ''
                    for Gen in range(0,len(Gameta1)):
                        if Gameta1[Gen].isupper() and Gameta2[Gen].islower():
                            Gene += Gameta1[Gen]+Gameta2[Gen]
                        else:
                            Gene += Gameta2[Gen]+Gameta1[Gen]
                    F += [Gene]
    return F



def main():
    P1 = 'Test'
    P2 = 'TS'
    GoodAnswer = 0
    while GoodAnswer==0:
        P1 = GenesRead(1)
        P2 = GenesRead(2)
        if len(P1) != len(P2):
            print('Ошибка ввода! Вводимое количество генов должно быть одинаковым у обоих родителей! \n')
        else:
            flag = 0
            for i in P1:
                if not ((i.lower() in P2) or (i.upper() in P2)):
                    flag = 1
            if flag == 1:
                print('Ошибка ввода! Гены должны быть аллельны! \n')
            else:
                flag = 0
                for i in range(0,len(P1)):
                    if P1[i].lower() != P2[i].lower():
                        flag = 1
                if flag == 1:
                    print('Ошибка ввода! Гены должны быть введены в одинаковом порядке! \n')
                else:
                    GoodAnswer = 1
    
    USING_FEN = False

    temp = input('Использовать фенотипы? (Оставьте пустым для отмены): ').strip()
    if len(temp)>0:
        USING_FEN = True
        UsedGenes = sorted(list(set(P1+P2)), key = lambda x: ord(x)*10+(320 if x.isupper() else 1))
        print()


        Dict = {}
        for Gen in UsedGenes:
            print('') #Считка гомозиготных признаков
            Fen = ''
            while len(Fen) == 0:
                Fen = input(f'\033[FВведите признак гена {Gen}: ').strip()
            Dict[Gen*2] = Fen


            if Gen.islower() and Gen.upper() in UsedGenes: #Считка гетерозиготных признаков (если есть, иначе присвоить доминантн.)
                Fen = input(f'Введите признак гена {Gen.upper()+Gen} (Оставьте пустым для доминантного признака): ').strip()
                if len(Fen) == 0:
                    Dict[Gen.upper()+Gen] = Dict[Gen.upper()*2]
                else:
                    Dict[Gen.upper()+Gen] = Fen
    
    print()



    Gen1 = [P1[i:i+2] for i in range(0, len(P1), 2)] # Форматирование генов в нужный вид
    Gen2 = [P2[i:i+2] for i in range(0, len(P2), 2)] # Т.е. разбить гены из строки 'AaBb' в строки ['Aa','Bb']
    
    
    Gam1 = FindGamets(Gen1) # Рассчёты полученных данных
    Gam2 = FindGamets(Gen2)
    F1 = FindNextGen(Gam1,Gam2)





    print(f'P: {P1} x {P2}') # Вывод родителей

    print('G: ',end='') # Вывод гамет каждого из родителей
    for G in Gam1:
        print(G,end=' ')
    print('  x  ',end=' ')
    for G in Gam2:
        print(G,end=' ')
    print()


    print('F1:',end=' ') # Вывод генов
    if USING_FEN: # С фенотипом
        for F in F1:
            print(f'{F}-',end='')
            for Gen in [F[i*2]+F[i*2+1] for i in range(len(F)//2)]:
                print(Dict[Gen],end=',')
            print('\b   ',end = '')
        print('\n')
    else: # Без фенотипа
        for F in F1:
            print(F, end=' ')
        print('\n')


    filters = ['']
    while len(filters)>0:
        filter = input('Введите фильтр (или оставьте пустым для завершения):').replace(' ','').replace(',','')
        filters = []

        if len(filter)>0 and USING_FEN: # Перевод фенотипов в фильтре в генотипы для фильтра
            flag = 0
            for Fen in Dict.values():
                if Fen in filter:
                    filter = filter.replace(Fen,'')
                    TempFilter = list(Dict.keys())[list(Dict.values()).index(Fen)] # Добавить в фильтр первый попавшийся ген с таким значением
                    if list(Dict.values()).count(Fen)>1: # Полное доминирование - добавить в фильтр доминантную ЧАСТЬ. Иначе оставить как есть
                        TempFilter = TempFilter[0]
                    filters += [TempFilter]
        

        while len(filter)>0: #Разбив строки фильтра на отдельные фильтры
            if len(filter)>1 and (filter[0].lower() == filter[1].lower()): #Если фильтр из двух букв
                filters += [filter[0:2]]
                filter = filter[2:]
            else: #Если фильтр из одной
                filters += [filter[0]]
                filter = filter[1:]
        
        if len(filters)>0: #Применение фильтров
            FilteredF = []
            for Gene in F1:
                flag = 0
                for filt in filters:
                    if not (filt in Gene):
                        flag = 1
                if flag == 0:
                    FilteredF += [Gene]
            
            print('Подошли следующие генотипы: ',end='') # Вывод генов
            if USING_FEN: # С фенотипом
                for F in FilteredF:
                    print(f'{F}-',end='')
                    for Gen in [F[i*2]+F[i*2+1] for i in range(len(F)//2)]:
                        print(Dict[Gen],end=',')
                    print('\b   ',end = '')
            else: # Без фенотипа
                for F in FilteredF:
                    print(F, end=' ')

            
            
            found = len(FilteredF)
            allpossible = len(Gam1)*len(Gam2)
            chance = round(found/allpossible*100, 5)
            print(f'\nЭто {found}/{allpossible} возможных генотипов (Шанс ~{chance}%)\n')




if __name__=='__main__':
    while True:
        main()
        print('Перезапуск программы! \n')