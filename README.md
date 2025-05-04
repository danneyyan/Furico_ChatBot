Chat bot no telegram para o precesso seletivo da FURIA

Este é um chatbot simples onde o objetivo é deixar o fã furioso sempre atualizado das novidades da FURIA
Neste chat temos informações básicas como - Notícias da FURIA
- Jogos futuros (via HLTV)
- Resultados recentes
- Conhecer lineup
- Alertas personalizados
- Integração com FACEIT e Gamers Club

Para executá-lo são necessários
- Python 3.10+
- Telegram Bot Token
- bibliotecas: `python-telegram-bot`, `requests`, `bs4`, `apscheduler`, etc.

Para acessá-lo execute o código e acesse o link "t.me/dyfurico_bot"

Estrutura do projeto
bot.py - script principal
database.py - gerenciamento de alertas

Para instalar e rodar localmente
git clone https://github.com/seunome/bot-furia.git
cd bot-furia
pip install -r requirements.txt
python bot.py

(Nota aos avaliadores. A intenção era fazer um chatbot e implementar nele uma personalidade do mascote da Fúria, o furico. 
Inicialmente o prejeto seria executado com foco no whatsapp devido a maior abrangência, porém, para esse caso existem barreiras pagas. 
Também planejei construir ferramentas onde os jogadores podem enviar mensagens importantes, lembretes, etc, através do FuricoBot para a base de usuários. E finalizar a ferramenta para usuários do chat encontrarem jogadores e organizar lobbys na GC, valve ou FaceIt através do chat, no entanto não consegui executar completamente devido a minha escassez de tempo)
