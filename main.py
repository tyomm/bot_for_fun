import telebot
from telebot import types
import time
import random
import datetime
import threading
from zoneinfo import ZoneInfo # Standard library module for timezones (Python 3.9+)
import re # For regular expressions in search

# --- Configuration ---
# IMPORTANT: Replace these with your actual details!
API_TOKEN = '7914179938:AAHqo1ZPgEb_s2SbF9ouvBS_cgf1ID1JiYw' # Get this from @BotFather
GIRLFRIEND_USER_ID = 6921647429  # 7843995956 Your girlfriend's Telegram User ID (integer)
YOUR_TELEGRAM_USER_ID = 6921647429 # Your Telegram User ID (integer), for forwarding messages


# Initialize the bot
bot = telebot.TeleBot(API_TOKEN)

# --- Global Data and Messages ---
# You can expand these lists endlessly to make the bot 'very long'!

# User state management: {chat_id: 'current_state'}
# States: 'main_menu', 'love_menu', 'memories_menu', 'sparkle_menu', 'feel_menu',
#         'games_menu', 'wyr_game', 'guess_number_game', 'baseball_game', 'film_search', 'music_search'
user_states = {}
# Game specific data: {chat_id: {'question_index': 0, 'secret_number': 0, 'attempts': 0, 'balls': 0, 'strikes': 0, 'outs': 0, 'hits': 0, 'bases': [False, False, False]}}
game_data = {}

# Start messages
START_MESSAGES = {
    "part1": "Hello, my dearest Hiyori", # Personalized for Hiyori
    "part2": "! I've created this little corner of the internet just for you, filled with all my love. Think of me as your personal companion, ready to bring a smile to your face whenever you need it.",
    "part3": "\n\nWhat would you like to do today, my love? Press the buttons as much as you want😁"
}

# Love Messages (for "💖 Send Me Love" section)
LOVE_MESSAGES = {
    "morning": [
        "Good morning, my sunshine! May your day be as bright and beautiful as your smile. ☀️",
        "Rise and shine, my love! Sending you a big hug to start your day. 😊",
        "Waking up with you in my thoughts is the best feeling. Have a wonderful day, my dearest Hiyori! ❤️",
        "Every sunrise reminds me of the new beginnings we share. Good morning, my love!",
        "May your coffee be strong and your day be filled with joy. Thinking of you! ☕💖",
        "A new day, a new chance to tell you how much I adore you. Good morning, sleepyhead! 😴",
        "Sending you a virtual kiss to start your day. Have a magnificent day, my love! 💋",
        "The world is a better place with you in it. Good morning, my beautiful inspiration!",
        "May your day be filled with laughter and little moments of pure happiness. Good morning! 😊",
        "Just wanted to send some love your way as you begin your day. You're amazing! ❤️"
    ],
    "just_because": [
        "My heart skips a beat every time I think of you. You're my favorite thought.",
        "Just wanted to remind you how incredibly special you are to me. You light up my world.",
        "Every moment with you is a treasure. Thank you for being you.",
        "You are my sunshine, my only sunshine. You make me happy when skies are gray.",
        "Your smile is my favorite thing in the world.",
        "I'm so incredibly lucky to have you in my life. You make everything better.",
        "Thinking of you and smiling. Sending you all my love!",
        "You're not just my girlfriend, you're my best friend, my confidant, my everything.",
        "My love for you grows with each passing breath. You are my everything.",
        "You're the missing piece I never knew I needed. So glad I found you. 🥰",
        "You inspire me to be a better person every single day.",
        "Just seeing your name pop up on my phone makes me smile.",
        "You have a way of making even the ordinary feel extraordinary.",
        "I love the way you [specific thing Hiyori does, e.g., hum when you're happy/solve problems].",
        "You're my favorite adventure, my favorite story, my favorite dream.",
        "If I had a flower for every time I thought of you, I could walk through my garden forever. 🌸",
        "You're the reason my heart sings.",
        "Every day with you is a new reason to fall deeper in love.",
        "You're simply irresistible to me.",
        "I cherish every single memory we've made together."
    ],
    "night": [
        "Good night, my love. Sweet dreams filled with happiness and peace. 🌙✨",
        "As you drift to sleep, know that you are deeply loved and cherished. Sleep well, my beautiful Hiyori. ❤️",
        "Sending you a warm hug and all my love before you sleep. See you in my dreams. 😴",
        "May your dreams be as sweet as you are. Good night, my angel.",
        "Counting down the moments until I can see you again. Sleep tight, my love.",
        "Close your eyes, my darling. I'll be dreaming of you.",
        "Wishing you a night as peaceful and beautiful as you are.",
        "The stars are twinkling, just like your eyes. Good night, my shining star.",
        "Rest well, my queen. You deserve all the peace and comfort in the world.",
        "Sending you a final thought of love before I close my eyes. Good night, my everything."
    ]
}

# Compliments (for "✨ A Little Sparkle" -> "🌟 Compliment Me!" and direct button)
COMPLIMENTS = [
    "Your laugh is the most beautiful sound in the world, Hiyori.",
    "I adore your kindness and how you make everyone around you feel loved.",
    "You're not just beautiful on the outside, but your heart shines even brighter.",
    "Your intelligence and wit always amaze me.",
    "I love your strength and resilience.",
    "You have the most captivating eyes.",
    "Your passion for drawing is so inspiring.",
    "Every outfit you wear looks amazing on you.",
    "You have a way of making even the toughest days feel manageable.",
    "Your creativity is truly inspiring.",
    "You're an incredible listener, and I appreciate that so much.",
    "You have a way of making everyone around you feel comfortable and happy.",
    "Your determination is one of the things I admire most about you.",
    "You're simply radiant, inside and out.",
    "I love your unique perspective on things.",
    "You bring so much joy into my life.",
    "You're truly one of a kind, and I'm so lucky to have you.",
    "Your empathy and compassion are boundless.",
    "You make the world a better place just by being in it.",
    "Your sense of humor is absolutely charming.",
    "You're incredibly graceful.",
    "I love how thoughtful you are.",
    "You have the most infectious smile.",
    "You handle challenges with such poise.",
    "You're an amazing problem-solver.",
    "Your presence brightens any room.",
    "You're wonderfully adventurous.",
    "I admire your unwavering spirit.",
    "You're beautiful in every single way."
]

