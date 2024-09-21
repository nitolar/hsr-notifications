import dotenv, os, pyttsx3, pytz, datetime, genshin, asyncio, json, contextvars, functools, psutil
from win10toast import ToastNotifier
from time import localtime, strftime

dotenv.load_dotenv(dotenv_path="settings.env")
hsr = genshin.Client()
toaster = ToastNotifier()
engine = pyttsx3.init()
os.system("") # To make colors in errors always work

if os.path.exists("cache.json"):
    pass
else: 
    with open("cache.json", "w", encoding='utf-8') as cache_f:
        data = {
            'hall_season': 0,
            'pf_season': 0,
            'apocalyptic_season': 0
        }
        json.dump(data, cache_f, indent=4)

if os.getenv('set_cookies_method') == 'auto':
    hsr.set_browser_cookies()
elif os.getenv('set_cookies_method') == 'login':
    if os.getenv('ltuid') == 0 or os.getenv('ltoken') == "":
        print("\33[31mIncorrect ltuid or ltoken empty!\033[0m")
        exit()
    else:
        hsr.set_cookies(ltuid=int(os.getenv('ltuid')), ltoken=os.getenv('ltoken'))
else:
    print("\33[31mIncorrect value for \"set_cookies_method\"! \n\33[93mSet it to: \"login\" or \"auto\"\033[0m")
    exit()

