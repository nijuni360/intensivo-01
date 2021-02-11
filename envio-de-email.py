import pandas as pd 
from IPython.display import display
import smtplib
import email.message
from decouple import config


df = pd.read_excel('Vendas.xlsx')
display(df)
faturamento = df [['ID Loja', 'Valor Final']] .groupby ('ID Loja').sum()
display(faturamento)
faturamento = faturamento.sort_values(by='Valor Final', ascending=False)
display(faturamento)
quantidade = df[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
quantidade = quantidade.sort_values(by='ID Loja',ascending=False)
display(quantidade)
ticket_medio = (faturamento['Valor Final'] /quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Medio'})
ticket_medio = ticket_medio.sort_values(by='Ticket Medio', ascending=False)
display(ticket_medio)
def enviar_email(resumo, loja):
    server = smtplib.SMTP('smtp.gmail.com:587')  
    corpo_email = "Corpo do E-mail"
    
    msg = email.message.Message()
    msg['Subject'] = "Assunto do E-mail"
    msg['From'] = config('EMAIL')
    msg['To'] = config('REM')
    password = config('SENHA')
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )
    
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

lojas = df['ID Loja'].unique()

for loja in lojas:
    tabela_loja = df.loc[df['ID Loja']== loja, ['ID Loja', 'Quantidade','Valor Final']]
    resumo_loja = tabela_loja.groupby('ID Loja').sum()
    resumo_loja['Ticket Medio'] = resumo_loja['Valor Final'] / resumo_loja['Quantidade']
    enviar_email(resumo_loja, loja)

tabela_diretoria = faturamento.join(quantidade).join(ticket_medio)
enviar_email(tabela_diretoria, 'Todas as Lojas')