# Our Memories (for "💌 Our Memories" section)
# For photos, you'd ideally upload them to Telegram once and use their file_id.
# For simplicity, we'll use text and placeholder URLs.
OUR_MEMORIES = [
    {"text": "Remember our first date at [Place]? I knew then you were special. ❤️", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Our+First+Date"},
    {"text": "That time we [funny shared memory, e.g., got lost on that hike and ended up finding that amazing view]? I still laugh thinking about it!", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Funny+Moment"},
    {"text": "Our trip to [Place, e.g., the mountains/beach] was unforgettable. Every moment with you is an adventure.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Our+Trip"},
    {"text": "The day we [important event together, e.g., adopted our pet/moved into our first place]. My heart was so full.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Special+Event"},
    {"text": "I'll never forget our first kiss. It was magical.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=First+Kiss"},
    {"text": "Remember that cozy evening when we [e.g., watched that movie/cooked dinner together]? Pure bliss.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Cozy+Evening"},
    {"text": "Every time I see [something that reminds you of her, e.g., a specific flower/a certain color], I think of you and smile.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Thinking+of+You"},
    {"text": "That unforgettable night we [e.g., danced until dawn/watched the meteor shower]. Pure magic with you.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Unforgettable+Night"},
    {"text": "Remember when we [e.g., tried that new restaurant/explored that hidden gem]? Every adventure is better with you.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Our+Adventure"},
    {"text": "That quiet moment when we [e.g., just held hands/shared a comfortable silence]. Those moments mean the world to me.", "photo_url": "https://placehold.co/600x400/FFC0CB/000000?text=Quiet+Moments"},
]

# Music Database (for "🎵 Our Soundtrack" -> "Search Music")
# IMPORTANT: These are placeholder links. Actual MP3 files cannot be sent directly.
MUSIC_DATABASE = [
    {"title": "Perfect", "artist": "Ed Sheeran", "link": "https://www.youtube.com/watch?v=2Vv-BfVoq4g", "genre": "Pop"},
    {"title": "All of Me", "artist": "John Legend", "link": "https://www.youtube.com/watch?v=450209w1010", "genre": "R&B"},
    {"title": "A Thousand Years", "artist": "Christina Perry", "link": "https://www.youtube.com/watch?v=rtOvBOTyX00", "genre": "Pop"},
    {"title": "Can't Help Falling in Love", "artist": "Elvis Presley", "link": "https://www.youtube.com/watch?v=vGJTaP6anOU", "genre": "Rock and Roll"},
    {"title": "Thinking Out Loud", "artist": "Ed Sheeran", "link": "https://www.youtube.com/watch?v=lp-EO5I60KA", "genre": "Pop"},
    {"title": "Your Song", "artist": "Elton John", "link": "https://www.youtube.com/watch?v=Cr-SqRLmecI", "genre": "Pop"},
    {"title": "Make You Feel My Love", "artist": "Adele", "link": "https://www.youtube.com/watch?v=0put0_tgyss", "genre": "Soul"},
    {"title": "Stand By Me", "artist": "Ben E. King", "link": "https://www.youtube.com/watch?v=hwZNLlA7QhE", "genre": "Soul"},
    {"title": "Something", "artist": "The Beatles", "link": "https://www.youtube.com/watch?v=Uelzvgj_g30", "genre": "Rock"},
    {"title": "Crazy Little Thing Called Love", "artist": "Queen", "link": "https://www.youtube.com/watch?v=zO6D_BAuYCI", "genre": "Rock and Roll"},
    {"title": "First Love (初恋)", "artist": "Hikaru Utada", "link": "https://www.youtube.com/watch?v=F0Kx0L_4k20", "genre": "J-Pop"}, # Example for Hiyori
    {"title": "Pretender (Official髭男dism)", "artist": "Official Hige Dandism", "link": "https://www.youtube.com/watch?v=mH92X-2gG9I", "genre": "J-Pop"}, # Example for Hiyori
    {"title": "Lemon", "artist": "Kenshi Yonezu", "link": "https://www.youtube.com/watch?v=SX_TSY7m0uY", "genre": "J-Pop"}, # Example for Hiyori
    # Add more songs that are special to you both, especially J-Pop for Hiyori!
]

# Film Database (for "🎬 Film Suggestion" -> "Search Films")
# IMPORTANT: These are placeholder links.
FILM_DATABASE = [
    {"title": "The Notebook", "genre": "Romance", "description": "A timeless story of enduring love.", "link": "https://www.imdb.com/title/tt0332280/"},
    {"title": "La La Land", "genre": "Musical/Romance", "description": "A vibrant and bittersweet tale of dreams and love in Los Angeles.", "link": "https://www.imdb.com/title/tt3783958/"},
    {"title": "About Time", "genre": "Romance/Comedy/Sci-Fi", "description": "A charming story about time travel and finding happiness in everyday moments.", "link": "https://www.imdb.com/title/tt2100440/"},
    {"title": "Pride & Prejudice", "genre": "Romance/Drama", "description": "A beautiful adaptation of Jane Austen's classic novel.", "link": "https://www.imdb.com/title/tt0414387/"},
    {"title": "When Harry Met Sally...", "genre": "Romantic Comedy", "description": "A classic exploration of whether men and women can truly be just friends.", "link": "https://www.imdb.com/title/tt0098635/"},
    {"title": "Eternal Sunshine of the Spotless Mind", "genre": "Sci-Fi/Romance", "description": "A unique and thought-provoking film about love, loss, and memory.", "link": "https://www.imdb.com/title/tt0338013/"},
    {"title": "Amelie", "genre": "Romantic Comedy/Fantasy", "description": "A whimsical tale of a shy waitress in Paris who secretly orchestrates the lives of those around her.", "link": "https://www.imdb.com/title/tt0211915/"},
    {"title": "Before Sunrise", "genre": "Romance/Drama", "description": "Two strangers meet on a train and spend a magical night exploring Vienna.", "link": "https://www.imdb.com/title/tt0112471/"},
    {"title": "500 Days of Summer", "genre": "Romantic Comedy/Drama", "description": "A non-linear look at a relationship from beginning to end, exploring love and heartbreak.", "link": "https://www.imdb.com/title/tt1022603/"},
    {"title": "Silver Linings Playbook", "genre": "Romantic Comedy/Drama", "description": "Two individuals struggling with mental health find an unexpected connection.", "link": "https://www.imdb.com/title/tt1045658/"},
    {"title": "Your Name (君の名は。)", "genre": "Animation/Romance/Fantasy", "description": "Two strangers find themselves linked in a bizarre way. When a comet approaches, they must find each other.", "link": "https://www.imdb.com/title/tt5311514/"}, # Example for Hiyori
    {"title": "Weathering With You (天気の子)", "genre": "Animation/Romance/Fantasy", "description": "A high school boy who has run away to Tokyo befriends a girl who can manipulate the weather.", "link": "https://www.imdb.com/title/tt9426210/"}, # Example for Hiyori
    # Add more films she might enjoy or that are meaningful to you both!
]

# Motivation Messages (for "💡 Motivation Boost" button)
MOTIVATION_MESSAGES = [
    "You are capable of amazing things, my love. Believe in yourself as much as I believe in you. ✨",
    "Every step forward, no matter how small, is progress. Keep going, you're doing great!",
    "Your dreams are within reach. Work hard, stay focused, and never give up. I'm always cheering for you!",
    "Remember your strength. You've overcome challenges before, and you'll conquer this one too.",
    "Let your light shine brightly, always. You are a true inspiration.",
    "Don't be afraid to take risks. Growth happens outside your comfort zone.",
    "You are enough, just as you are. Embrace your unique brilliance.",
    "The only limit is your imagination. Dream big, my love!",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "You are stronger than you think. You are loved more than you know.",
    "The best way to get started is to quit talking and begin doing. - Walt Disney",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "It always seems impossible until it's done. - Nelson Mandela",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. - Zig Ziglar"
]

# "I am sad now" responses
SAD_RESPONSES = [
    "Oh, my love. I'm so sorry you're feeling sad. Please know I'm here for you, always. Sending you the biggest hug. ❤️",
    "It breaks my heart to hear you're sad. Remember that it's okay to feel this way, and I'm here to listen if you want to talk, or just to sit in silence with you.",
    "Sending you all my comfort and warmth. May your sadness pass quickly, and know that you are deeply cherished.",
    "Even on cloudy days, your light still shines. I'm sending you virtual sunshine and a gentle squeeze. You're not alone.",
    "My dearest, please don't carry this burden alone. Let me share it with you. What can I do to make you feel even a tiny bit better right now?",
    "A little virtual hot chocolate for my sweet love. ☕ It's okay to not be okay. I'm here for you.",
    "When you feel overwhelmed, remember to breathe. I'm sending you peace and calm. You are strong.",
    "Your happiness is my priority. How can I help brighten your day, even just a little?",
    "Sending you a warm, comforting blanket of love. Wrap yourself in it and know you're safe with me.",
    "Even the strongest hearts need a moment to rest. Take your time, my love. I'm right here."
]

# Secret Message (can be updated manually or via a special command only you know)
SECRET_MESSAGE = "You are the most incredible person I know, and every day with you is a gift. My love for you grows with each passing moment. You are my destiny. You are my sun, my moon, and all my stars. ❤️"

# --- Game Data for "Would You Rather" ---
WOULD_YOU_RATHER_QUESTIONS = [
    {"question": "Would you rather be able to fly or be invisible?", "options": ["Fly", "Invisible"]},
    {"question": "Would you rather live without internet or live without air conditioning?", "options": ["No Internet", "No AC"]},
    {"question": "Would you rather be able to talk to animals or speak all human languages?", "options": ["Talk to Animals", "All Languages"]},
    {"question": "Would you rather have unlimited money or unlimited time?", "options": ["Unlimited Money", "Unlimited Time"]},
    {"question": "Would you rather explore outer space or the deep ocean?", "options": ["Outer Space", "Deep Ocean"]},
    {"question": "Would you rather always be 10 minutes late or always be 20 minutes early?", "options": ["10 Mins Late", "20 Mins Early"]},
    {"question": "Would you rather have a perpetually messy room or a perpetually messy mind?", "options": ["Messy Room", "Messy Mind"]},
    {"question": "Would you rather be able to teleport or be able to read minds?", "options": ["Teleport", "Read Minds"]},
    {"question": "Would you rather be a master of every musical instrument or a master of every sport?", "options": ["Music Master", "Sport Master"]},
    {"question": "Would you rather have a personal chef or a personal masseuse?", "options": ["Personal Chef", "Personal Masseuse"]},
]

# --- Baseball Game Data ---
BASEBALL_OUTCOMES = {
    "swing": {
        "strike": ["Strike! ❌ You swung at a bad pitch.", "Swing and a miss! ⚾️❌", "Strike one! You'll get the next one!"],
        "foul": ["Foul ball! 💨 Still in the game.", "Just a tip, foul ball. Keep your eye on it!"],
        "hit": ["💥 Crack! It's a HIT! ⚾️🏃‍♀️ You're on base!", "Amazing hit, Hiyori! 🤩", "That's a single! Great job!"],
        "out": ["Out! ⚾️ You hit it right to the fielder. Better luck next time."],
    },
    "wait": {
        "ball": ["Ball! ✅ Good eye, Hiyori.", "That's a ball. Smart decision!", "Ball one. Patience pays off."],
        "strike": ["Strike! ❌ You watched a good one go by.", "Strike two! That was a tempting pitch.", "Strike! The umpire calls it."],
    }
}

# --- Keyboard Functions ---

def get_main_menu_keyboard():
    """Returns the main menu ReplyKeyboardMarkup with many buttons."""
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        types.KeyboardButton("💖 Send Me Love"),
        types.KeyboardButton("💌 Our Memories"),
        types.KeyboardButton("✨ A Little Sparkle"),
        types.KeyboardButton("🎵 Our Soundtrack"),
        types.KeyboardButton("💭 Tell Me How You Feel"),
        types.KeyboardButton("🎁 Surprise Me!"),
        types.KeyboardButton("🔒 Secret Message"),
        types.KeyboardButton("🫂 Hug Me"),
        types.KeyboardButton("😽 Meow!"),
        types.KeyboardButton("🐾 Mrrr..."),
        types.KeyboardButton("💋 Kiss Me"),
        types.KeyboardButton("🎬 Film Suggestion"),
        types.KeyboardButton("🌟 Compliment Me!"),
        types.KeyboardButton("❓ About Me?"),
        types.KeyboardButton("💡 Motivation Boost"),
        types.KeyboardButton("😔 I Am Sad Now"),
        types.KeyboardButton("🎨 Sketch Me"),
        types.KeyboardButton("🎲 Play a Game"), # Leads to games sub-menu
        types.KeyboardButton("❤️ My Heart"),
        types.KeyboardButton("🤔 Honest Mind"),
        types.KeyboardButton("💞 Tyom"),
        types.KeyboardButton("Click Me💋")
    ]
    keyboard.add(*buttons)
    return keyboard

#=========================================================================
good_girl_messages = [
    "That’s my good girl. 😈💦",
    "You love being my good girl, don’t you? 😏👅",
    "Only good girls get rewarded… 🥵🎁",
    "Say it again, just like that. Good girl. 🔥💋",
    "Mmm, such a good girl for me. 😮‍💨🍑",
    "You make it so hard to behave, good girl. 😜🫦",
    "Good girls like you always know how to tease. 😋💄",
    "The way you look at me… yeah, that's a very good girl. 👀😈",
    "You earned it, baby. Good girl. 🖤😌",
    "I love it when my good girl listens. 😍🫶",
    "Don’t stop… good girl, just like that. 🥵💦",
    "Even when you’re bad, you’re still my good girl. 😏🔗"
]

user_indexes = {}

# Create the button somewhere in your code
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton("Click Me💋"))

