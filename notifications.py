import dotenv, os, pyttsx3, pytz, datetime, genshin, asyncio
from win10toast import ToastNotifier
from time import localtime, strftime

dotenv.load_dotenv(dotenv_path="settings.env")
hsr = genshin.Client()
toaster = ToastNotifier()
engine = pyttsx3.init()

if os.getenv('set_cookies_method') == 'auto':
    hsr.set_browser_cookies()
else:
    hsr.set_cookies(ltuid=int(os.getenv('ltuid')), ltoken=os.getenv('ltoken'))

async def trailblaze():
    trailblaze_notification_send = False
    trailblaze_last_count = -1
    while(True):
        ac = await hsr.get_game_accounts()
        for account in ac:
            if "hkrpg" in account.game_biz:
                uid = account.uid
        notes = await hsr.get_starrail_notes(uid=uid)

        if trailblaze_notification_send == True:
            if trailblaze_last_count != notes.current_stamina:
                trailblaze_notification_send = False

        if (os.getenv('trailblaze_milestone')) == 'True':
            trailblaze_milestones = os.getenv('trailblaze_milestones').split(', ')
            if notes.current_stamina in trailblaze_milestones:
                if trailblaze_notification_send == False:
                    print(f"{strftime('%H:%M:%S', localtime())} | One of your Trailblaze Power milestone was reached")
                    if os.getenv('tts') == 'True':
                        engine.say("One of your Trailblaze Power milestone was reached")
                        engine.runAndWait()
                    trailblaze_last_count = notes.current_stamina
                    toaster.show_toast("One of your Trailblaze Power milestone was reached", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                    trailblaze_notification_send = True
            else:
                if trailblaze_notification_send == False:
                    if notes.current_stamina == notes.max_stamina:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power is FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your Trailblaze Power is FULL")
                            engine.runAndWait()
                        trailblaze_last_count = notes.current_stamina
                        toaster.show_toast("Your Trailblaze Power is FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                        trailblaze_notification_send = True
                    elif notes.current_stamina >= notes.max_stamina:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power isn't just FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your Trailblaze Power isn't just FULL")
                            engine.runAndWait()
                        trailblaze_last_count = notes.current_stamina
                        toaster.show_toast("Your Trailblaze Power isn't just FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                        trailblaze_notification_send = True   
        else:
            if trailblaze_notification_send == False:
                if notes.current_stamina == notes.max_stamina:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power is FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your Trailblaze Power is FULL")
                        engine.runAndWait()
                    trailblaze_last_count = notes.current_stamina
                    toaster.show_toast("Your Trailblaze Power is FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                    trailblaze_notification_send = True
                elif notes.current_stamina >= notes.max_stamina:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power isn't just FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your Trailblaze Power isn't just FULL")
                        engine.runAndWait()
                    trailblaze_last_count = notes.current_stamina
                    toaster.show_toast("Your Trailblaze Power isn't just FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                    trailblaze_notification_send = True

        await asyncio.sleep(480)

async def assignments():
    assignments_notification_send = False
    assignments_last_count = 0
    while(True):
        ac = await hsr.get_game_accounts()
        for account in ac:
            if "hkrpg" in account.game_biz:
                uid = account.uid
        notes = await hsr.get_starrail_notes(uid=uid)
        finished = 0
        for i in notes.expeditions:
            if i.status == "Finished":
                finished += 1

        if assignments_notification_send == True:
            if finished != assignments_last_count:
                assignments_notification_send = False

        elif assignments_notification_send == False:
            if finished == notes.total_expedition_num:
                print(f"{strftime('%H:%M:%S', localtime())} | All your assignments have completed")
                if os.getenv('tts') == 'True':
                    engine.say("All your assignments have completed")
                    engine.runAndWait()
                assignments_last_count = finished
                toaster.show_toast("All your assignments have completed", f"{assignments_last_count} assignments have completed out of {notes.total_expedition_num}", "ico/Assignment.ico", 15)
                assignments_notification_send = True
            elif finished > assignments_last_count:
                print(f"{strftime('%H:%M:%S', localtime())} | Some of your assignments have completed")
                if os.getenv('tts') == 'True':
                    engine.say("Some of your assignments have completed")
                    engine.runAndWait()
                assignments_last_count = finished
                toaster.show_toast("Some of your assignments have completed", f"{assignments_last_count} assignments have completed out of {notes.total_expedition_num}", "ico/Assignment.ico", 15)
                assignments_notification_send = True
        
        await asyncio.sleep(600)

async def daily():
    daily_last_day = -1
    timezone = pytz.timezone('Etc/GMT-8')
    while (True):
        day = datetime.datetime.now(timezone).strftime('%d')
        
        if daily_last_day != day:
            try:
                reward = await hsr.claim_daily_reward(game="hkrpg")
            except genshin.AlreadyClaimed:
                daily_last_day = day
            else:
                print(f"{strftime('%H:%M:%S', localtime())} | Claimed daily reward - {reward.amount}x {reward.name}")
                if os.getenv('tts') == 'True':
                    engine.say("Collected your daily check-in reward")
                    engine.runAndWait()
                daily_last_day = day
                if os.getenv('daily_not') == 'True':
                    toaster.show_toast("Collected your daily check-in reward", f"Claimed daily reward - {reward.amount}x {reward.name}", "ico/Daily.ico", 15)
        
        await asyncio.sleep(900)
      
if __name__ == "__main__":
    print("-----------------------------------")
    loop = asyncio.get_event_loop()
    if (os.getenv('trailblaze_not')) == 'True':
        task1 = asyncio.ensure_future(trailblaze())
        print("Trailblaze Power turned on")
    if (os.getenv('assignments_not')) == 'True':
        task2 = asyncio.ensure_future(assignments())
        print("Assignments turned on")
    if (os.getenv('daily_check_in')) == 'True':
        task3 = asyncio.ensure_future(daily())
        print("Daily check-in turned on")
    print("-----------------------------------")
    toaster.notification_active()
    loop.run_forever()
    