from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,ConversationHandler,filters,MessageHandler, CallbackQueryHandler
# from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
from datetime import UTC
from remotive_search import call_remotive
from naukri_search import call_naukri
from internshala_search import call_intern
#Loading environment variable from .env file
load_dotenv()
TOKEN=os.getenv('JOB_HUNTER_TOKEN')
#States for naukri command
NAUKRI_KEY, NAUKRI_LOC = range(2)
#States for internshala command
INTERN_KEY, INTERN_LOC = range(2)
#States for Remotive command
REMOTIVE_KEY, REMOTIVE_COMPANY = range(2)
#Inline Keyboard Markup
nav_inline_keyboard=InlineKeyboardMarkup([[InlineKeyboardButton('⬅️',callback_data='page_prev'),InlineKeyboardButton('➡️',callback_data='page_next')]])
#Reply Keyboard Button
cancel_button=ReplyKeyboardMarkup([['Cancel']], resize_keyboard=True, one_time_keyboard=True)
#Pagination for Better UI
def log_user(user,command):
    user_id=user.id or ''
    user_first=user.first_name or ''
    user_last=user.last_name or ''
    user_lang=user.language_code or ''
    username=user.username or ''
    is_bot=str(user.is_bot) or 'None'
    time=datetime.now(UTC).isoformat()
    with open('user_logs.csv','a',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow([user_id,username,user_first,user_last,is_bot,user_lang,time,command])
def paginate_jobs(full_text, jobs_per_page=4):
    jobs = full_text.strip().split('\n\n')  # split each job block
    pages = []
    for i in range(0, len(jobs), jobs_per_page):
        page = '\n\n'.join(jobs[i:i+jobs_per_page])
        pages.append(page)
    return pages

# start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.effective_user,'start')
    await update.message.reply_text(f"Hi {update.effective_user.first_name}! I am Job Hunter bot. You can search for jobs across different platform by using these command : \n/internshala - Search internships on Internshala.\n/naukri - Search jobs on Naukri.\n/remotive - Search jobs on Remotive",reply_to_message_id=update.message.id)
# remotive command
async def remotive_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.effective_user,'remotive')
    await update.message.reply_text('Enter the keyword / designation e.g. Software Engineer',reply_markup=cancel_button)
    return REMOTIVE_KEY

async def remotive_keyword(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # print(user_message)
    if update.message.text.lower()=='cancel':
        return await cancel_command(update, context)
    context.user_data['keyword'] = update.message.text
    await update.message.reply_text('Enter your desired company e.g. Meta')
    return REMOTIVE_COMPANY

async def remotive_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower()=='cancel':
        return await cancel_command(update, context)
    company_name=update.message.text
    jobs=call_remotive(context.user_data['keyword'],company_name)
    await update.message.reply_text('Processing...', reply_markup=ReplyKeyboardRemove())
    if '\n\n' in jobs:
        paged_jobs=paginate_jobs(jobs)
        context.user_data['pages']=paged_jobs
        context.user_data['page_index']=0
        footer=f'*Page 1/{len(paged_jobs)}*'
        await update.message.reply_text(f'{paged_jobs[0]}\n\n{footer}',parse_mode='markdown',reply_markup=nav_inline_keyboard,link_preview_options=LinkPreviewOptions(is_disabled=True))
        return ConversationHandler.END
    else:
        await update.message.reply_text(jobs,parse_mode='markdown', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def jobs_page_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    pages=context.user_data.get('pages',[])
    page_index=context.user_data.get('page_index',0)
    if query.data=='page_prev' and page_index>0:
        page_index-=1
    elif query.data=='page_next' and page_index<len(pages)-1:
        page_index+=1
    else:
        return
    context.user_data['page_index']=page_index
    footer=f'*Page {page_index+1}/{len(pages)}*'
    await query.edit_message_text(f'{pages[page_index]}\n\n{footer}',parse_mode='markdown',reply_markup=nav_inline_keyboard,link_preview_options=LinkPreviewOptions(is_disabled=True))


#Internshala command
async def intern_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.effective_user,'internshala')
    await update.message.reply_text("Enter the keyword / designation e.g. Software Engineer",reply_markup=cancel_button)
    return INTERN_KEY

async def intern_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower()=='cancel':
        return await cancel_command(update,context)
    context.user_data['keyword']=update.message.text
    await update.message.reply_text('Enter your desired location e.g. Mumbai')
    return INTERN_LOC

async def intern_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower()=='cancel':
        return await cancel_command(update,context)
    jobs=call_intern(context.user_data['keyword'],update.message.text)
    await update.message.reply_text('Processing...',reply_markup=ReplyKeyboardRemove())
    if '\n\n' in jobs:
        paged_jobs=paginate_jobs(jobs)
        context.user_data['pages']=paged_jobs
        context.user_data['page_index']=0
        footer=f'*Page 1/{len(paged_jobs)}*'
        await update.message.reply_text(f'{paged_jobs[0]}\n\n{footer}',parse_mode='markdown',reply_markup=nav_inline_keyboard,link_preview_options=LinkPreviewOptions(is_disabled=True))
        return ConversationHandler.END
    else:
        await update.message.reply_text(jobs,parse_mode='markdown')
        return ConversationHandler.END

# Naukri command

async def naukri_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update.effective_user,'naukri')
    await update.message.reply_text('Enter the keyword / designation e.g. Software Engineer',reply_markup=cancel_button)
    return NAUKRI_KEY