# Handle "Click Me💋" button presses
@bot.message_handler(func=lambda message: message.text == "Click Me💋")
def handle_click_me(message):
    uid = message.chat.id
    idx = user_indexes.get(uid, 0)
    bot.send_message(uid, good_girl_messages[idx])
    user_indexes[uid] = (idx + 1) % len(good_girl_messages)

# ======================================================================

def get_love_sub_menu():
    """Returns the inline keyboard for 'Send Me Love' options."""
    keyboard = [
        [types.InlineKeyboardButton("🌞 Good Morning, Sunshine!", callback_data='love_morning')],
        [types.InlineKeyboardButton("💖 Just Because I Love You", callback_data='love_just_because')],
        [types.InlineKeyboardButton("🌙 Sweet Dreams, My Love", callback_data='love_night')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_memories_sub_menu():
    """Returns the inline keyboard for 'Our Memories' options."""
    keyboard = [
        [types.InlineKeyboardButton("📸 See Our Photos", callback_data='memory_photo')],
        [types.InlineKeyboardButton("😄 Our Funniest Moments", callback_data='memory_funny')],
        [types.InlineKeyboardButton("🫂 Our Firsts", callback_data='memory_firsts')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_sparkle_sub_menu():
    """Returns the inline keyboard for 'A Little Sparkle' options."""
    keyboard = [
        [types.InlineKeyboardButton("🌟 Compliment Me!", callback_data='sparkle_compliment')],
        [types.InlineKeyboardButton("💡 Wise Words for My Love", callback_data='sparkle_wise_words')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_feel_sub_menu():
    """Returns the inline keyboard for 'Tell Me How You Feel' options."""
    keyboard = [
        [types.InlineKeyboardButton("😊 Happy", callback_data='feel_happy'),
         types.InlineKeyboardButton("🙁 Sad", callback_data='feel_sad')],
        [types.InlineKeyboardButton("💖 Loved", callback_data='feel_loved'),
         types.InlineKeyboardButton("😔 Stressed", callback_data='feel_stressed')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_games_sub_menu():
    """Returns the inline keyboard for games options."""
    keyboard = [
        [types.InlineKeyboardButton("🎲 Would You Rather?", callback_data='game_wyr')],
        [types.InlineKeyboardButton("🔢 Guess the Number", callback_data='game_guess_number')],
        [types.InlineKeyboardButton("⚾️ Baseball Game", callback_data='game_baseball')], # New Baseball Game button
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_wyr_game_keyboard(question_index):
    """Returns inline keyboard for 'Would You Rather' game choices."""
    question_data = WOULD_YOU_RATHER_QUESTIONS[question_index]
    keyboard = [
        [types.InlineKeyboardButton(question_data["options"][0], callback_data=f'wyr_choice_{question_index}_0'),
         types.InlineKeyboardButton(question_data["options"][1], callback_data=f'wyr_choice_{question_index}_1')],
        [types.InlineKeyboardButton("➡️ Next Question", callback_data='wyr_next'),
         types.InlineKeyboardButton("🛑 End Game", callback_data='wyr_end')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_baseball_game_keyboard():
    """Returns inline keyboard for baseball game actions."""
    keyboard = [
        [types.InlineKeyboardButton("🏏 Swing!", callback_data='baseball_swing'),
         types.InlineKeyboardButton("👀 Wait!", callback_data='baseball_wait')],
        [types.InlineKeyboardButton("🛑 End Game", callback_data='baseball_end')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_baseball_game_over_keyboard():
    """Returns inline keyboard for baseball game over options."""
    keyboard = [
        [types.InlineKeyboardButton("⚾️ Play Again?", callback_data='game_baseball')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)


def get_film_options_keyboard():
    """Returns inline keyboard for film options."""
    keyboard = [
        [types.InlineKeyboardButton("🎬 Get a Random Film", callback_data='film_random')],
        [types.InlineKeyboardButton("🔍 Search Films by Title", callback_data='film_search_prompt')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_music_options_keyboard():
    """Returns inline keyboard for music options."""
    keyboard = [
        [types.InlineKeyboardButton("🎵 Get a Random Song", callback_data='music_random')],
        [types.InlineKeyboardButton("🔍 Search Music by Title/Artist", callback_data='music_search_prompt')],
        [types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
    ]
    return types.InlineKeyboardMarkup(keyboard)

def get_back_to_main_menu_inline_keyboard():
    """Simple inline keyboard to go back to main menu."""
    keyboard = [[types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]
    return types.InlineKeyboardMarkup(keyboard)

# --- Message Handlers ---

@bot.message_handler(commands=['start'])
def start_message(message):
    """Handles the /start command, welcomes the user, and sets up the main keyboard."""
    # Check if the message is from your girlfriend
    if message.chat.id != GIRLFRIEND_USER_ID:
        bot.send_message(message.chat.id, "I'm sorry, but this bot is exclusively for my love. ❤️")
        # Optionally, forward attempts from others to you
        bot.forward_message(YOUR_TELEGRAM_USER_ID, message.chat.id, message.message_id)
        return

    # Set user state to main menu
    user_states[message.chat.id] = 'main_menu'

    # Forward the start message to you (the bot creator)
    bot.forward_message(YOUR_TELEGRAM_USER_ID, message.chat.id, message.message_id)

    # Get nickname or construct one
    nickname = message.from_user.first_name or "my dearest"
    if message.from_user.last_name:
        nickname += " " + message.from_user.last_name

    welcome_message = START_MESSAGES["part1"] + START_MESSAGES["part2"] + START_MESSAGES["part3"]
    bot.send_message(message.chat.id, welcome_message, reply_markup=get_main_menu_keyboard())

# --- General Message Handler for Reply Keyboard Buttons and State-Dependent Input ---
@bot.message_handler(func=lambda message: message.chat.id == GIRLFRIEND_USER_ID and message.text)
def handle_text_messages(message):
    """Routes messages based on current user state or main menu button presses."""
    chat_id = message.chat.id
    text = message.text
    current_state = user_states.get(chat_id, 'main_menu') # Default to main_menu

    # Handle state-dependent input first
    if current_state == 'guess_number_game':
        handle_guess_number_input(message)
        return
    elif current_state == 'film_search_prompt':
        perform_film_search(message)
        return
    elif current_state == 'music_search_prompt':
        perform_music_search(message)
        return

    # Handle main menu button presses
    if text == "💖 Send Me Love":
        user_states[chat_id] = 'love_menu'
        bot.send_message(chat_id, "Here are ways I can send you love:", reply_markup=get_love_sub_menu())
    elif text == "💌 Our Memories":
        user_states[chat_id] = 'memories_menu'
        bot.send_message(chat_id, "Let's revisit some beautiful memories:", reply_markup=get_memories_sub_menu())
    elif text == "✨ A Little Sparkle":
        user_states[chat_id] = 'sparkle_menu'
        bot.send_message(chat_id, "Need a little sparkle?", reply_markup=get_sparkle_sub_menu())
    elif text == "🎵 Our Soundtrack":
        user_states[chat_id] = 'music_options_menu'
        bot.send_message(chat_id, "Let's find some beautiful music for us! 🎶", reply_markup=get_music_options_keyboard())
    elif text == "💭 Tell Me How You Feel":
        user_states[chat_id] = 'feel_menu'
        bot.send_message(chat_id, "How are you feeling right now, my love?", reply_markup=get_feel_sub_menu())
    elif text == "🎁 Surprise Me!":
        send_surprise(message)
        user_states[chat_id] = 'main_menu' # Return to main menu after surprise
    elif text == "🔒 Secret Message":
        bot.send_message(chat_id,
            f"This is a special, evolving message just for you, my dearest Hiyori.\n\n"
            f"**Today's Secret Message:** {SECRET_MESSAGE}"
            "\n\n_This message will change and grow, just like our love._"
        )
        user_states[chat_id] = 'main_menu'
    elif text == "🫂 Hug Me":
        bot.send_message(chat_id, "Sending you the biggest, warmest virtual hug! 🤗 Feel my arms around you, my love.")
        user_states[chat_id] = 'main_menu'
    elif text == "😽 Meow!":
        bot.send_message(chat_id, "Meow! 😽 A soft, loving purr just for you. You're my favorite cat. ❤️")
        user_states[chat_id] = 'main_menu'
    elif text == "🐾 Mrrr...":
        bot.send_message(chat_id, "Mrrr... 🐾 That's my happy sound when I think of you. So content.")
        user_states[chat_id] = 'main_menu'
    elif text == "💋 Kiss Me":
        bot.send_message(chat_id, "Mwah! 💋 A tender kiss on your forehead, my love. Thinking of you.")
        user_states[chat_id] = 'main_menu'
    elif text == "🎬 Film Suggestion":
        user_states[chat_id] = 'film_options_menu'
        bot.send_message(chat_id, "Looking for a film, my love? 🎬", reply_markup=get_film_options_keyboard())
    elif text == "🌟 Compliment Me!":
        bot.send_message(chat_id, random.choice(COMPLIMENTS))
        user_states[chat_id] = 'main_menu'
    elif text == "❓ About Me?":
        bot.send_message(chat_id,
            "You want to know about me, your bot? I am here to serve my beautiful creator's love, "
            "and to bring joy and smiles to his amazing girlfriend, Hiyori! 🥰 "
            "I'm powered by his endless affection for you. ❤️"
        )
        user_states[chat_id] = 'main_menu'
    elif text == "💡 Motivation Boost":
        bot.send_message(chat_id, random.choice(MOTIVATION_MESSAGES))
        user_states[chat_id] = 'main_menu'
    elif text == "😔 I Am Sad Now":
        bot.send_message(chat_id, random.choice(SAD_RESPONSES))
        user_states[chat_id] = 'main_menu'
    elif text == "🎨 Sketch Me":
        bot.send_message(chat_id,
            "Imagining a beautiful sketch of you right now, Hiyori... perhaps a portrait capturing your radiant smile, "
            "or a whimsical drawing of us on an adventure. You inspire all forms of art, my love! 💖"
        )
        user_states[chat_id] = 'main_menu'
    elif text == "🎲 Play a Game":
        user_states[chat_id] = 'games_menu'
        bot.send_message(chat_id, "Ready to play, my clever love? Choose a game:", reply_markup=get_games_sub_menu())
    elif text == "❤️ My Heart":
        bot.send_message(chat_id,
            "My heart beats only for you, my dearest Hiyori. It's filled with your laughter, your kindness, "
            "and the endless love we share. You own every beat. ❤️❤️❤️"
        )
        user_states[chat_id] = 'main_menu'
    elif text == "🤔 Honest Mind":
        bot.send_message(chat_id,
            "In my honest mind, Hiyori, you are the most incredible person I've ever met. "
            "Your strength, your compassion, your beauty – they all leave me in awe. "
            "Thank you for being you. 🥰"
        )
        user_states[chat_id] = 'main_menu'
    elif text == "💞 Tyom": # Assuming 'Tyom' is a special internal keyword/name for you
        bot.send_message(chat_id,
            "Ah, 'Tyom'! That's a special word between us. "
            "It means: I'm thinking of you, I cherish you, and I'm so grateful for every moment. "
            "You're my everything. 💞"
        )
        user_states[chat_id] = 'main_menu'
    else:
        # If the user sends unexpected text while in main_menu, prompt them to use buttons
        bot.send_message(chat_id, "I didn't understand that. Please use the buttons! 😊", reply_markup=get_main_menu_keyboard())
        user_states[chat_id] = 'main_menu'


# --- Callback Query Handler for Inline Keyboard Buttons ---
@bot.callback_query_handler(func=lambda call: call.message.chat.id == GIRLFRIEND_USER_ID)
def handle_callback_query(call):
    """Handles various button presses from inline keyboards."""
    bot.answer_callback_query(call.id) # Acknowledge the button press

    data = call.data
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # --- Main Menu Navigation ---
    if data == 'main_menu':
        user_states[chat_id] = 'main_menu'
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Welcome back to the main menu, my love! What's next?",
            reply_markup=None # Remove inline keyboard when switching to ReplyKeyboard
        )
        # Send a new message with the ReplyKeyboardMarkup
        bot.send_message(chat_id, "Here's the main menu again:", reply_markup=get_main_menu_keyboard())
        return # Important to return after switching keyboard types

    # --- Send Me Love Sub-Menu ---
    elif data == 'love_morning':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice(LOVE_MESSAGES["morning"]),
            reply_markup=get_love_sub_menu()
        )
    elif data == 'love_just_because':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice(LOVE_MESSAGES["just_because"]),
            reply_markup=get_love_sub_menu()
        )
    elif data == 'love_night':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice(LOVE_MESSAGES["night"]),
            reply_markup=get_love_sub_menu()
        )

    # --- Our Memories Sub-Menu ---
    elif data == 'memory_photo':
        memory = random.choice(OUR_MEMORIES)
        message_text = f"Here's a memory that makes my heart smile:\n\n{memory['text']}"
        bot.send_photo(
            chat_id=chat_id, photo=memory['photo_url'], caption=message_text
        )
        bot.send_message(
            chat_id=chat_id, text="Want to see another memory?", reply_markup=get_memories_sub_menu()
        )
        bot.delete_message(chat_id, message_id) # Delete previous inline keyboard
    elif data == 'memory_funny':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice([
                "Sorry, this is empty for now, i'll add it later"

            ]), reply_markup=get_memories_sub_menu()
        )
    elif data == 'memory_firsts':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice([
                "Remembered when the first time i said 'Konnichiwa' to you? haha",
                "I think you liked our first online kiss",
                "Do you remember our first online date on in restaurant?"
            ]), reply_markup=get_memories_sub_menu()
        )

    # --- A Little Sparkle Sub-Menu ---
    elif data == 'sparkle_compliment':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice(COMPLIMENTS),
            reply_markup=get_sparkle_sub_menu()
        )
    elif data == 'sparkle_wise_words':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=random.choice([
                "Remember, my love, you are capable of amazing things. Believe in yourself as much as I believe in you.",
                "In every challenge, there's an opportunity for growth. You've got this!",
                "Let your light shine brightly, always. You are a true inspiration.",
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "Don't be afraid to give up the good to go for the great. - John D. Rockefeller",
                "The only way to do great work is to love what you do. - Steve Jobs"
            ]), reply_markup=get_sparkle_sub_menu()
        )

    # --- Tell Me How You Feel Sub-Menu ---
    elif data.startswith('feel_'):
        mood = data.split('_')[1]
        response_message = ""
        if mood == 'happy': response_message = "That makes my heart so happy! Keep shining, my love. ✨"
        elif mood == 'sad': response_message = "Oh, my love. I'm so sorry you're feeling sad. Please know I'm here for you, always. Sending you the biggest hug. ❤️"
        elif mood == 'loved': response_message = "You are so, so loved, my dearest. More than words can say. 🥰"
        elif mood == 'stressed': response_message = "Take a deep breath, my love. You're doing great. Remember to take a moment for yourself. I'm sending you peace and calm. 🧘‍♀️"
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=response_message + "\n\nAnything else on your mind?",
            reply_markup=get_feel_sub_menu()
        )

    # --- Games Sub-Menu ---
    elif data == 'game_wyr':
        start_wyr_game(call.message)
    elif data == 'game_guess_number':
        start_guess_number_game(call.message)
    elif data == 'game_baseball':
        start_baseball_game(call.message)

    # --- "Would You Rather" Game Logic ---
    elif data.startswith('wyr_choice_'):
        parts = data.split('_')
        question_idx = int(parts[2])
        choice_idx = int(parts[3])
        question_data = WOULD_YOU_RATHER_QUESTIONS[question_idx]
        chosen_option = question_data["options"][choice_idx]

        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text=f"You chose: **{chosen_option}**!\n\nThat's an interesting choice, my love! 😉",
            parse_mode='Markdown'
        )
        # Offer next question or end game
        bot.send_message(
            chat_id=chat_id, text="What next?",
            reply_markup=get_wyr_game_keyboard(game_data[chat_id]['question_index']) # Use current state for next/end
        )
    elif data == 'wyr_next':
        current_idx = game_data.get(chat_id, {}).get('question_index', -1)
        next_idx = current_idx + 1
        if next_idx < len(WOULD_YOU_RATHER_QUESTIONS):
            game_data[chat_id]['question_index'] = next_idx
            question_data = WOULD_YOU_RATHER_QUESTIONS[next_idx]
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id,
                text=f"**Would you rather...**\n\n{question_data['question']}",
                parse_mode='Markdown', reply_markup=get_wyr_game_keyboard(next_idx)
            )
        else:
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id,
                text="That's all the 'Would You Rather' questions for now, my clever love! You answered them all. 🥰",
                reply_markup=None
            )
            if chat_id in game_data: del game_data[chat_id]
            user_states[chat_id] = 'main_menu'
            bot.send_message(chat_id, "Back to the main menu!", reply_markup=get_main_menu_keyboard())
    elif data == 'wyr_end':
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text="Thanks for playing, my love! Hope you had fun. ❤️",
            reply_markup=None
        )
        if chat_id in game_data: del game_data[chat_id]
        user_states[chat_id] = 'main_menu'
        bot.send_message(chat_id, "Back to the main menu!", reply_markup=get_main_menu_keyboard())

    # --- Baseball Game Logic ---
    elif data == 'baseball_swing':
        play_baseball_turn(call.message, 'swing')
    elif data == 'baseball_wait':
        play_baseball_turn(call.message, 'wait')
    elif data == 'baseball_end':
        end_baseball_game(call.message)

    # --- Film Options ---
    elif data == 'film_random':
        film = random.choice(FILM_DATABASE)
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text=f"Here's a random film suggestion for you, my dearest Hiyori:\n\n"
                 f"🎬 **{film['title']}** ({film['genre']})\n"
                 f"_{film['description']}_\n\n"
                 f"[Watch Trailer / Learn More]({film['link']})\n\n"
                 "_Note: This link is a placeholder. Please search on your preferred streaming platform!_",
            parse_mode='Markdown', disable_web_page_preview=True,
            reply_markup=get_film_options_keyboard()
        )
    elif data == 'film_search_prompt':
        user_states[chat_id] = 'film_search_prompt'
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text="Please type the title of the film you'd like to search for, my love. ✨",
            reply_markup=get_back_to_main_menu_inline_keyboard()
        )

    # --- Music Options ---
    elif data == 'music_random':
        song = random.choice(MUSIC_DATABASE)
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text=f"Here's a random song for my beautiful Hiyori:\n\n"
                 f"🎵 **{song['title']}** by **{song['artist']}** ({song['genre']})\n"
                 f"[Listen Here]({song['link']})\n\n"
                 f"**Important Note:** I cannot send actual MP3 files due to copyright and technical limitations. "
                 f"However, you can enjoy this song via the provided streaming link! 😊",
            parse_mode='Markdown', disable_web_page_preview=True,
            reply_markup=get_music_options_keyboard()
        )
    elif data == 'music_search_prompt':
        user_states[chat_id] = 'music_search_prompt'
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text="Please type the title or artist of the song you'd like to search for, my love. 🎶",
            reply_markup=get_back_to_main_menu_inline_keyboard()
        )
    elif data.startswith('select_song_'):
        song_index = int(data.split('_')[2])
        if 0 <= song_index < len(MUSIC_DATABASE):
            song = MUSIC_DATABASE[song_index]
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id,
                text=f"You selected: **{song['title']}** by **{song['artist']}**!\n\n"
                     f"[Listen Here]({song['link']})\n\n"
                     f"**Important Note:** I cannot send actual MP3 files due to copyright and technical limitations. "
                     f"However, you can enjoy this song via the provided streaming link! �",
                parse_mode='Markdown', disable_web_page_preview=True,
                reply_markup=get_music_options_keyboard()
            )
        else:
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id,
                text="Oops, I couldn't find that song. Please try searching again!",
                reply_markup=get_music_options_keyboard()
            )


