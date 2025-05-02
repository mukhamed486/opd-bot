import random
import logging
import pandas as pd
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "7642827641:AAGNl8UYh2ac2URXJuqR7UPEK7zv1MSfWIQ"

# 📊 База ИИ-инструментов
tools_data = [
    # Текст
    {"name": "ChatGPT", "type": "текст", "desc": "Генерации текстов, ответов на вопросы, ведения диалогов и помощи в создании различного контента на естественном языке", "link": "https://chat.openai.com/", "lang": "английский"},
    {"name": "Notion AI", "type": "текст", "desc": "Встроенный в платформу Notion интеллектуальный помощник, который помогает писать тексты, генерировать идеи, создавать списки задач, улучшать заметки и резюмировать большие объёмы информации.", "link": "https://www.notion.so/product/ai", "lang": "английский"},
    {"name": "CopyMonkey", "type": "текст", "desc": "ИИ для автоматического создания описаний товаров для маркетплейсов, оптимизированных под ключевые слова, что помогает быстро заполнять карточки продуктов и повышать конверсию.", "link": "https://copymonkey.ai", "lang": "английский"},
    {"name": "Jasper", "type": "текст", "desc": "Мощная нейросеть для копирайтинга и создания маркетингового контента, которая позволяет быстро генерировать статьи, рекламные тексты, посты для соцсетей и email-рассылки на основе заданных тем.", "link": "https://www.jasper.ai", "lang": "английский"},

    # Визуализация
    {"name": "Midjourney", "type": "визуализация", "desc": "Продвинутая нейросеть для генерации изображений по текстовым описаниям, специализирующаяся на создании фантастических, художественных и креативных визуализаций различной сложности.", "link": "https://midjourney.com", "lang": "английский"},
    {"name": "Leonardo AI", "type": "визуализация", "desc": "Генератор изображений и концепт-арта, предназначенный для дизайнеров, художников и геймеров, который позволяет создавать реалистичные сцены и персонажей на основе коротких текстовых подсказок.", "link": "https://leonardo.ai", "lang": "английский"},
    {"name": "Canva AI", "type": "визуализация", "desc": "Автоматическая генерация дизайнов, изображений, презентаций и других материалов с минимальными усилиями со стороны пользователя.", "link": "https://canva.com", "lang": "русский"},
    {"name": "NightCafe", "type": "визуализация", "desc": "Простая генерация изображений", "link": "https://creator.nightcafe.studio/", "lang": "английский"},

    # Видео
    {"name": "Runway", "type": "видео", "desc": "Универсальная платформа для создания и редактирования видео с помощью ИИ, позволяющая генерировать спецэффекты, удалять фоны, менять стиль и даже создавать короткие фильмы без опыта монтажа.", "link": "https://runwayml.com", "lang": "английский"},
    {"name": "Pictory", "type": "видео", "desc": "Сервис для превращения длинных текстов и статей в короткие видеоролики для социальных сетей, что помогает создавать контент в формате видео даже без специальных навыков работы с видеоредакторами.", "link": "https://pictory.ai", "lang": "английский"},
    {"name": "Synthesia", "type": "видео", "desc": "Мощная платформа для создания видео с виртуальными дикторами на основе текстовых сценариев, что позволяет быстро производить обучающие ролики, презентации и маркетинговые видео без съёмок.", "link": "https://synthesia.io", "lang": "английский"},

    # Перевод
    {"name": "DeepL", "type": "перевод", "desc": "Один из самых точных и качественных сервисов машинного перевода, который обеспечивает более естественный и грамматически правильный перевод текстов на разные языки по сравнению с аналогами.", "link": "https://deepl.com", "lang": "английский"},
    {"name": "Targum", "type": "перевод", "desc": "Нейросеть, специализирующаяся на переводе аудио и видео контента на разные языки в реальном времени, сохраняя при этом интонацию и эмоциональную окраску оригинального выступления.", "link": "https://targum.video", "lang": "русский"},

    # Дизайн и логотипы
    {"name": "Looka", "type": "дизайн", "desc": "Генератор логотипов", "link": "https://looka.com", "lang": "английский"},
    {"name": "Designs AI", "type": "дизайн", "desc": "Автоматический дизайн", "link": "https://designs.ai", "lang": "английский"},

    # Сайты / бизнес
    {"name": "Durable", "type": "сайт", "desc": "Конструктор сайтов, основанный на ИИ, который способен за считанные минуты сгенерировать полноценный сайт для малого бизнеса на основе краткого описания задачи без необходимости писать код.", "link": "https://durable.co", "lang": "английский"},
    {"name": "Bookmark", "type": "сайт", "desc": "Умный конструктор сайтов с поддержкой ИИ, который автоматически создаёт индивидуальные сайты на основе ответов пользователя на короткую анкету, оптимизируя контент и структуру.", "link": "https://bookmark.com", "lang": "английский"},

    # Презентации
    {"name": "Tome", "type": "презентации", "desc": "Генератор презентаций нового поколения, который автоматически создает слайды на основе текстового описания задачи, используя искусственный интеллект для оформления и структурирования информации.", "link": "https://tome.app", "lang": "английский"},
    {"name": "Beautiful.ai", "type": "презентации", "desc": "ИИ-платформа для создания красивых презентаций с минимальными усилиями, которая сама предлагает оформление слайдов, оптимальные композиции и визуальные решения для бизнес-отчётов и выступлений.", "link": "https://beautiful.ai", "lang": "английский"},

    # Картинки и арт
    {"name": "Fotor", "type": "фото", "desc": "Обработка фото с AI", "link": "https://www.fotor.com/features/ai-image-generator/", "lang": "английский"},
    {"name": "Remini", "type": "фото", "desc": "Улучшение качества фото", "link": "https://remini.ai", "lang": "английский"},
]

