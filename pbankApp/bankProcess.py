#--- pbankApp ---#
class bankProcess:
    def __init__(self) -> None:
        pass
    
    def start():
        bankProcess.hello()

    def hello():
        print("YAPACAĞIN İŞLEMİ SEÇ")
        select = input("1-Hesap Oluştur\n2-Giriş Yap\n")
        if select == "1":
            bankProcess.createAccount()
        elif select == "2":
            bankProcess.loginAccount()
        else:
            print("Yanlış seçim yaptın tekrar dene.")
            bankProcess.hello()

    def createAccount():
        while True:
            try:
                account_id = input("Kullanıcı adı giriniz: ")
                bankProcess.check_account_id(account_id)
                password = input("Parola giriniz: ")
                bankProcess.check_except(password)
                balance = input("Kullanılacak bakiyeyi giriniz: ")
                with open("account_information.txt","a",encoding="utf-8") as file:
                    file.write(account_id+':'+password+':'+balance+'\n')
                    bankProcess.accountInformation(account_id,password,balance)
                    break
            except Exception as ex:
                print(ex)
                print("Tekrar dene..")

    def check_account_id(account_id):
        control = True
        with open("account_information.txt","r",encoding="utf-8") as file:
            for line in file:
                linelist = line.split(':')
                if linelist[0] == account_id:
                    print(f"{account_id} Bu kullanıcı adı mevcut.")
                    control = False
                    break
                else:
                    pass
            if control:
                bankProcess.check_except(account_id)
            else:
                print("Tekrar Dene..")
                bankProcess.createAccount()
    
    def check_except(check):
        import re 
        if len(check)<7:
            raise Exception(f"{check} en az 7 karakter olmalıdır.")
        elif not re.search("[a-z]",check):
            raise Exception(f"{check} küçük harf içermelidir.")
        elif not re.search("[A-Z]",check):
            raise Exception(f"{check} büyük harf içermelidir.")
        elif not re.search("[0-9]",check):
            raise Exception(f"{check} rakam içermelidir.")
        elif re.search("[_@$]",check):
            raise Exception(f"{check} alfa numerik karakter içermemelidir.")
        elif re.search("\s",check):
            raise Exception(f"{check} boşluk içermemelidir.")
        else:
            print(f"Geçerli {check}")
    
    def accountInformation(account_id,password,balance):
        print(f"Tebrikler\nHesap bilgilerin:\nKullanıcı Adı:{account_id} Şifre:{password} Bakiye:{balance}")

    def loginAccount():
        account_id = input("Kullanıcı adı giriniz: ")
        password = input("Parola giriniz: ")
        bankProcess.loginControl(account_id,password)
    
    def loginControl(account_id,password):
        control = False
        with open("account_information.txt","r",encoding="utf-8") as file:
            for line in file:
                linelist = line.split(':')
                if linelist[0] == account_id:
                    print(f"{account_id} Kullanıcı adını doğru girdiniz..")
                    if linelist[1] == password:
                        print(f"{password} Şifreyi doğru girdiniz..")
                        control = True
                        break
                    else:
                        control = False
                        pass
                else:
                    control = False
                    pass
        if control:
            bankProcess.accountInformation(account_id,password,linelist[2])
            bankProcess.bankOptions(account_id,password,linelist[2])
        else:
            print("Yanlış girdiniz tekrar deneyin.")
            bankProcess.loginAccount()
        
    def bankOptions(account_id,password,balance):
        select = input("Seçenekler\n1-Para Çek\n2-Para Yatır\n")
        if select == "1":
            bankProcess.moneyWithdraw(account_id,password,balance)
        elif select =="2":
            bankProcess.moneyDeposit(account_id,password,balance)
        else:
            print("Yanlış seçim yaptın tekrar dene..")
            bankProcess.bankOptions(account_id,password,balance)

    def moneyDeposit(account_id,password,balance):
        money = input("Yatıracağınız parayı giriniz\n")
        select = input("Parayı yatırmak istiyormusunuz?(e/h)\n")
        if select == "e" or select == "E":
            total = int(balance)+int(money)
            print(f"Parayı ekledin yeni bakiyen {total}")
            bankProcess.balanceUpdate(account_id,total)
        elif select =="h" or select == "H":
            print("İyi günler..")
        else:
            print("Yanlış seçim tekrar dene.")
            bankProcess.moneyDeposit(account_id,password,balance)

    def moneyWithdraw(account_id,password,balance):
        money = input("Çekeceğiniz parayı giriniz\n")
        if int(money)<=int(balance):
            select = input("Parayı çekebilirsiniz çekmek istiyormusunuz?(e/h)\n")
            if select == "e" or select == "E":
                total = int(balance)-int(money)
                print(f"Parayı çektiniz kalan bakiyen {total}")
                bankProcess.balanceUpdate(account_id,total)
            elif select =="h" or select == "H":
                print("İyi günler..")
            else:
                print("Yanlış işlem seçtin tekrar gir.")
                bankProcess.moneyWithdraw(account_id,password,balance)
        else:
            print("Girdiğiniz değer bakiyenizden fazla tekrar deneyin.")
            bankProcess.moneyWithdraw(account_id,password,balance)

    def balanceUpdate(account_id,balance):
        with open('account_information.txt',"r",encoding="utf-8") as file:
            liste = []
            for line in file:
                liste.append(bankProcess.balanceControl(line,account_id,balance))
            with open("account_information.txt","w",encoding="utf-8") as file2:
                for line in liste:
                    file2.write(line)

    def balanceControl(line,account_id,balance):
        line = line[:-1]
        liste = line.split(':')
        accountName = liste[0]
        accountPass = liste[1]
        if accountName == account_id:
            liste[2] = balance
        money = liste[2]

        return accountName+':'+accountPass+':'+str(money)+'\n'

bankProcess.start()