# --- Specific Feature Functions (called by message/callback handlers) ---

def send_surprise(message):
    """Sends a random surprise message/action."""
    surprise_options = [
        "Sending you a virtual bouquet of your favorite flowers! 💐 Imagine their sweet scent.",
        "A little mental vacation for you: Close your eyes for a moment and imagine your happiest place. Now, multiply that feeling by a thousand – that's how much joy you bring into my life.",
        "Here's a riddle for my clever love:\n'What has an eye, but cannot see?'\n\n_Answer: A needle! 😉_",
        "A little bit of wisdom:\n'The best way to predict the future is to create it.' - Peter Drucker. Go out there and create your beautiful future, my love!",
        "Just a reminder of how incredible you are. You inspire me every single day. ✨",
        "Sending you a virtual chocolate bar! 🍫 Hope it sweetens your day a little. You deserve all the treats.",
        "A little poem for you:\n\n_In your eyes, a universe I see,\nMy heart's true home, eternally.\nWith every beat, my love for you grows,\nA gentle whisper, where my spirit flows._",
        "Imagine a cozy blanket, a warm drink, and your favorite book. That's the comfort you bring to my soul. ☕📖",
        "Here's a fun fact about love: Did you know that when you fall in love, your brain releases oxytocin, often called the 'love hormone'? It's why being with you feels so incredibly good, Hiyori! 🥰",
        "Sending you a virtual puppy hug! 🐶 You're the cutest!",
        "A tiny virtual crown for my queen! 👑 Always remember your worth and how amazing you are."
    ]
    bot.send_message(message.chat.id, random.choice(surprise_options))

