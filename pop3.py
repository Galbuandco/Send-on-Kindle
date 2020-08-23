import socket
import ssl
import re


def conferma(user,passwd):
    #indirizzo e porta mail server pop3
    mailserver = ("pop.gmail.com", 995)
    
    # comandi del protocollo pop3 da inviare al server
    comandi = [f'{user} \r\n',f'{passwd} \r\n']
    
    # connesione al socket tramite tunneling ssl siccome gmail accetta solo conessioni crittofrate
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket = ssl.wrap_socket(
        clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    clientSocket.connect(mailserver)
    
    
    # esegue i comandi uno alla volta e restituisce la risposta
    for comando in comandi:
        clientSocket.sendall(str.encode(comando))
        print(clientSocket.recv(2048))
    
    #questo comando è a parte perchè ha richiesto un parsing del messaggio più difficoltoso 
    #non funzionava il ciclo "standard" come quello usato sotto per http,ma per qualche strano motivo il socket rimaneva in ascolto all'infinito
    #ho quidi dovuto forzare un timeout sul socket e gestire l'errore 

    clientSocket.send(str.encode("retr 254\r\n")) #ipotizzo che l'ultima mail arrivata sia quella di conferma
    clientSocket.settimeout(1.0)
    output=""
    while True:
        try:
            msg=clientSocket.recv(8)
            output=output+msg.decode("utf-8")
        except:
            #in questa parte prendo la mail e faccio un parsing per ottenre il link di convalida  
            stripped=re.sub("\r\n","",output)
            http= re.findall(r"<[A-Za-z%:0-9=?&-/_]*verification[A-Za-z%:0-9=?&-/_]*>",stripped)
            http= re.sub("<","",http[0])
            http= re.sub(">","",http)
            break
        
    
    #in questa ultima parte creo una connessione con amazon inviando una richiesta get del link di conferma        
    httpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    httpSocket = ssl.wrap_socket(
        httpSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    httpSocket.connect(("amazon.com",443))
    
    httpSocket.sendall(str.encode(f"""GET {http} HTTP/2
    Host: it.wikipedia.org
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate, br
    Referer: https://www.google.com/
    DNT: 1
    Connection: keep-alive
    Upgrade-Insecure-Requests: 1\r\n\r\n"""))

    #parsing della risposta anche se un po' inutile perchè poi non la uso    
    response = ''
    while True:
        recv = httpSocket.recv(1024)
        if not recv:
            break
        response += recv.decode("utf-8")
    
