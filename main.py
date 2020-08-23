#ho spilatto in due moduli il codice pe l'invio e la conferma per un maggior ordine
import smtp
import pop3


#L'inoltro di un filie sul kindle richiede di mandare una mail al proprio alias e per alcuni account 
#è anche necessario verficare il documento 

#input dati utenti
scelta= input ("Usare default o cambiare utente ?")
if (scelta=="default"):
    #smtp.invia_mail_con_allegato(mail,paaasword,documento,alisa)
else:
    user = (input("username\n"))
    user= user.strip()
    passwd = input("password\n")
    passwd = passwd.strip()
    doc = input("file\n")
    doc = doc.strip()
    mail= input("alias Mail\n")
    mail = mail.strip()

    #richiamo i moduli creati a seconda della necessità
    if (input("Ti viene richiesta la conferma ? si/no \n")=="si"):
        smtp.invia_mail_con_allegato(user,passwd,doc,mail)
    else:
        smtp.invia_mail_con_allegato(user,passwd,doc,mail)
        pop3.conferma(user,passwd)