if os.getenv("server") not in ["eu", "us", "as"]:
    print("\33[31mIncorrect value for \"server\"! \n\33[93mSet it to on of this values: \"eu\", \"us\", \"as\"\033[0m")
    exit()

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

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
                    await to_thread(toaster.show_toast, "One of your Trailblaze Power milestone was reached", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                    trailblaze_notification_send = True
            else:
                if trailblaze_notification_send == False:
                    if notes.current_stamina == notes.max_stamina:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power is FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your Trailblaze Power is FULL")
                            engine.runAndWait()
                        trailblaze_last_count = notes.current_stamina
                        await to_thread(toaster.show_toast, "Your Trailblaze Power is FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                        trailblaze_notification_send = True
                    elif notes.current_stamina >= notes.max_stamina:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power isn't just FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your Trailblaze Power isn't just FULL")
                            engine.runAndWait()
                        trailblaze_last_count = notes.current_stamina
                        await to_thread(toaster.show_toast, "Your Trailblaze Power isn't just FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                        trailblaze_notification_send = True   
        else:
            if trailblaze_notification_send == False:
                if notes.current_stamina == notes.max_stamina:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power is FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your Trailblaze Power is FULL")
                        engine.runAndWait()
                    trailblaze_last_count = notes.current_stamina
                    await to_thread(toaster.show_toast, "Your Trailblaze Power is FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
                    trailblaze_notification_send = True
                elif notes.current_stamina >= notes.max_stamina:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your Trailblaze Power isn't just FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your Trailblaze Power isn't just FULL")
                        engine.runAndWait()
                    trailblaze_last_count = notes.current_stamina
                    await to_thread(toaster.show_toast, "Your Trailblaze Power isn't just FULL", f"You currently have {notes.current_stamina} Trailblaze Power out of {notes.max_stamina}", "ico/Trailblaze.ico", 15)
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
                await to_thread(toaster.show_toast, "All your assignments have completed", f"{assignments_last_count} assignments have completed out of {notes.total_expedition_num}", "ico/Assignment.ico", 15)
                assignments_notification_send = True
            elif finished > assignments_last_count:
                print(f"{strftime('%H:%M:%S', localtime())} | Some of your assignments have completed")
                if os.getenv('tts') == 'True':
                    engine.say("Some of your assignments have completed")
                    engine.runAndWait()
                assignments_last_count = finished
                await to_thread(toaster.show_toast, "Some of your assignments have completed", f"{assignments_last_count} assignments have completed out of {notes.total_expedition_num}", "ico/Assignment.ico", 15)
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
                    await to_thread(toaster.show_toast, "Collected your daily check-in reward", f"Claimed daily reward - {reward.amount}x {reward.name}", "ico/Daily.ico", 15)

        await asyncio.sleep(900)

async def shop():
    timezones = {"eu": "Etc/GMT-1", "as": "Etc/GMT-8", "us": "Etc/GMT+5"}
    last_day = -1
    while(True):
        day = datetime.datetime.now(pytz.timezone(timezones[os.getenv("server")])).strftime('%d')

        if last_day != day:
            last_day = day
            if day == "01":
                print(f"{strftime('%H:%M:%S', localtime())} | Shop has been reset today")
                if os.getenv('tts') == 'True':
                    engine.say("Shop has been reset today")
                    engine.runAndWait()
                await to_thread(toaster.show_toast, "Shop reset", f"Shop has been reset today", "ico/Shop.ico", 60)

        await asyncio.sleep(900)

hall_reset = False

async def hall():
    global hall_reset
    while(True):    
        ac = await hsr.get_game_accounts()
        for account in ac:
            if "hkrpg" in account.game_biz:
                uid = account.uid
        hall = await hsr.get_starrail_challenge(uid=uid)

        with open("cache.json", "r", encoding='utf-8') as cache_f:
            cache = json.load(cache_f)
            season = cache['hall_season']
            cache_f.close()

        if season != hall.seasons[0].id:
            with open("cache.json", "w", encoding='utf-8') as cache_f:
                hall_reset = True
                cache['hall_season'] = hall.seasons[0].id
                json.dump(cache, cache_f, indent=4)
                cache_f.close()
            print(f"{strftime('%H:%M:%S', localtime())} | Forgotten Hall has been reset")
            if os.getenv('tts') == 'True':
                engine.say("Forgotten Hall has been reset")
                engine.runAndWait()
            await to_thread(toaster.show_toast, "Forgotten Hall reset", f"Forgotten Hall has been reset", "ico/Hall.ico", 60)

        await asyncio.sleep(900)

pf_reset = False

async def pf():
    global pf_reset
    while(True):    
        ac = await hsr.get_game_accounts()
        for account in ac:
            if "hkrpg" in account.game_biz:
                uid = account.uid
        pf = await hsr.get_starrail_pure_fiction(uid=uid)

        with open("cache.json", "r", encoding='utf-8') as cache_f:
            cache = json.load(cache_f)
            season = cache['pf_season']
            cache_f.close()

        if season != pf.seasons[0].id:
            with open("cache.json", "w", encoding='utf-8') as cache_f:
                pf_reset = True
                cache['pf_season'] = pf.seasons[0].id
                json.dump(cache, cache_f, indent=4)
                cache_f.close()
            print(f"{strftime('%H:%M:%S', localtime())} | Pure Fiction has been reset")
            if os.getenv('tts') == 'True':
                engine.say("Pure Fiction has been reset")
                engine.runAndWait()
            await to_thread(toaster.show_toast, "Pure Fiction reset", f"Pure Fiction has been reset", "ico/pf.ico", 60)

        await asyncio.sleep(900)

apocalyptic_reset = False

async def apocalyptic():
    global apocalyptic_reset
    while(True):    
        ac = await hsr.get_game_accounts()
        for account in ac:
            if "hkrpg" in account.game_biz:
                uid = account.uid
        apocalyptic = await hsr.get_starrail_apc_shadow(uid=uid)

        with open("cache.json", "r", encoding='utf-8') as cache_f:
            cache = json.load(cache_f)
            season = cache['apocalyptic_season']
            cache_f.close()

        if season != apocalyptic.seasons[0].id:
            with open("cache.json", "w", encoding='utf-8') as cache_f:
                apocalyptic_reset = True
                cache['apocalyptic_season'] = apocalyptic.seasons[0].id
                json.dump(cache, cache_f, indent=4)
                cache_f.close()
            print(f"{strftime('%H:%M:%S', localtime())} | Apocalyptic Shadow has been reset")
            if os.getenv('tts') == 'True':
                engine.say("Apocalyptic Shadow has been reset")
                engine.runAndWait()
            await to_thread(toaster.show_toast, "Apocalyptic Shadow reset", f"Apocalyptic Shadow has been reset", "ico/Apocalyptic.ico", 60)

        await asyncio.sleep(900)

async def reminder():
    game_on = False
    global hall_reset
    global pf_reset
    global apocalyptic_reset
    while (True):
        name = "starrail.exe" # "notepad++.exe"
        if name in (p.name().lower() for p in psutil.process_iter()):
            if game_on == False:
                game_on = True

                if (int(os.getenv("reminder_additional_delay")) != 0):
                    await asyncio.sleep(int(os.getenv("reminder_additional_delay")))

                timezones = {"eu": "Etc/GMT-1", "as": "Etc/GMT-8", "us": "Etc/GMT+5"}
                day = datetime.datetime.now(pytz.timezone(timezones[os.getenv("server")])).strftime('%d')
                if os.getenv("reminder_shop") == "True":
                    if day == "01":
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Shop has been reset today")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Shop has been reset today")
                            engine.runAndWait()
                        await to_thread(toaster.show_toast, "Shop reset", f"Shop has been reset today", "ico/Shop.ico", 5)

                if os.getenv("reminder_hall") == "True":
                    if hall_reset:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Forgotten Hall has been reset")
                    if os.getenv('tts') == 'True':
                        engine.say("REMINDER Forgotten Hall has been reset")
                        engine.runAndWait()
                    await to_thread(toaster.show_toast, "Forgotten Hall reset", f"Forgotten Hall has been reset", "ico/Hall.ico", 5)

                if os.getenv("reminder_pf") == "True":
                    if pf_reset:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Pure Fiction has been reset")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Pure Fiction has been reset")
                            engine.runAndWait()
                        await to_thread(toaster.show_toast, "Pure Fiction reset", f"Pure Fiction has been reset", "ico/pf.ico", 5)

                if os.getenv("reminder_apocalyptic") == "True":
                    if apocalyptic_reset:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Apocalyptic Shadow has been reset")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Apocalyptic Shadow has been reset")
                            engine.runAndWait()
                        await to_thread(toaster.show_toast, "Apocalyptic Shadow reset", f"Apocalyptic Shadow has been reset", "ico/Apocalyptic.ico", 5)
        else:
            if game_on == True:
                game_on = False

        await asyncio.sleep(int(os.getenv("reminder_time")))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("-----------------------------------")
    if (os.getenv('trailblaze_not')) == 'True':
        task1 = asyncio.ensure_future(trailblaze())
        print("Trailblaze Power turned on")
    if (os.getenv('assignments_not')) == 'True':
        task2 = asyncio.ensure_future(assignments())
        print("Assignments turned on")
    if (os.getenv('daily_check_in')) == 'True':
        task3 = asyncio.ensure_future(daily())
        print("Daily check-in turned on")
    if (os.getenv('shop_not')) == 'True':
        task4 = asyncio.ensure_future(shop())
        print("Shop reset turned on")
    if (os.getenv('hall_not')) == 'True':
        task5 = asyncio.ensure_future(hall())
        print("Forgotten Hall reset turned on")
    if (os.getenv('pf_not')) == 'True':
        task6 = asyncio.ensure_future(pf())
        print("Pure Fiction reset turned on")
    if (os.getenv('apocalyptic_not')) == 'True':
        task7 = asyncio.ensure_future(apocalyptic())
        print("Apocalyptic Shadow reset turned on")
    if (os.getenv('reminder')) == 'True':
        task8 = asyncio.ensure_future(reminder())
        print('Reminder turned on')
    print("-----------------------------------")
    toaster.notification_active()
    loop.run_forever()