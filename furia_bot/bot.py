# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import init_db, set_alert_status, get_alert_status, get_all_users_with_alerts
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime


TOKEN = '7581534483:AAHRnz8wyM1QprbwVPuE-FAy3A4T03iqqFI'

# Inicializa o banco de dados
init_db()

# Função para criar o menu principal com botões
def criar_menu_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Últimas Notícias", callback_data='noticias')],
        [InlineKeyboardButton("2. Próximos Jogos", callback_data='jogos')],
        [InlineKeyboardButton("3. Resultados Recentes", callback_data='resultados')],
        [InlineKeyboardButton("4. Conhecer o Time", callback_data='time')],
        [InlineKeyboardButton("5. Curiosidades", callback_data='curiosidades')],
        [InlineKeyboardButton("6. Loja Oficial", callback_data='loja')],
        [InlineKeyboardButton("7. Sorteios", callback_data='sorteios')],
        [InlineKeyboardButton("8. Encontrar Lobby", callback_data='encontrar_lobby')],
        [InlineKeyboardButton("9. Ativar alertas", callback_data='ativar_alertas')],
        [InlineKeyboardButton("10. Desativar alertas", callback_data='desativar_alertas')],
    ])

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá, Furioso! O que você quer ver hoje?",
        reply_markup=criar_menu_principal()
    )

# Comando /alertas para ver o status atual
async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    status = get_alert_status(user.id)

    if status:
        texto = "🔔 Você está recebendo alertas de jogos da FURIA."
    else:
        texto = "🔕 Você não está recebendo alertas de jogos da FURIA."

    await update.message.reply_text(texto, reply_markup=criar_menu_principal())

# Handler dos botões
async def botao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    respostas = {
        'noticias': "📰 Últimas notícias da FURIA:\n- Nova contratação anunciada!\n- Classificados para os playoffs!",
        'resultados': "✅ Resultados recentes:\n- FURIA 2x1 NIP\n- FURIA 1x2 Heroic",
        'time': "👥 Lineup atual da FURIA CS:\n- KSCERATO\n- yuurih\n- YEKINDAR\n- FalleN (IGL)\n- Molodoy",
        'curiosidades': "🤔 Você sabia?\nA FURIA já participou de mais de 20 torneios internacionais!",
        'loja': "🛒 Acesse a loja oficial da FURIA: [https://www.furia.gg/](https://www.furia.gg/)",
        'sorteios': "🎁 Sorteios ativos:\n- Camiseta autografada\n- A lendária AWP Redline ST do Professor (brincadeira... ou não 👀)",
    }

    if query.data == "ativar_alertas":
        set_alert_status(user.id, user.username, 1)
        await query.edit_message_text("✅ Alertas ativados! Você receberá notificações dos jogos da FURIA.")
        await context.bot.send_message(chat_id=query.message.chat_id, text="📋 Menu principal:", reply_markup=criar_menu_principal())
        return

    elif query.data == "desativar_alertas":
        set_alert_status(user.id, user.username, 0)
        await query.edit_message_text("🚫 Alertas desativados.")
        await context.bot.send_message(chat_id=query.message.chat_id, text="📋 Menu principal:", reply_markup=criar_menu_principal())
        return

    elif query.data == "jogos":
        texto_resposta = f"📅 Próximos jogos da FURIA:\n{obter_proximos_jogos()}"

    elif query.data == "encontrar_lobby":
        keyboard = [
            [InlineKeyboardButton("🎯 Matchmaking", callback_data="lobby_matchmaking")],
            [InlineKeyboardButton("🕹️ Gamers Club", callback_data="lobby_gc")],
            [InlineKeyboardButton("🔥 Face It", callback_data="lobby_faceit")],
            [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")],
        ]
        await query.edit_message_text("🎮 Escolha uma plataforma para encontrar um lobby:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif query.data == "voltar_menu":
        await query.edit_message_text("👋 Olá, Furioso! O que você quer ver hoje:", reply_markup=criar_menu_principal())
        return

    elif query.data == "lobby_matchmaking":
        texto_resposta = "🎯 Matchmaking: entre na fila com seus amigos no CS2 e boa sorte!"

    elif query.data == "lobby_gc":
        texto_resposta = "🕹️ Gamers Club: acesse https://gamersclub.gg/cs e crie sua sala personalizada!"

    elif query.data == "lobby_faceit":
        texto_resposta = "🔥 FACEIT: jogue competitivo no nível mais alto! https://www.faceit.com/"

    elif query.data in respostas:
        texto_resposta = respostas[query.data]

    else:
        texto_resposta = "❌ Opção inválida."

    await query.edit_message_text(texto_resposta, parse_mode='Markdown')
    await context.bot.send_message(chat_id=query.message.chat_id, text="📋 Menu principal:", reply_markup=criar_menu_principal())

# Scraping dos jogos da FURIA
def obter_proximos_jogos():
    url = 'https://www.hltv.org/team/8297/furia'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "⚠️ Erro ao buscar os jogos. Tente novamente mais tarde."

    soup = BeautifulSoup(response.text, 'html.parser')
    jogos = []

    for match in soup.select('.upcomingMatches .match'):
        try:
            data = match.select_one('.matchTime').get('data-unix')
            timestamp = int(data) // 1000
            horario = datetime.fromtimestamp(timestamp).strftime('%d/%m %H:%M')

            time1 = match.select_one('.matchTeam1 .team').text.strip()
            time2 = match.select_one('.matchTeam2 .team').text.strip()
            evento = match.select_one('.matchEvent .event-name').text.strip()

            jogos.append(f"{horario} - {time1} vs {time2} ({evento})")
        except Exception:
            continue

    return '\n'.join(jogos) if jogos else "🔍 Nenhum jogo encontrado no momento."

# Envia alerta programado
async def enviar_alerta(application):
    mensagem = "📢 *Atenção!*\nA FURIA joga hoje às 20h! Não perca! 🔥"
    for user_id in get_all_users_with_alerts():
        try:
            await application.bot.send_message(chat_id=user_id, text=mensagem, parse_mode='Markdown')
        except Exception as e:
            print(f"Erro ao enviar mensagem para {user_id}: {e}")

# Inicialização do bot e agendador
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alertas", alertas))
    app.add_handler(CallbackQueryHandler(botao_handler))

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(enviar_alerta(app)), 'cron', hour=17, minute=0)
    scheduler.start()

    print("🤖 Bot rodando com agendador ativo...")
    app.run_polling()
