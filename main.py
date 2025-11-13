from telegram import Update
from telegram.ext import ContextTypes
subscribers = set()
user_notifications = {}

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subscribers.add(user_id)
    await update.message.reply_text("You are now subscribed to notifications!")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subscribers.discard(user_id)
    await update.message.reply_text("You have unsubscribed from notifications.")

async def notifyme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Usage: /notifyme [movie name]")
        return
    movie_name = ' '.join(context.args).strip().lower()
    user_notifications.setdefault(user_id, set()).add(movie_name)
    await update.message.reply_text(f"You will be notified when '{movie_name.title()}' is added.")

async def remindme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /remindme [movie name] [time]")
        return
    movie_name = ' '.join(context.args[:-1]).strip().lower()
    remind_time = context.args[-1]
    await update.message.reply_text(f"Reminder set for '{movie_name.title()}' at {remind_time} (feature coming soon)")
import os
import json
from telegram import Update
from telegram.ext import ContextTypes
RATINGS_FILE = "movie_ratings.json"
def load_ratings():
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_ratings(ratings):
    with open(RATINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(ratings, f, ensure_ascii=False, indent=2)

movie_ratings = load_ratings()

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /rate [movie name] [1-5]")
        return
    movie_name = ' '.join(context.args[:-1]).strip().lower()
    rating_str = context.args[-1]
    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Rating must be a number from 1 to 5.")
        return
    user_id = str(update.effective_user.id)
    if movie_name not in movie_files:
        await update.message.reply_text("Movie not found. Please check the name.")
        return
    if movie_name not in movie_ratings:
        movie_ratings[movie_name] = {}
    movie_ratings[movie_name][user_id] = rating
    save_ratings(movie_ratings)
    ratings = list(movie_ratings[movie_name].values())
    avg = sum(ratings) / len(ratings)
    await update.message.reply_text(f"Your rating has been saved!\nCurrent average for '{movie_name.title()}': {avg:.2f} ⭐ ({len(ratings)} ratings)")

async def show_rating_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /showrating [movie name]")
        return
    movie_name = ' '.join(context.args).strip().lower()
    if movie_name not in movie_ratings or not movie_ratings[movie_name]:
        await update.message.reply_text("No ratings yet for this movie.")
        return
    ratings = list(movie_ratings[movie_name].values())
    avg = sum(ratings) / len(ratings)
    await update.message.reply_text(f"Average rating for '{movie_name.title()}': {avg:.2f} ⭐ ({len(ratings)} ratings)")

async def topmovies_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Load ratings and downloads data
    try:
        ratings = load_json('movie_ratings.json') if os.path.exists('movie_ratings.json') else {}
        movie_files = load_json('movie_files.json') if os.path.exists('movie_files.json') else {}
    except Exception:
        ratings = {}
        movie_files = {}
    # Aggregate top-rated movies
    top_rated = sorted(ratings.items(), key=lambda x: sum(x[1].values())/len(x[1]) if x[1] else 0, reverse=True)[:10]
    top_downloaded = sorted(movie_files.items(), key=lambda x: x[1].get('downloads', 0), reverse=True)[:10]
    msg = "\U0001F3AC Top Movies\n"
    if top_rated:
        msg += "\nTop Rated:\n"
        for i, (movie, data) in enumerate(top_rated, 1):
            avg = sum(data.values())/len(data) if data else 0
            msg += f"{i}. {movie.title()} - {avg:.2f}/5\n"
    if top_downloaded:
        msg += "\nMost Downloaded:\n"
        for i, (movie, data) in enumerate(top_downloaded, 1):
            downloads = data.get('downloads', 0)
            msg += f"{i}. {movie.title()} - {downloads} downloads\n"
    if not top_rated and not top_downloaded:
        msg += "No movie ratings or downloads found yet."
    await update.message.reply_text(msg)

async def topusers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example: show most active users by number of ratings
    try:
        ratings = load_json('movie_ratings.json') if os.path.exists('movie_ratings.json') else {}
    except Exception:
        ratings = {}
    user_activity = {}
    for movie, user_ratings in ratings.items():
        for user_id in user_ratings:
            user_activity[user_id] = user_activity.get(user_id, 0) + 1
    top_users = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:10]
    msg = "\U0001F464 Top Users\n"
    if top_users:
        for i, (user_id, count) in enumerate(top_users, 1):
            msg += f"{i}. User {user_id} - {count} ratings\n"
    else:
        msg += "No user activity found yet."
    await update.message.reply_text(msg)

async def analytics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example: show bot usage statistics
    try:
        ratings = load_json('movie_ratings.json') if os.path.exists('movie_ratings.json') else {}
        movie_files = load_json('movie_files.json') if os.path.exists('movie_files.json') else {}
    except Exception:
        ratings = {}
        movie_files = {}
    total_movies = len(movie_files)
    total_ratings = sum(len(r) for r in ratings.values())
    total_downloads = sum(f.get('downloads', 0) for f in movie_files.values())
    msg = (f"\U0001F4CA Bot Analytics\n"
           f"Total movies: {total_movies}\n"
           f"Total ratings: {total_ratings}\n"
           f"Total downloads: {total_downloads}\n")
    await update.message.reply_text(msg)
from typing import Final
from telegram import (
    Update,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedDocument,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import re
import uuid
from telegram import (
    Update,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedDocument
)
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    ContextTypes
)

from telegram.ext import InlineQueryHandler