df = pd.DataFrame(tools_data)

# 🔎 Классификация задачи
def classify_task(text):
    text = text.lower()
    if any(w in text for w in ["текст", "контент", "статья", "эссе", "описание"]):
        return "текст"
    elif any(w in text for w in ["перевод", "перевести"]):
        return "перевод"
    elif any(w in text for w in ["логотип", "бренд", "дизайн"]):
        return "дизайн"
    elif any(w in text for w in ["изображение", "рисунок", "арт", "картинку"]):
        return "визуализация"
    elif any(w in text for w in ["презентац", "слайды", "презу"]):
        return "презентации"
    elif any(w in text for w in ["сайт", "лендинг", "веб"]):
        return "сайт"
    elif any(w in text for w in ["видео", "ролик", "анимация"]):
        return "видео"
    elif any(w in text for w in ["фото", "фотография", "обработка"]):
        return "фото"
    else:
        return "текст"

# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Текст", callback_data="тип_текст"),
        InlineKeyboardButton("Визуализация", callback_data="тип_визуализация"),
        InlineKeyboardButton("Перевод", callback_data="тип_перевод")
    ], [
        InlineKeyboardButton("Дизайн", callback_data="тип_дизайн"),
        InlineKeyboardButton("Видео", callback_data="тип_видео"),
        InlineKeyboardButton("Презентации", callback_data="тип_презентации"),
        InlineKeyboardButton("Сайт", callback_data="тип_сайт")
    ]]
    await update.message.reply_text(
     "🎓 <b>Добро пожаловать в интеллектуальный помощник СПбПУ!</b>\n"
        "Институт передовых производственных технологий\n\n"
        "🤖 <b>Цель бота:</b> помочь вам найти подходящие ИИ-инструменты для автоматизации задач в рамках управления проектами, учёбы и повседневной работы.\n\n"
        "🧠 <b>Что умеет бот:</b>\n"
        "• Предложить нейросети под ваши задачи: от текста до аналитики\n"
        "• Подобрать сервисы по ключевым словам (даже если просто пишете фразу)\n"
        "• Фильтровать инструменты по языку интерфейса\n"
        "• Принимать ваши идеи через /suggest\n\n"
        "📌 <b>Как пользоваться:</b>\n"
        "1️⃣ Выберите категорию задачи ниже\n"
        "2️⃣ Или напишите, что вам нужно (например: «сделай презентацию»)\n"
        "3️⃣ Получите список нейросетей с описанием и ссылками\n\n"
        "🛠 <i>Проект разработан в рамках учебной практики СПбПУ</i>\n"
        "📅 <i>Версия: апрель 2025</i>\n",
     parse_mode="HTML",
     reply_markup=InlineKeyboardMarkup(keyboard)
 )

# 🧠 Текстовая задача
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    task_type = classify_task(user_text)
    keyboard = [
        [InlineKeyboardButton("Русский", callback_data=f"язык_{task_type}_русский")],
        [InlineKeyboardButton("Английский", callback_data=f"язык_{task_type}_английский")],
        [InlineKeyboardButton("Любой", callback_data=f"язык_{task_type}_любой")]
    ]
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text

    responses = [
        "🧠 Обрабатываю вашу задачу...",
        "🤖 Уже ищу решения!",
        "💡 Секунду, подбираю ИИ-инструменты...",
        "📊 Анализирую ваш запрос...",
        "🔍 Думаю, что может подойти..."
    ]
    await update.message.reply_text(random.choice(responses), parse_mode="HTML")

    task_type = classify_task(user_text)
    keyboard = [
        [InlineKeyboardButton("Русский", callback_data=f"язык_{task_type}_русский")],
        [InlineKeyboardButton("Английский", callback_data=f"язык_{task_type}_английский")],
        [InlineKeyboardButton("Любой", callback_data=f"язык_{task_type}_любой")]
    ]
    await update.message.reply_text(
        f"📌 Обнаружен тип задачи: <b>{task_type}</b>\nВыберите язык интерфейса:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🔘 Выбор категории
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    task_type = query.data.replace("тип_", "")
    await show_tools(query.message, task_type, lang="любой")

# 🌐 Язык интерфейса
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, task_type, lang = query.data.split("_")
    await show_tools(query.message, task_type, lang)

# 🧰 Отображение инструментов
async def show_tools(message, task_type, lang="любой"):
    filtered = df[df["type"] == task_type]
    if lang != "любой":
        filtered = filtered[filtered["lang"] == lang]
    if filtered.empty:
        await message.reply_text("Инструменты по задаче не найдены.")
        return
    for _, row in filtered.iterrows():
        button = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Перейти", url=row["link"])]])
        await message.reply_text(
            f"<b>{row['name']}</b>\n{row['desc']}\n🌍 Язык: {row['lang']}",
            parse_mode="HTML",
            reply_markup=button
        )

# 📘 /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 <b>Как пользоваться:</b>\n"
        "1. Введите свою задачу (например: 'перевести видео')\n"
        "2. Выберите язык\n"
        "3. Получите список подходящих ИИ-инструментов\n\n"
        "/start — начать сначала\n"
        "/help — помощь",
        parse_mode="HTML"
    )
async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    suggestion = update.message.text.replace("/suggest", "").strip()
    if suggestion:
        await update.message.reply_text("Спасибо за ваше предложение! 🚀 Оно будет рассмотрено.")
        with open("suggestions.txt", "a", encoding="utf-8") as f:
            f.write(suggestion + "\n")
    else:
        await update.message.reply_text("Пожалуйста, напишите идею после команды /suggest.")
# ▶ main()
def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("suggest", suggest))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern="тип_"))
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern="язык_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
