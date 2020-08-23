import socket
import ssl
import base64
import pexpect

def invia_mail_con_allegato(username,password,nome_file,alias):
    
    #indirizzo e porta mailserver 
    mailserver = ("smtp.gmail.com", 465)

    #ecoding di username e password 
    encodedBytes = base64.b64encode(username.encode("utf-8"))
    user = str(encodedBytes, "utf-8")
    encodedBytes = base64.b64encode(password.encode("utf-8"))
    passwd = str(encodedBytes, "utf-8")

    #encoding del file fatto da riga di comando
    child=pexpect.spawn("/usr/bin/base64",[nome_file])
    file=str(child.read(),"utf-8")



    
#comandi del protocollo smtp da inviare al server
# la struttura della mail l'ho ricavata copiandola da una vecchia mail scaricata tramite pop3 per vederla in formato "grezzo"
    comandi=['helo smtp.gmail.com \r\n','auth login \r\n',f'{user} \r\n',f'{passwd} \r\n',"mail from:<myself>\r\n",f"rcpt to:<{alias}>\r\n","DATA\r\n",
    f"""Subject: convert
Content-Type: multipart/mixed; boundary="00000000000069402205aa1847c8"

--00000000000069402205aa1847c8
Content-Type: multipart/alternative; boundary="00000000000069401e05aa1847c6"

--00000000000069401e05aa1847c6
Content-Type: text/plain; charset="UTF-8"



--00000000000069401e05aa1847c6
Content-Type: text/html; charset="UTF-8"

<div dir="ltr"><br></div>

--00000000000069401e05aa1847c6--
--00000000000069402205aa1847c8
Content-Type: application/pdf; name="{nome_file}"
Content-Disposition: attachment; filename="{nome_file}"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_kcgeai2l0
Content-ID: <f_kcgeai2l0>

{file}
--00000000000069402205aa1847c8--
 \r\n.\r\n""","quit"]

#connesione al socket tramite tunneling ssl siccome gmail accetta solo conessioni crittofrate 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    clientSocket.connect(mailserver)

    
#esegue i comandi uno alla volta e restituisce la risposta
    for comando in comandi:
        clientSocket.sendall(str.encode(comando))
        print(clientSocket.recv(1024))