from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, InlineQueryHandler
)
import random
from datetime import datetime
import json
import os
import urllib.parse
import re
import asyncio
from typing import Final
BOT_VERSION = "1.0"
# If a local .env file exists, load it (simple KEY=VALUE parser). This helps local/dev runs.
try:
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith('#'):
                    continue
                if '=' not in ln:
                    continue
                k, v = ln.split('=', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
except Exception as _e:
    print(f"Warning: failed to read .env file: {_e}")

# Read the bot token from environment for safety. Do not keep tokens in source control.
def _find_token_in_env():
    """Find a Telegram bot token from common env names or any value that matches the token pattern.

    Preference order:
    1. TELEGRAM_BOT_TOKEN
    2. BOT_TOKEN, TELEGRAM_TOKEN, TOKEN
    3. Any environment value that matches the Telegram token regular expression
    """
    # explicit common names
    for name in ("TELEGRAM_BOT_TOKEN", "BOT_TOKEN", "TELEGRAM_TOKEN", "TOKEN"):
        v = os.environ.get(name)
        if v:
            return v
    # fallback: search any env value that looks like a Telegram bot token
    token_pattern = re.compile(r'^\d{6,}:[A-Za-z0-9_\-]{20,}$')
    for k, v in os.environ.items():
        if isinstance(v, str) and token_pattern.match(v):
            return v
    return None

TOKEN: Final = _find_token_in_env()
if TOKEN:
    # canonicalize the variable so other code can inspect TELEGRAM_BOT_TOKEN
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", TOKEN)
else:
    print("ERROR: TELEGRAM_BOT_TOKEN environment variable is not set. Exiting.")
    import sys
    sys.exit(1)
BOT_USERNAME: Final = '@asamflixstreambot'
ADMIN_IDS = {8221911290, 7235130481}
CHANNEL_ID = {-1003158591242, -1003192209387}
GROUP_ID = {-1003192207003,  -1003156900504}

# External API integrations (TMDB/YTS) removed — the bot will provide a safe web search link instead

RESPONSES_FILE = "learned_responses.json"
MOVIE_FILES = "movie_files.json"
WARNINGS_FILE = "warnings.json"
BLOCKED_FILE = "blocked.json"
SCHEDULE_FILE = "schedule.json"

user_waiting_for_movie = {}
pending_genre_upload = {}
GENRES = [
    "action", "comedy", "romance", "horror", "scifi", "drama", "animation",
    "thriller", "documentary", "series", "anime", "adventure", "fantasy",
    "crime", "family", "mystery", "others"
]

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

learned_responses = load_json(RESPONSES_FILE)
movie_files = load_json(MOVIE_FILES)
warnings = load_json(WARNINGS_FILE)
blocked = set(load_json(BLOCKED_FILE))
schedule = load_json(SCHEDULE_FILE)

def save_learned_responses(responses): save_json(RESPONSES_FILE, responses)
def save_movie_files(files): save_json(MOVIE_FILES, files)
def save_warnings(warn): save_json(WARNINGS_FILE, warn)
def save_blocked(blocked_set): save_json(BLOCKED_FILE, list(blocked_set))
def save_schedule(sched): save_json(SCHEDULE_FILE, sched)

def format_size(size_bytes):
    if size_bytes is None:
        return ""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024


async def send_media(chat_targets, file_type, file_id, caption, bot, reply_markup=None):
    """Send a video/document to one or multiple chat targets.
    Accepts a single chat id (int/str) or an iterable (list/set/tuple) of ids.
    This prevents crashes when CHANNEL_ID/GROUP_ID are stored as collections.
    """
    # Normalize to list
    if isinstance(chat_targets, (set, tuple)):
        targets = list(chat_targets)
    elif isinstance(chat_targets, list):
        targets = chat_targets
    else:
        targets = [chat_targets]

    for ch in targets:
        try:
            if file_type == "video":
                await bot.send_video(ch, file_id, caption=caption, reply_markup=reply_markup)
            else:
                # treat subtitles and others as documents
                await bot.send_document(ch, file_id, caption=caption, reply_markup=reply_markup)
        except Exception as e:
            print(f"Failed to send to {ch}: {e}")

async def fetch_tmdb_info(query):
    """TMDB integration removed — always return None so callers fall back to a search link."""
    return None

async def search_yts_movie(query: str) -> str:
    """YTS integration removed — return a safe web search URL for the movie instead of doing network calls."""
    return f"https://www.google.com/search?q={urllib.parse.quote(query + ' movie')}"

def clean_movie_filename(filename):
    filename = re.sub(r'@imdb\.?', '', filename, flags=re.IGNORECASE)
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[\._]+', ' ', name)
    match = re.search(r'(\d{4})', name)
    year = match.group(1) if match else ''
    if year: name = name.replace(year, '').strip()
    name = ' '.join(word.capitalize() for word in name.split())
    new_filename = f"{name} {year}{ext}" if year else f"{name}{ext}"
    return new_filename.strip()


def normalize_for_search(text: str) -> str:
    """Normalize text for robust matching: lowercase, remove non-alphanumerics, collapse spaces."""
    if not text:
        return ""
    txt = text.lower()
    # keep letters, numbers and spaces
    txt = re.sub(r'[^a-z0-9\s]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

async def movie_to_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if not CHANNEL_ID:
        await update.message.reply_text("CHANNEL_ID is not set.")
        return
    if context.args:
        movie_name = ' '.join(context.args).strip().lower()
        matches = []
        for title, file_info in movie_files.items():
            if movie_name.replace(" ", "") in title.replace(" ", ""):
                matches.append((title, file_info))
        if matches:
            matches.sort()
            for title, file_info in matches:
                file_id = file_info["file_id"]
                file_type = file_info.get("file_type", "video")
                description = file_info.get("description", "")
                poster_url = file_info.get("poster_url", "")
                file_size = file_info.get("file_size")
                size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
                caption = title.title() + size_str
                if description:
                    caption += f"\n\n{description}"
                if poster_url:
                    caption += f"\n\nPoster: {poster_url}"
                try:
                    await send_media(CHANNEL_ID, file_type, file_id, caption, context.bot)
                except Exception as e:
                    print(f"Failed to send {title} to channel: {e}")
            await update.message.reply_text(f"Sent {len(matches)} files to the channel.")
        else:
            await update.message.reply_text("No matching movies found.")
    else:
        await update.message.reply_text("Please type a movie name.\nExample: /movie_to_channel avatar")

async def movie_to_group_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if not GROUP_ID:
        await update.message.reply_text("GROUP_ID is not set.")
        return
    if context.args:
        movie_name = ' '.join(context.args).strip().lower()
        matches = []
        for title, file_info in movie_files.items():
            if movie_name.replace(" ", "") in title.replace(" ", ""):
                matches.append((title, file_info))
        if matches:
            matches.sort()
            for title, file_info in matches:
                file_id = file_info["file_id"]
                file_type = file_info.get("file_type", "video")
                description = file_info.get("description", "")
                poster_url = file_info.get("poster_url", "")
                file_size = file_info.get("file_size")
                size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
                caption = title.title() + size_str
                if description:
                    caption += f"\n\n{description}"
                if poster_url:
                    caption += f"\n\nPoster: {poster_url}"
                try:
                    await send_media(GROUP_ID, file_type, file_id, caption, context.bot)
                except Exception as e:
                    print(f"Failed to send {title} to group: {e}")
            await update.message.reply_text(f"Sent {len(matches)} files to the group.")
        else:
            await update.message.reply_text("No matching movies found.")
    else:
        await update.message.reply_text("Please type a movie name.\nExample: /movie_to_group avatar")

# --- Inline Buttons Helper ---
async def get_inline_buttons(title):
    buttons = []
    yts_link = await search_yts_movie(title)
    tmdb = await fetch_tmdb_info(title)
    if tmdb and tmdb.get("poster_url"):
        buttons.append([InlineKeyboardButton("More Info", url=tmdb["poster_url"])])
    else:
        buttons.append([InlineKeyboardButton("More Info", url=yts_link)])
    # Download Subtitle button if subtitle exists
    subtitle_title = None
    for t, f in movie_files.items():
        if t.startswith(title) and f.get("file_type") == "subtitle":
            subtitle_title = t
            break
    if subtitle_title:
        buttons.append([InlineKeyboardButton("Download Subtitle", switch_inline_query=subtitle_title)])
    # Always add Search Again button for every movie
    buttons.append([InlineKeyboardButton("Search Again", switch_inline_query=title)])
    return InlineKeyboardMarkup(buttons) if buttons else None

# ─── handlers/inline_result_handler.py ───
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def chosen_inline_result_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.chosen_inline_result.query

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Search Again", switch_inline_query=query)]
    ])

    try:
        await context.bot.send_message(
            chat_id=update.chosen_inline_result.from_user.id,
            text=f"🔎 Search again for \"{query}\" or change the episode number.",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error sending search again: {e}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        return
    file = update.message.document or update.message.video
    if not file:
        await update.message.reply_text("Unsupported file type. Please send as document or video.")
        return
    genre = pending_genre_upload.pop(user_id, None)
    original_name = (file.file_name or "unnamed_movie").lower()
    movie_name = clean_movie_filename(original_name).lower()
    subtitle_exts = ['.srt', '.ass', '.vtt']
    is_subtitle = any(movie_name.endswith(ext) for ext in subtitle_exts)
    movie_files[movie_name] = {
        "file_id": file.file_id,
        "file_type": 'subtitle' if is_subtitle else ('video' if update.message.video else 'document'),
        "description": "",
        "poster_url": "",
        "genre": genre,
        "file_size": getattr(file, "file_size", None),
        "downloads": 0
    }
    save_movie_files(movie_files)
    if genre:
        await update.message.reply_text(f"File '{movie_name.title()}' saved to genre '{genre.title()}'!")
    else:
        await update.message.reply_text(f"File '{movie_name.title()}' saved!")

async def search_movies_with_filters(keyword, filters):
    # This would pull from an API or your DB
    sample = [
        {"title": f"{keyword} Thriller Ep1", "episode": 1, "genre": "thriller", "resolution": "1080p"},
        {"title": f"{keyword} Thriller Ep2", "episode": 2, "genre": "thriller", "resolution": "720p"},
    ]
    # Filter locally for now
    return [
        movie for movie in sample
        if (not filters["genre"] or movie["genre"] == filters["genre"]) and
           (not filters["resolution"] or movie["resolution"] == filters["resolution"])
    ]

#inline_query command

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Accept queries that are empty or only spaces
    raw_query = update.inline_query.query
    query = raw_query.lower().strip()
    results = []

    # Extract dynamic limit from query string
    limit_match = re.search(r"limit=(\d+)", query)
    max_results = int(limit_match.group(1)) if limit_match else 40

    # Clean query by removing the limit part
    query = re.sub(r"limit=\d+", "", query).strip()

    count = 0
    # If query is empty, only spaces, or only one character, show all movies
    show_all = not query
    for title, file_info in movie_files.items():
        title_lower = title.lower()
        match = show_all or query in title_lower
        if match:
            downloads = file_info.get("downloads", 0)
            file_id = file_info["file_id"]
            file_type = file_info.get("file_type", "video")
            description = file_info.get("description", "")
            poster_url = file_info.get("poster_url", "")
            file_size = file_info.get("file_size")
            resolution = file_info.get("resolution", "")
            genre = file_info.get("genre", "")

            # Build display strings
            size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
            downloads_str = f"\nDownloads: {downloads}" if downloads else ""
            resolution_str = f"\nResolution: {resolution}" if resolution else ""
            genre_str = f"\nGenre: {genre}" if genre else ""

            caption = f"{title.title()}{size_str}{downloads_str}{resolution_str}{genre_str}"
            if description:
                caption += f"\n\n{description}"
            if poster_url:
                caption += f"\n\nPoster: {poster_url}"

            display_title = title.title()
            if file_size and resolution:
                display_title += f" ({format_size(file_size)}, {resolution})"
            elif file_size:
                display_title += f" ({format_size(file_size)})"

            result_id = str(uuid.uuid4())

            if file_type == "video":
                results.append(
                    InlineQueryResultCachedVideo(
                        id=result_id,
                        video_file_id=file_id,
                        title=display_title,
                        caption=caption
                    )
                )
            else:
                results.append(
                    InlineQueryResultCachedDocument(
                        id=result_id,
                        document_file_id=file_id,
                        title=display_title,
                        caption=caption
                    )
                )

            count += 1
            if count >= max_results:
                break

    await update.inline_query.answer(results, cache_time=0, is_personal=True)

async def notify_admins_of_request(context, user, movie_name):
    """
    Notify admins about a movie request.
    """
    message = (
        f"📩 <b>New Movie Request:</b>\n"
        f"User: {user.full_name} (ID: {user.id})\n"
        f"Requested Movie: <code>{movie_name.title()}</code>\n\n"
        "Reply with /approve to upload this movie."
    )
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(admin_id, message, parse_mode="HTML")
        except Exception as e:
            print(f"Error notifying admin {admin_id}: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    msg = {
        "en": "Hello! I am asamflixstreambot, your personal assistant for streaming content. You can use me to get information about movies, series, and more!\n\nTry /movie Avatar or /action",
        "fr": "Bonjour! Je suis asamflixstreambot, votre assistant personnel pour le streaming. Utilisez-moi pour obtenir des informations sur les films, séries, et plus encore!\n\nEssayez /movie Avatar ou /action"
    }
    await update.message.reply_text(msg.get(lang, msg["en"]))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    if lang == "fr":
        genre_lines = "\n".join([f"/{g} - Films {g.title()}" for g in GENRES])
        msg = (
            "Je suis asamflixstreambot! Voici ce que vous pouvez essayer:\n"
            "/movie [nom] - rechercher ou obtenir un film\n"
            f"{genre_lines}\n"
            "/popular - afficher les films les plus téléchargés\n"
            "Vous pouvez aussi envoyer un fichier film, il sera sauvegardé automatiquement (admin seulement).\n"
            "Ou utilisez-moi en mode inline: @asamflixstreambot nom du film\n"
            "\nPour changer la langue: /setlang en ou /setlang fr"
        )
    else:
        genre_lines = "\n".join([f"/{g} - {g.title()} movies" for g in GENRES])
        msg = (
            "I am asamflixstreambot! Here are some things you can try:\n"
            "/movie [name] - search for a movie or get a movie file\n"
            f"{genre_lines}\n"
            "/popular - show most downloaded movies\n"
            "You can also upload a movie file and it will be saved automatically by file name (admin only).\n"
            "Or use me inline: @asamflixstreambot movie title\n"
            "\nTo change language: /setlang en or /setlang fr"
        )
    await update.message.reply_text(msg)

async def popular_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_movies = sorted(movie_files.items(), key=lambda x: x[1].get("downloads", 0), reverse=True)
    top = sorted_movies[:10]
    if not top or all(x[1].get("downloads", 0) == 0 for x in top):
        await update.message.reply_text("No downloads yet!")
        return
    msg = "🔥 <b>Most Popular Movies:</b>\n"
    for i, (title, info) in enumerate(top, 1):
        msg += f"{i}. {title.title()} — {info.get('downloads', 0)} downloads\n"
    await update.message.reply_text(msg, parse_mode="HTML")

async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        movie_name = ' '.join(context.args).strip().lower()
        matches = []
        for title, file_info in movie_files.items():
            if movie_name.replace(" ", "") in title.replace(" ", ""):
                matches.append((title, file_info))
        if matches:
            matches.sort()
            failed = []
            for title, file_info in matches:
                movie_files[title]["downloads"] = movie_files[title].get("downloads", 0) + 1
                save_movie_files(movie_files)
                downloads = movie_files[title].get("downloads", 0)
                file_id = file_info["file_id"]
                file_type = file_info.get("file_type", "video")
                description = file_info.get("description", "")
                poster_url = file_info.get("poster_url", "")
                file_size = file_info.get("file_size")
                size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
                downloads_str = f"\nDownloads: {downloads}" if downloads else ""
                caption = title.title() + size_str + downloads_str
                if description:
                    caption += f"\n\n{description}"
                if poster_url:
                    caption += f"\n\nPoster: {poster_url}"
                try:
                    if file_type == "video":
                        await update.message.reply_video(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                    elif file_type == "subtitle":
                        await update.message.reply_document(file_id, caption=caption + "\n\n[Subtitle]", reply_markup=await get_inline_buttons(title))
                    else:
                        await update.message.reply_document(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                except Exception as e:
                    print(f"Send file error for {title}: {e}")
                    failed.append((title, str(e)))
                    # continue to next file rather than aborting
                    continue
            if failed:
                msg = f"Sent {len(matches)-len(failed)} files, {len(failed)} failed.\n"
                msg += "Failed files:\n"
                for t, reason in failed:
                    msg += f"- {t}: {reason}\n"
                await update.message.reply_text(msg)
            else:
                await update.message.reply_text(f"Sent {len(matches)} files.")
            return
        yts_link = await search_yts_movie(movie_name)
        tmdb = await fetch_tmdb_info(movie_name)
        if tmdb:
            reply = (
                f"Sorry, I don't have '{movie_name.title()}' in my cloud.\n\n"
                f"🎬 <b>{tmdb['title']} ({tmdb['year']})</b>\n"
                f"⭐ Rating: {tmdb['rating']}\n"
                f"{tmdb['overview']}\n"
                f"{'<a href=\"' + tmdb['poster_url'] + '\">Poster</a>' if tmdb['poster_url'] else ''}\n\n"
                f"🔗 <a href=\"{yts_link}\">YTS/YIFY Torrent</a>"
            )
            await update.message.reply_text(reply, parse_mode="HTML", disable_web_page_preview=False)
        else:
            reply = (
                f"Sorry, I don't have '{movie_name.title()}' in my cloud.\n\n"
                f"🔗 [YTS/YIFY Torrent]({yts_link})"
            )
            await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=False)
        await update.message.reply_text(
            "❓ Would you like to request this movie for upload? Reply 'yes' to confirm.",
        )
        context.user_data["pending_request"] = movie_name
    else:
        await update.message.reply_text("please type a movie name.\nexample: /movie avatar")

async def rename_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    args_joined = ' '.join(context.args)
    if '|' not in args_joined:
        await update.message.reply_text("Usage: /rename old_name | new_name\nExample: /rename the.town.2010.bluray.mkv | The Town 2010 Bluray.mkv")
        return
    old_name, new_name = [x.strip().lower() for x in args_joined.split('|', 1)]
    if old_name not in movie_files:
        await update.message.reply_text(f"Movie '{old_name}' not found.")
        return
    if new_name in movie_files:
        await update.message.reply_text(f"A movie with the name '{new_name}' already exists.")
        return
    movie_files[new_name] = movie_files.pop(old_name)
    save_movie_files(movie_files)
    await update.message.reply_text(f"Renamed '{old_name}' to '{new_name}'.")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.full_name
        await update.message.reply_text(f"Welcome, {name}! 🎉 Enjoy your stay.")

async def warn_and_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if user_id in ADMIN_IDS or user_id in blocked:
        return
    if "http://" in update.message.text or "https://" in update.message.text or "t.me/" in update.message.text:
        warnings[str(user_id)] = warnings.get(str(user_id), 0) + 1
        save_warnings(warnings)
        if warnings[str(user_id)] < 4:
            await update.message.reply_text(
                f"⚠️ Warning {warnings[str(user_id)]}/3: Please do not post links in this group!"
            )
        else:
            blocked.add(user_id)
            save_blocked(blocked)
            await update.message.reply_text(
                "🚫 You have been blocked from the group for repeatedly posting links."
            )
            try:
                await context.bot.ban_chat_member(chat_id, user_id)
            except Exception as e:
                print(f"Error banning user: {e}")

async def unblock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if context.args:
        try:
            user_id = int(context.args[0])
            if user_id in blocked:
                blocked.remove(user_id)
                save_blocked(blocked)
                await update.message.reply_text(f"User {user_id} has been unblocked. You can add them back to the group.")
            else:
                await update.message.reply_text("User is not blocked.")
        except Exception:
            await update.message.reply_text("Usage: /unblock <user_id>")
    else:
        await update.message.reply_text("Usage: /unblock <user_id>")

async def handle_response(text: str) -> str:
    processed_text = text.strip().lower()
    # Get user language from context if available
    user_id = None
    try:
        from telegram import Update
        frame = None
        import inspect
        for f in inspect.stack():
            if 'update' in f.frame.f_locals:
                frame = f.frame
                break
        if frame:
            update = frame.f_locals['update']
            user_id = update.effective_user.id
    except Exception:
        pass
    lang = get_lang(user_id) if user_id else "en"
    # Multi-language responses
    responses = {
        "greeting": {
            "en": ["Hello! 👋 How can I help you today?", "Hi there! 😊 Need a movie recommendation?", "Hey! What would you like to watch?", "Greetings! 🎬", "Howdy! Ready for some movies?", "Hi! Let me know if you want a movie suggestion.", "Hey there! How's your day going?", "Yo! Looking for something to watch?", "Good to see you! 😊"],
            "fr": ["Bonjour! 👋 Comment puis-je vous aider aujourd'hui?", "Salut! 😊 Besoin d'une recommandation de film?", "Hey! Que voulez-vous regarder?", "Salutations! 🎬", "Howdy! Prêt pour des films?", "Salut! Dites-moi si vous voulez une suggestion de film.", "Hey! Comment se passe votre journée?", "Yo! Vous cherchez quelque chose à regarder?", "Ravi de vous voir! 😊"]
        },
        "good_morning": {"en": "Good morning! ☀️ Hope you have a great day. Want a movie to start your morning?", "fr": "Bonjour! ☀️ Passez une excellente journée. Voulez-vous un film pour commencer la matinée?"},
        "good_afternoon": {"en": "Good afternoon! 🌞 Need a movie for your break?", "fr": "Bon après-midi! 🌞 Besoin d'un film pour votre pause?"},
        "good_evening": {"en": "Good evening! 🌙 Ready to relax with a movie?", "fr": "Bonsoir! 🌙 Prêt à vous détendre avec un film?"},
        "how_are_you": {"en": ["I'm doing great, thanks for asking! How about you?", "I'm fantastic! Hope you're having a good day too.", "I'm good! Ready to help you find a movie.", "All good here! What movie are you in the mood for?"], "fr": ["Je vais très bien, merci! Et vous?", "Je suis fantastique! J'espère que vous passez une bonne journée aussi.", "Je vais bien! Prêt à vous aider à trouver un film.", "Tout va bien ici! Quel film voulez-vous regarder?"]},
        "name": {"en": "I'm asamflixstreambot, your friendly movie assistant! 🎬", "fr": "Je suis asamflixstreambot, votre assistant cinéma! 🎬"},
        "thanks": {"en": ["You're welcome! 😊", "No problem at all!", "Anytime! Let me know if you need more movie tips.", "Glad I could help!"], "fr": ["De rien! 😊", "Pas de problème!", "N'importe quand! Dites-moi si vous voulez plus de conseils de films.", "Heureux d'avoir pu aider!"]},
        "bye": {"en": ["Goodbye! Have a great day! 👋", "See you later! Enjoy your movies!", "Bye! Come back anytime for more recommendations.", "Take care! 🎬"], "fr": ["Au revoir! Passez une bonne journée! 👋", "À plus tard! Profitez de vos films!", "Bye! Revenez quand vous voulez pour plus de recommandations.", "Prenez soin de vous! 🎬"]},
        "help": {"en": "I can help you find movies, recommend genres, and chat! Try these:\n- /movie [name] (e.g. /movie avatar)\n- /action, /comedy, /romance, etc.\n- /popular (most downloaded movies)\nOr just ask me for a joke or say hi!", "fr": "Je peux vous aider à trouver des films, recommander des genres et discuter! Essayez ceci:\n- /movie [nom] (ex: /movie avatar)\n- /action, /comedy, /romance, etc.\n- /popular (films les plus téléchargés)\nOu demandez-moi une blague ou dites bonjour!"},
        "joke": {"en": ["Why did the computer go to the movies? To get some byte-sized entertainment! 😄", "Why don't movie stars use social media? Because they already have too many followers!", "Why did the popcorn turn down the movie role? It didn't want to be in a corny film!", "Why did the scarecrow win an award? Because he was outstanding in his field!"], "fr": ["Pourquoi l'ordinateur est-il allé au cinéma? Pour un divertissement en octets! 😄", "Pourquoi les stars de cinéma n'utilisent-elles pas les réseaux sociaux? Parce qu'elles ont déjà trop de followers!", "Pourquoi le pop-corn a-t-il refusé le rôle au cinéma? Il ne voulait pas être dans un film trop 'maïs'!", "Pourquoi l'épouvantail a-t-il gagné un prix? Parce qu'il était exceptionnel dans son domaine!"]},
        "weather": {"en": "I can't check the weather yet, but I can recommend a cozy movie for any day! ☔🎬", "fr": "Je ne peux pas vérifier la météo, mais je peux recommander un film confortable pour n'importe quel jour! ☔🎬"},
        "time": {"en": "It's currently {now}. Perfect time for a movie, don't you think?", "fr": "Il est actuellement {now}. Moment parfait pour un film, non?"},
        "creator": {"en": "I was created by asamflix to help you discover awesome movies and have fun!", "fr": "J'ai été créé par asamflix pour vous aider à découvrir des films géniaux et vous amuser!"},
        "recommend": {"en": "Looking for a recommendation? Try /action or /comedy for the hottest movies right now!", "fr": "Vous cherchez une recommandation? Essayez /action ou /comedy pour les meilleurs films du moment!"},
        "learned": {"en": "Learned new response for: '{question}'", "fr": "Nouvelle réponse apprise pour: '{question}'"},
        "teach_usage": {"en": "To teach me, use: {cmd} question = answer", "fr": "Pour m'apprendre, utilisez: {cmd} question = réponse"},
        "fallback": {"en": ["Hmm, I didn't quite get that. Want to talk about movies or need a recommendation?", "I'm still learning! Try asking about movies, genres, or use /help for ideas.", "Sorry, I don't understand yet. But I can help you find a great movie!", "I'm here to chat and help with movies! Try /movie [name] or say hi."], "fr": ["Hmm, je n'ai pas bien compris. Voulez-vous parler de films ou besoin d'une recommandation?", "J'apprends encore! Essayez de demander des films, des genres, ou utilisez /help pour des idées.", "Désolé, je ne comprends pas encore. Mais je peux vous aider à trouver un super film!", "Je suis là pour discuter et aider avec les films! Essayez /movie [nom] ou dites bonjour."]}
    }
    # Check for 'what can you do' and similar queries first
    if any(phrase in processed_text for phrase in ["what can you do", "help", "commands", "options"]):
        return responses["help"][lang]
    greetings = ["hello", "hi", "hey", "yo", "sup", "wassup", "good morning", "good afternoon", "good evening", "morning", "afternoon", "evening", "greetings", "howdy", "what's up", "hiya", "heya", "salutations"]
    if any(greet in processed_text for greet in greetings):
        return random.choice(responses["greeting"][lang])
    if "good morning" in processed_text:
        return responses["good_morning"][lang]
    if "good afternoon" in processed_text:
        return responses["good_afternoon"][lang]
    if "good evening" in processed_text:
        return responses["good_evening"][lang]
    if any(phrase in processed_text for phrase in ["how are you", "how's it going", "how do you do", "how are things"]):
        return random.choice(responses["how_are_you"][lang])
    if any(phrase in processed_text for phrase in ["what's your name", "who are you", "your name"]):
        return responses["name"][lang]
    if any(phrase in processed_text for phrase in ["thank", "thanks", "thank you"]):
        return random.choice(responses["thanks"][lang])
    if any(phrase in processed_text for phrase in ["bye", "goodbye", "see you", "later", "catch you later"]):
        return random.choice(responses["bye"][lang])
    if any(phrase in processed_text for phrase in ["what can you do", "help", "commands", "options"]):
        return responses["help"][lang]
    if any(phrase in processed_text for phrase in ["joke", "make me laugh", "tell me something funny"]):
        return random.choice(responses["joke"][lang])
    if "weather" in processed_text:
        return responses["weather"][lang]
    if "time" in processed_text:
        now = datetime.now().strftime('%H:%M')
        return responses["time"][lang].format(now=now)
    if any(phrase in processed_text for phrase in ["who made you", "your creator", "who created you"]):
        return responses["creator"][lang]
    if "recommend" in processed_text and "movie" in processed_text:
        return responses["recommend"][lang]
    for cmd in ["learn:", "teach:", "add:", "remember:"]:
        if processed_text.startswith(cmd):
            try:
                _, pair = processed_text.split(cmd, 1)
                question, answer = pair.split("=", 1)
                question = question.strip()
                answer = answer.strip()
                learned_responses[question] = answer
                save_learned_responses(learned_responses)
                return responses["learned"][lang].format(question=question)
            except Exception:
                return responses["teach_usage"][lang].format(cmd=cmd)
    # Match learned responses if the question is contained in the message
    for question, answer in learned_responses.items():
        if question.strip().lower() in processed_text:
            return answer
    return random.choice(responses["fallback"][lang])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_text = update.message.text

    if user_id in blocked:
        return

    # --- Movie request confirmation ---
    if context.user_data.get("pending_request"):
        if message_text.strip().lower() == "yes":
            movie_name = context.user_data.pop("pending_request")
            await notify_admins_of_request(context, update.effective_user, movie_name)
            await update.message.reply_text("✅ Your request has been sent to the admins!")
            return
        else:
            context.user_data.pop("pending_request")

    hacking_keywords = [
        "os.", "subprocess", "eval(", "exec(", "import ", "open(", "token", "api_key", "del ", "rm ", "drop ", "delete ", "shutdown", "restart", "kill", "sudo", "chmod", "chown", "wget", "curl", "pip install", "apt-get", "system(", "bash", "sh ", "python", "exit(", "quit(", "fork", "thread", "multiprocessing"
    ]
    if any(kw in message_text.lower() for kw in hacking_keywords):
        await update.message.reply_text("⚠️ Suspicious activity detected. This action is not allowed.")
        return

    if "http://" in message_text or "https://" in message_text or "t.me/" in message_text:
        await warn_and_block(update, context)
        return

    movie_query = message_text or ""
    normalized_message = normalize_for_search(movie_query)
    for title, file_info in movie_files.items():
        normalized_title = normalize_for_search(title)
        # match when the normalized title appears inside the normalized message
        if not normalized_title:
            continue
        if normalized_title in normalized_message or normalized_message in normalized_title:
            # --- Download count ---
            movie_files[title]["downloads"] = movie_files[title].get("downloads", 0) + 1
            save_movie_files(movie_files)
            downloads = movie_files[title].get("downloads", 0)
            file_id = file_info["file_id"]
            file_type = file_info.get("file_type", "video")
            description = file_info.get("description", "")
            poster_url = file_info.get("poster_url", "")
            file_size = file_info.get("file_size")
            size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
            downloads_str = f"\nDownloads: {downloads}" if downloads else ""
            caption = f"{title.title()}{size_str}{downloads_str}"
            if description:
                caption += f"\n\n{description}"
            if poster_url:
                caption += f"\n\nPoster: {poster_url}"
            if file_type == "video":
                try:
                    await update.message.reply_video(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                except Exception as e:
                    print(f"Send file error for {title}: {e}")
                    await update.message.reply_text(f"Sorry, I couldn't send '{title}'. The file may be missing or the identifier is invalid.")
                    return
            elif file_type == "subtitle":
                try:
                    await update.message.reply_document(file_id, caption=caption + "\n\n[Subtitle]", reply_markup=await get_inline_buttons(title))
                except Exception as e:
                    print(f"Send file error for {title}: {e}")
                    await update.message.reply_text(f"Sorry, I couldn't send '{title}'. The file may be missing or the identifier is invalid.")
                    return
            else:
                try:
                    await update.message.reply_document(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                except Exception as e:
                    print(f"Send file error for {title}: {e}")
                    await update.message.reply_text(f"Sorry, I couldn't send '{title}'. The file may be missing or the identifier is invalid.")
                    return
            return

    if user_waiting_for_movie.get(user_id):
        user_waiting_for_movie.pop(user_id)
        context.args = message_text.split()
        await movie_command(update, context)
        return

    if update.message.chat.type == "private":
        response = await handle_response(message_text)
        await update.message.reply_text(response)

async def genre_command(update: Update, context: ContextTypes.DEFAULT_TYPE, genre: str):
    user_id = update.effective_user.id
    if user_id in ADMIN_IDS and not context.args:
        pending_genre_upload[user_id] = genre
        await update.message.reply_text(f"Send the movie file you want to add to the {genre.title()} genre.")
        return
    if context.args:
        search_name = ' '.join(context.args).strip().lower()
        matches = []
        for title, file_info in movie_files.items():
            if file_info.get("genre") == genre and search_name.replace(" ", "") in title.replace(" ", ""):
                matches.append((title, file_info))
        if matches:
            matches.sort()
            for title, file_info in matches:
                movie_files[title]["downloads"] = movie_files[title].get("downloads", 0) + 1
                save_movie_files(movie_files)
                downloads = movie_files[title].get("downloads", 0)
                file_id = file_info["file_id"]
                file_type = file_info.get("file_type", "video")
                description = file_info.get("description", "")
                poster_url = file_info.get("poster_url", "")
                file_size = file_info.get("file_size")
                size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
                downloads_str = f"\nDownloads: {downloads}" if downloads else ""
                caption = title.title() + size_str + downloads_str
                if description:
                    caption += f"\n\n{description}"
                if poster_url:
                    caption += f"\n\nPoster: {poster_url}"
                try:
                    if file_type == "video":
                        await update.message.reply_video(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                    elif file_type == "subtitle":
                        await update.message.reply_document(file_id, caption=caption + "\n\n[Subtitle]", reply_markup=await get_inline_buttons(title))
                    else:
                        await update.message.reply_document(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                except Exception as e:
                    print(f"Send file error for {title} in genre search: {e}")
                    await update.message.reply_text(f"Sorry, I couldn't send '{title}'. The file may be missing or invalid.")
            return
        await update.message.reply_text(f"No matching movies found in {genre.title()} for '{search_name}'.")
    else:
        found = False
        for title, file_info in movie_files.items():
            if file_info.get("genre") == genre:
                movie_files[title]["downloads"] = movie_files[title].get("downloads", 0) + 1
                save_movie_files(movie_files)
                downloads = movie_files[title].get("downloads", 0)
                file_id = file_info["file_id"]
                file_type = file_info.get("file_type", "video")
                description = file_info.get("description", "")
                poster_url = file_info.get("poster_url", "")
                file_size = file_info.get("file_size")
                size_str = f"\nSize: {format_size(file_size)}" if file_size else ""
                downloads_str = f"\nDownloads: {downloads}" if downloads else ""
                caption = title.title() + size_str + downloads_str
                if description:
                    caption += f"\n\n{description}"
                if poster_url:
                    caption += f"\n\nPoster: {poster_url}"
                try:
                    if file_type == "video":
                        await update.message.reply_video(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                    elif file_type == "subtitle":
                        await update.message.reply_document(file_id, caption=caption + "\n\n[Subtitle]", reply_markup=await get_inline_buttons(title))
                    else:
                        await update.message.reply_document(file_id, caption=caption, reply_markup=await get_inline_buttons(title))
                except Exception as e:
                    print(f"Send file error for {title} in genre listing: {e}")
                    await update.message.reply_text(f"Sorry, I couldn't send '{title}'. The file may be missing or invalid.")
                found = True
        if not found:
            await update.message.reply_text(f"No {genre.title()} movies available yet!")

def make_genre_handler(genre):
    return lambda update, context: genre_command(update, context, genre)

async def mention_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return
    if f"@{BOT_USERNAME.lstrip('@').lower()}" in update.message.text.lower():
        user_id = update.effective_user.id
        user_waiting_for_movie[user_id] = True
        await update.message.reply_text(
            "👋 I'm online! Please type the movie name you want to search."
        )

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

# --- Admin Panel ---
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    text = (
        "Admin Panel:\n"
        "/delete <movie_name> - Delete a movie\n"
        "/stats - Show bot stats\n"
        "/adduser <user_id> - Allow a user\n"
        "/removeuser <user_id> - Remove a user"
    )
    await update.message.reply_text(text)

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /delete <movie_name>")
        return
    movie_name = ' '.join(context.args).strip().lower()
    if movie_name in movie_files:
        del movie_files[movie_name]
        save_movie_files(movie_files)
        await update.message.reply_text(f"Deleted '{movie_name}'.")
    else:
        await update.message.reply_text("Movie not found.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    total_movies = len(movie_files)
    total_downloads = sum(f.get("downloads", 0) for f in movie_files.values())
    await update.message.reply_text(f"Total movies: {total_movies}\nTotal downloads: {total_downloads}")

async def adduser_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /adduser <user_id>")
        return
    try:
        user_id = int(context.args[0])
        ADMIN_IDS.add(user_id)
        await update.message.reply_text(f"User {user_id} added to allowed users.")
    except Exception:
        await update.message.reply_text("Invalid user_id.")

async def removeuser_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /removeuser <user_id>")
        return
    try:
        user_id = int(context.args[0])
        ADMIN_IDS.discard(user_id)
        await update.message.reply_text(f"User {user_id} removed from allowed users.")
    except Exception:
        await update.message.reply_text("Invalid user_id.")

# --- Multi-language Support ---
LANGUAGES = {"en": "English", "fr": "French"}
USER_LANG = {}  # user_id: lang_code

def get_lang(user_id):
    return USER_LANG.get(str(user_id), "en")

async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0] not in LANGUAGES:
        await update.message.reply_text("Usage: /setlang <en|fr>")
        return
    USER_LANG[str(update.effective_user.id)] = context.args[0]
    await update.message.reply_text(f"Language set to {LANGUAGES[context.args[0]]}")

def tr(text, lang):
    translations = {
        "en": {"welcome": "Welcome!", "not_allowed": "You are not allowed to use this bot."},
        "fr": {"welcome": "Bienvenue!", "not_allowed": "Vous n'êtes pas autorisé à utiliser ce bot."}
    }
    return translations.get(lang, translations["en"]).get(text, text)

# --- Scheduled Posting ---
async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /schedule <YYYY-MM-DD HH:MM> <movie_name>")
        return
    try:
        dt = datetime.strptime(context.args[0] + " " + context.args[1], "%Y-%m-%d %H:%M")
        movie_name = ' '.join(context.args[2:]).strip().lower()
        schedule[movie_name] = dt.strftime("%Y-%m-%d %H:%M")
        save_schedule(schedule)
        await update.message.reply_text(f"Scheduled '{movie_name}' for {dt}.")
    except Exception:
        await update.message.reply_text("Invalid format. Usage: /schedule <YYYY-MM-DD HH:MM> <movie_name>")

async def scheduled_posting(app):
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        to_post = [k for k, v in schedule.items() if v == now]
        for movie_name in to_post:
            if movie_name in movie_files and CHANNEL_ID:
                file_info = movie_files[movie_name]
                file_id = file_info["file_id"]
                caption = movie_name.title()
                try:
                    await send_media(CHANNEL_ID, 'video', file_id, caption, app.bot)
                except Exception as e:
                    print(f"Failed to post to channel: {e}")
                del schedule[movie_name]
                save_schedule(schedule)
        await asyncio.sleep(60)
async def scheduled_posting_job(context: ContextTypes.DEFAULT_TYPE):
    """JobQueue-compatible scheduled posting job."""
    app = context.application
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    to_post = [k for k, v in schedule.items() if v == now]
    for movie_name in to_post:
        if movie_name in movie_files and CHANNEL_ID:
            file_info = movie_files[movie_name]
            file_id = file_info["file_id"]
            caption = movie_name.title()
            try:
                await send_media(CHANNEL_ID, 'video', file_id, caption, app.bot)
            except Exception as e:
                print(f"Failed to post to channel: {e}")
            del schedule[movie_name]
            save_schedule(schedule)


async def validate_files_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: validate stored Telegram file IDs and report any invalid ones."""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    invalid = []
    checked = 0
    for title, info in movie_files.items():
        file_id = info.get("file_id")
        if not file_id:
            invalid.append((title, "missing file_id"))
            continue
        try:
            checked += 1
            await context.bot.get_file(file_id)
        except Exception as e:
            invalid.append((title, str(e)))
    msg = f"Checked {checked} files."
    if invalid:
        msg += "\nInvalid entries:\n"
        for title, reason in invalid:
            msg += f"- {title}: {reason}\n"
    else:
        msg += "\nAll file IDs look OK."
    await update.message.reply_text(msg)

if __name__ == '__main__':
    print('Starting bot...')
    # Ensure Application instances are weakref-able so JobQueue can store a weakref.
    # Some PTB builds define Application with __slots__ that do not include '__weakref__'.
    # Create a small subclass with '__weakref__' in __slots__ and replace the module
    # symbol so ApplicationBuilder will construct the subclass instead.
    try:
        import telegram.ext._application as _appmod
        Application = _appmod.Application
        app_slots = Application.__dict__.get('__slots__', ())
        # normalize to tuple
        if isinstance(app_slots, str):
            app_slots = (app_slots,)
        if '__weakref__' not in app_slots:
            new_slots = tuple(app_slots) + ('__weakref__',)
            _AppWithWeakRef = type(Application.__name__, (Application,), {'__slots__': new_slots})
            _appmod.Application = _AppWithWeakRef
    except Exception:
        # If anything goes wrong, fall back to default behavior and let PTB raise errors.
        pass

    builder = ApplicationBuilder().token(TOKEN)
    # If we created a subclass to add '__weakref__', ensure the builder uses it
    try:
        if '_AppWithWeakRef' in locals():
            # DefaultValue lives in the applicationbuilder module
            import telegram.ext._applicationbuilder as _ab
            builder._application_class = _ab.DefaultValue(locals()['_AppWithWeakRef'])
    except Exception:
        pass
    app = builder.build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('movie', movie_command))
    app.add_handler(CommandHandler('unblock', unblock_command))
    app.add_handler(CommandHandler('rename', rename_command))
    app.add_handler(CommandHandler('popular', popular_command))
    app.add_handler(CommandHandler('admin', admin_panel))
    app.add_handler(CommandHandler('delete', delete_command))
    app.add_handler(CommandHandler('stats', stats_command))
    app.add_handler(CommandHandler('adduser', adduser_command))
    app.add_handler(CommandHandler('removeuser', removeuser_command))
    app.add_handler(CommandHandler('setlang', setlang_command))
    app.add_handler(CommandHandler('schedule', schedule_command))
    app.add_handler(CommandHandler('movie_to_channel', movie_to_channel_command))
    app.add_handler(CommandHandler('movie_to_group', movie_to_group_command))
    app.add_handler(CommandHandler('rate', rate_command))
    app.add_handler(CommandHandler('showrating', show_rating_command))
    app.add_handler(CommandHandler('subscribe', subscribe_command))
    app.add_handler(CommandHandler('unsubscribe', unsubscribe_command))
    app.add_handler(CommandHandler('notifyme', notifyme_command))
    app.add_handler(CommandHandler('remindme', remindme_command))
    app.add_handler(CommandHandler('topmovies', topmovies_command))
    app.add_handler(CommandHandler('topusers', topusers_command))
    app.add_handler(CommandHandler('analytics', analytics_command))

    for genre in GENRES:
        app.add_handler(CommandHandler(genre, make_genre_handler(genre)))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f"@{BOT_USERNAME.lstrip('@')}"), mention_handler))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_error_handler(error)

    # --- Start scheduled posting via JobQueue ---
    # Run scheduled_posting_job every 60 seconds
    # Guard against environments where the PTB JobQueue is not available
    try:
        if getattr(app, 'job_queue', None) is not None:
            app.job_queue.run_repeating(scheduled_posting_job, interval=60, first=10)
        else:
            print("JobQueue not available; scheduled posting disabled.")
            print("To enable scheduled jobs install the job-queue extra: pip install \"python-telegram-bot[job-queue]\"")
    except AttributeError:
        print("JobQueue not available; scheduled posting disabled.")
        print("To enable scheduled jobs install the job-queue extra: pip install \"python-telegram-bot[job-queue]\"")
    except Exception as e:
        print(f"Could not schedule jobs: {e}\nScheduled posting disabled.")

    # Admin utility: validate stored file IDs
    app.add_handler(CommandHandler('validate_files', validate_files_command))

    print('polling...')
    try:
        app.run_polling()
    except Exception as e:
        # Provide a clearer error message when the bot token is invalid/rejected
        try:
            from telegram.error import InvalidToken
        except Exception:
            InvalidToken = None
        if InvalidToken is not None and isinstance(e, InvalidToken):
            print(f"ERROR: Bot token invalid or rejected by Telegram API: {e}")
            print("Please set a valid TELEGRAM_BOT_TOKEN in your environment or in a local .env file (see .env.example).")
            import sys
            sys.exit(1)
        # re-raise other unexpected exceptions so they can be debugged
        raise