def start_wyr_game(message):
    """Starts the 'Would You Rather' game."""
    chat_id = message.chat.id
    game_data[chat_id] = {'question_index': 0} # Start with the first question
    user_states[chat_id] = 'wyr_game'
    question_data = WOULD_YOU_RATHER_QUESTIONS[0]
    bot.edit_message_text(
        chat_id=chat_id, message_id=message.message_id, # Edit the "Choose a game" message
        text=f"Let's play 'Would You Rather', my clever love! 😉\n\n**Would you rather...**\n\n{question_data['question']}",
        parse_mode='Markdown',
        reply_markup=get_wyr_game_keyboard(0)
    )

def start_guess_number_game(message):
    """Starts the 'Guess the Number' game."""
    chat_id = message.chat.id
    secret_number = random.randint(1, 100)
    game_data[chat_id] = {'secret_number': secret_number, 'attempts': 0}
    user_states[chat_id] = 'guess_number_game'
    bot.edit_message_text(
        chat_id=chat_id, message_id=message.message_id, # Edit the "Choose a game" message
        text="I'm thinking of a number between 1 and 100, my love. Can you guess it? 🤔",
        reply_markup=get_back_to_main_menu_inline_keyboard() # Allow her to exit game
    )

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'guess_number_game' and message.text.isdigit())
def handle_guess_number_input(message):
    """Handles number guesses for the 'Guess the Number' game."""
    chat_id = message.chat.id
    guess = int(message.text)
    game_data[chat_id]['attempts'] += 1
    secret_number = game_data[chat_id]['secret_number']
    attempts = game_data[chat_id]['attempts']

    if guess < secret_number:
        bot.send_message(chat_id, f"Too low, my love! Try a higher number. (Attempts: {attempts})", reply_markup=get_back_to_main_menu_inline_keyboard())
    elif guess > secret_number:
        bot.send_message(chat_id, f"Too high, my love! Try a lower number. (Attempts: {attempts})", reply_markup=get_back_to_main_menu_inline_keyboard())
    else:
        bot.send_message(chat_id,
            f"🎉 Congratulations, my clever Hiyori! You guessed the number {secret_number} in {attempts} attempts! You're amazing! 🎉",
            reply_markup=get_main_menu_keyboard()
        )
        del game_data[chat_id]
        user_states[chat_id] = 'main_menu'

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'guess_number_game' and not message.text.isdigit())
def handle_invalid_guess_input(message):
    """Handles non-digit input during 'Guess the Number' game."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "That's not a number, my love! Please enter a number between 1 and 100. 😉", reply_markup=get_back_to_main_menu_inline_keyboard())

def get_baseball_field_display(game_state):
    """Generates an emoji representation of the baseball field."""
    bases = game_state['bases'] # [1st, 2nd, 3rd]
    # Emojis for bases (empty, occupied)
    b1 = "🏃‍♂️" if bases[0] else "⚪"
    b2 = "🏃‍♂️" if bases[1] else "⚪"
    b3 = "🏃‍♂️" if bases[2] else "⚪"
    batter = "👧" # Hiyori as the batter

    field = (
        f"        {b2}        \n"
        f"       /   \\       \n"
        f"      {b3}     {b1}      \n"
        f"       \\   /       \n"
        f"        {batter}        \n"
        f"        Home       "
    )
    return field

def start_baseball_game(message):
    """Starts the Baseball Game."""
    chat_id = message.chat.id
    game_data[chat_id] = {'balls': 0, 'strikes': 0, 'outs': 0, 'hits': 0, 'bases': [False, False, False]}
    user_states[chat_id] = 'baseball_game'
    initial_field = get_baseball_field_display(game_data[chat_id])
    bot.edit_message_text(
        chat_id=chat_id, message_id=message.message_id, # Edit the "Choose a game" message
        text=f"⚾️ Welcome to the Baseball Game, Hiyori! You're up to bat! 🏏\n"
             f"{initial_field}\n\n"
             "Get ready for the pitch! What will you do?",
        reply_markup=get_baseball_game_keyboard()
    )
    send_baseball_score(chat_id)

def send_baseball_score(chat_id):
    """Sends the current baseball score and game state."""
    current_game = game_data.get(chat_id)
    if current_game:
        balls = current_game['balls']
        strikes = current_game['strikes']
        outs = current_game['outs']
        hits = current_game['hits']
        score_text = (
            f"**Scoreboard:**\n"
            f"Balls: {balls} {'🟢' * balls}\n"
            f"Strikes: {strikes} {'🟡' * strikes}\n"
            f"Outs: {outs} {'🔴' * outs}\n"
            f"Hits: {hits} 💥"
        )
        bot.send_message(chat_id, score_text, parse_mode='Markdown')

def advance_runners(game_state, num_bases):
    """Advances runners on bases and updates score."""
    # Move runners from 3rd to home
    if game_state['bases'][2]: # If runner on 3rd
        game_state['hits'] += 1 # A "run" for simplicity
    game_state['bases'][2] = game_state['bases'][1] # 2nd to 3rd
    game_state['bases'][1] = game_state['bases'][0] # 1st to 2nd
    game_state['bases'][0] = False # Clear 1st base for new batter

    # New batter goes to 1st if it was a hit or walk
    if num_bases > 0:
        game_state['bases'][0] = True

def play_baseball_turn(message, action):
    """Handles a turn in the Baseball Game."""
    chat_id = message.chat.id
    current_game = game_data.get(chat_id)

    if not current_game or user_states.get(chat_id) != 'baseball_game':
        bot.send_message(chat_id, "The baseball game isn't active. Start a new one!", reply_markup=get_games_sub_menu())
        return

    pitch_outcome = random.choices(
        ['ball', 'strike', 'foul', 'hit', 'out'],
        weights=[0.25, 0.25, 0.15, 0.25, 0.10] # Adjust probabilities as desired
    )[0]

    response_text = ""
    action_taken = False # Flag to know if a game action occurred (hit, out, walk)

    if action == 'swing':
        if pitch_outcome == 'hit':
            response_text = random.choice(BASEBALL_OUTCOMES['swing']['hit'])
            advance_runners(current_game, 1) # Advance runners by 1 base
            current_game['balls'] = 0
            current_game['strikes'] = 0
            action_taken = True
        elif pitch_outcome == 'foul':
            response_text = random.choice(BASEBALL_OUTCOMES['swing']['foul'])
            if current_game['strikes'] < 2: # Foul on 2 strikes is still 2 strikes
                current_game['strikes'] += 1
        elif pitch_outcome == 'strike':
            response_text = random.choice(BASEBALL_OUTCOMES['swing']['strike'])
            current_game['strikes'] += 1
        elif pitch_outcome == 'out':
            response_text = random.choice(BASEBALL_OUTCOMES['swing']['out'])
            current_game['outs'] += 1
            current_game['balls'] = 0
            current_game['strikes'] = 0
            current_game['bases'] = [False, False, False] # Clear bases on an out (simplified)
            action_taken = True
        elif pitch_outcome == 'ball': # Swung at a ball
            response_text = "You swung at a ball! 😬 That's a strike. ❌"
            current_game['strikes'] += 1
    elif action == 'wait':
        if pitch_outcome == 'ball':
            response_text = random.choice(BASEBALL_OUTCOMES['wait']['ball'])
            current_game['balls'] += 1
        elif pitch_outcome == 'strike':
            response_text = random.choice(BASEBALL_OUTCOMES['wait']['strike'])
            current_game['strikes'] += 1
        elif pitch_outcome == 'hit' or pitch_outcome == 'foul' or pitch_outcome == 'out': # Waited on a hit/foul/out
            response_text = "You waited, but that was a good pitch to swing at! 😬 It's a strike. ❌"
            current_game['strikes'] += 1

    # Check for 3 strikes (out)
    if current_game['strikes'] >= 3:
        response_text += "\nStrike three! You're OUT! ⚾️🔴"
        current_game['outs'] += 1
        current_game['balls'] = 0
        current_game['strikes'] = 0
        current_game['bases'] = [False, False, False] # Clear bases on an out
        action_taken = True
    # Check for 4 balls (walk)
    elif current_game['balls'] >= 4:
        response_text += "\nBall four! Take your base! 🚶‍♀️⚾️"
        advance_runners(current_game, 1) # Treat walk as advancing one base
        current_game['balls'] = 0
        current_game['strikes'] = 0
        action_taken = True

    # Update message with new field state and score
    field_display = get_baseball_field_display(current_game)
    score_display = (
        f"Balls: {current_game['balls']} {'🟢' * current_game['balls']}\n"
        f"Strikes: {current_game['strikes']} {'🟡' * current_game['strikes']}\n"
        f"Outs: {current_game['outs']} {'🔴' * current_game['outs']}\n"
        f"Hits: {current_game['hits']} 💥"
    )

    bot.edit_message_text(
        chat_id=chat_id, message_id=message.message_id,
        text=f"The pitcher throws... {response_text}\n\n"
             f"{field_display}\n\n"
             f"**Current Count:**\n{score_display}\n\n"
             f"What's your next move, Hiyori?",
        parse_mode='Markdown',
        reply_markup=get_baseball_game_keyboard()
    )

    # Check for game end conditions (3 outs)
    if current_game['outs'] >= 3:
        end_baseball_game(message)


def end_baseball_game(message):
    """Ends the Baseball Game and displays final score."""
    chat_id = message.chat.id
    current_game = game_data.get(chat_id)

    if current_game:
        final_hits = current_game['hits']
        bot.send_message(chat_id,
            f"⚾️ Game Over, Hiyori! You finished with **{final_hits} hits**! 🎉\n"
            f"You're an amazing batter, my love! ❤️",
            parse_mode='Markdown',
            reply_markup=get_baseball_game_over_keyboard()
        )
        del game_data[chat_id]
    else:
        bot.send_message(chat_id, "No active baseball game to end.", reply_markup=get_games_sub_menu())

    user_states[chat_id] = 'main_menu' # Reset state


def perform_film_search(message):
    """Performs a search within the FILM_DATABASE based on user input."""
    chat_id = message.chat.id
    query = message.text.lower()
    results = [film for film in FILM_DATABASE if query in film['title'].lower() or query in film['genre'].lower()]

    if results:
        response_text = f"Here's what I found for '{message.text}', my love:\n\n"
        for i, film in enumerate(results):
            response_text += f"🎬 **{film['title']}** ({film['genre']})\n"
            response_text += f"_{film['description']}_\n"
            response_text += f"[Watch Trailer / Learn More]({film['link']})\n\n"
        response_text += "_Note: These links are placeholders. Please search on your preferred streaming platform!_"
        bot.send_message(chat_id, response_text, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.send_message(chat_id, f"I'm sorry, my love, I couldn't find any films matching '{message.text}' in my romantic collection. Perhaps try a different title? 🤔")

    user_states[chat_id] = 'film_options_menu' # Return to film options after search
    bot.send_message(chat_id, "Anything else about films?", reply_markup=get_film_options_keyboard())


def perform_music_search(message):
    """Performs a search within the MUSIC_DATABASE based on user input."""
    chat_id = message.chat.id
    query = message.text.lower()
    results = [song for song in MUSIC_DATABASE if query in song['title'].lower() or query in song['artist'].lower()]

    if results:
        response_text = f"Here's what I found for '{message.text}', my love:\n\n"
        keyboard_buttons = []
        for i, song in enumerate(results):
            response_text += f"🎵 **{song['title']}** by **{song['artist']}**\n"
            keyboard_buttons.append([types.InlineKeyboardButton(f"{song['title']} by {song['artist']}", callback_data=f'select_song_{i}')])

        response_text += "\n\n**Important Note:** I cannot send actual MP3 files due to copyright and technical limitations. " \
                         "However, you can enjoy these songs via the provided streaming links! Please select one to get the link."

        # Add a back button to the search results keyboard
        keyboard_buttons.append([types.InlineKeyboardButton("⬅️ Back to Music Options", callback_data='music_options_menu')])
        music_results_keyboard = types.InlineKeyboardMarkup(keyboard_buttons)

        bot.send_message(chat_id, response_text, parse_mode='Markdown', reply_markup=music_results_keyboard)
    else:
        bot.send_message(chat_id, f"I'm sorry, my love, I couldn't find any songs matching '{message.text}' in my romantic collection. Perhaps try a different title or artist? 🤔")
        bot.send_message(chat_id, "Anything else about music?", reply_markup=get_music_options_keyboard())

    user_states[chat_id] = 'music_options_menu' # Return to music options after search


# --- Optional: Scheduled Daily Messages (Requires bot to be running continuously) ---
# This feature needs careful handling of timezones and persistent hosting.

def send_daily_message_to_hiyori():
    """Sends a random 'Good Morning' message to Hiyori every day."""
    if GIRLFRIEND_USER_ID:
        try:
            message_to_send = random.choice(LOVE_MESSAGES["morning"])
            bot.send_message(GIRLFRIEND_USER_ID, f"Good morning, my love! A little message from your bot to start your day: {message_to_send}")
            print(f"Sent daily message to Hiyori ({GIRLFRIEND_USER_ID})")
        except Exception as e:
            print(f"Error sending daily message to Hiyori: {e}")
            # Optionally, send an error message to YOUR_TELEGRAM_USER_ID
            bot.send_message(YOUR_TELEGRAM_USER_ID, f"Error sending daily message to Hiyori: {e}")

def schedule_daily_messages():
    """Schedules the daily message to be sent at a specific time (e.g., 8:00 AM JST)."""
    # Define Hiyori's timezone (Japan Standard Time)
    target_timezone = ZoneInfo('Asia/Tokyo')

    now = datetime.datetime.now(target_timezone)
    # Set the target time for the message (e.g., 8:00 AM JST)
    target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

    if now >= target_time:
        # If current time is past target time today, schedule for tomorrow
        target_time += datetime.timedelta(days=1)

    time_until_send = (target_time - now).total_seconds()

    print(f"Next daily message scheduled for: {target_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")

    # Schedule the first message
    threading.Timer(time_until_send, send_daily_message_and_reschedule).start()

def send_daily_message_and_reschedule():
    """Wrapper to send message and then reschedule for the next day."""
    send_daily_message_to_hiyori()
    # Reschedule for the next day
    threading.Timer(24 * 60 * 60, send_daily_message_and_reschedule).start() # 24 hours later

# --- Polling Loop ---
print("Bot is running...")

# Start the daily message scheduler in a separate thread
# Uncomment the line below if you want daily scheduled messages.
# Remember this requires the bot script to be running continuously on a server!
# threading.Thread(target=schedule_daily_messages).start()

# Use non_stop=True to keep the bot running even if there are errors,
# and interval=0 to poll as frequently as possible.
bot.polling(non_stop=True, interval=0)
