# Premium API
Uma API simples para gerenciamento das atividades do Premium Estúdio.
<br>Referências: 
  <br>-<a href="https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04-pt">Como servir aplicativos Flask com o Gunicorn e o Nginx.</a>
  <br>-<a href="https://www.youtube.com/watch?v=WFzRy8KVcrM">Construindo uma API REST com Python e Flask.</a>
> :construction: Projeto em construção :construction:
## Iniciando o projeto
Nada de muito diferente por aqui. Usei OOP e ORM, então os modelos estão em /models e a relação com o DB está no database.py. Para alterar do SQLite para qualquer outro db, basta alterar a string do SQLAlchemy no .flaskenv.

## Autenticação
Estou usando JWT, resta verificar como alterar isso para ambientes de intranet.

## Swagger
A implementação é bem simples com o Flasgger. O Swagger é iniciado no app.py e os yamls estão na pasta /docs. Daí basta adicionar os decoradores antes das funcões apontando para os respectivos yamls.
```
@swag_from('./docs/class/def.yaml')
```

## Resumo bem rápido sobre a utilização do Flask
O caminho aqui é usar os decoradores para marcar as rotas. Basta marcar com o método e o caminho da url e escrever a função logo em seguida que a mágica acontece.

## Servindo no CentOS com Linux
### Instale o gunicorn na pasta do projeto
Ele será o servidor de aplicação.
```
python3 -m pip install gunicorn
```
### Crie um arquivo wsgi.py na pasta do projeto, iniciando o app.py.
```
from src.app import app as application

if __name__ == "__main__":
    application.run()
```
Teste para garantir que tudo está de pé.
```
gunicorn --bind 0.0.0.0:5000 wsgi
```
### Crie um arquivo .service em /etc/system.d/system/
```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=<caminho do diretório>
Environment="PATH=<caminho da venv/bin do projeto>"
ExecStart=<caminho do gunicorn usado*>/gunicorn --workers 3 --bind unix:/run/myproject.sock -m 007 wsgi

[Install]
WantedBy=multi-user.target
```

* obtenha o caminho do gunicorn com o venv ativado, usando 
```
which gunicorn
```

## Suba o serviço
```
systemctl start myproject.service
systemctl enable myproject.service
```

## Crie a configuraçao para o projeto no sites-available do Nginx
```
  
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include proxy_params;
        proxy_pass http://unix:<caminho do sock>/myproject.sock;
    }
}
```

## Inclua o link no sites-enabled 
```
ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

## Confira se está tudo certo e libere os acessos
Confira se a sintaxe do conf está certa, reinicie o Nginx e libere o firewall. Caso o Nginx não consiga acessar o sock, mesmo com as permissões, use o último comando abaixo.
```
nginx -t
systemctl restart nginx
ufw allow 'Nginx Full'
sudo setenforce 0
```