async def naukri_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower()=='cancel':
        return await cancel_command(update,context)
    context.user_data['keyword']=update.message.text
    await update.message.reply_text('Enter your desired location e.g. Mumbai')
    return NAUKRI_LOC

async def naurkri_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() == 'cancel':
        return await cancel_command(update, context)
    r=call_naukri(context.user_data['keyword'], update.message.text)
    await update.message.reply_text('Processing...',reply_markup=ReplyKeyboardRemove())
    if '\n\n' in r:
        paged_jobs=paginate_jobs(r)
        context.user_data['pages']=paged_jobs
        context.user_data['page_index']=0
        footer=f'*Page 1/{len(paged_jobs)}*'
        await update.message.reply_text(f'{paged_jobs[0]}\n\n{footer}',parse_mode='markdown', reply_markup=nav_inline_keyboard, link_preview_options=LinkPreviewOptions(is_disabled=True))
        return ConversationHandler.END
    else:
        await update.message.reply_text(r)
        return ConversationHandler.END
# cancel command
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
#build app
app = ApplicationBuilder().token(TOKEN).build()
print('Bot Started...')
#handling commands
app.add_handler(CommandHandler('start',start_command))
app.add_handler(ConversationHandler(entry_points=[CommandHandler('remotive',remotive_command)],states={REMOTIVE_KEY : [MessageHandler(filters.TEXT & ~filters.COMMAND,remotive_keyword)],REMOTIVE_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND,remotive_company)]},fallbacks=[CommandHandler('cancel',cancel_command)]))
app.add_handler(CallbackQueryHandler(callback=jobs_page_navigation,pattern='^page_'))
app.add_handler(ConversationHandler([CommandHandler('internshala',intern_command)],{INTERN_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, intern_keyword)], INTERN_LOC : [MessageHandler(filters.TEXT & ~filters.COMMAND, intern_location)]},fallbacks=[CommandHandler('cancel',cancel_command)]))
app.add_handler(ConversationHandler(entry_points=[CommandHandler('naukri',naukri_command)], states={NAUKRI_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, naukri_keyword)], NAUKRI_LOC: [MessageHandler(filters.TEXT & ~filters.COMMAND,naurkri_location)]}, fallbacks=[CommandHandler('cancel',cancel_command)]))
#polling
print('Polling...')
app.run_polling(poll_interval=2)
