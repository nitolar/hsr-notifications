# HSR Notifications
[![Last Commit](https://img.shields.io/github/last-commit/nitolar/hsr-notifications)](https://github.com/nitolar/hsr-notifications/commits/master)
[![Repo size](https://img.shields.io/github/repo-size/nitolar/hsr-notifications)](https://github.com/nitolar/hsr-notifications/graphs/code-frequency)
[![LICENSE](https://img.shields.io/github/license/nitolar/hsr-notifications)](https://github.com/nitolar/hsr-notifications/blob/master/LICENSE.md)


Brings Trailblaze Power and Assignments notifications to your windows PC!

Also automatically collects your daily check-in!

[Check out Genshin Impact version](https://github.com/nitolar/genshin-notifications)


## Preview

[hsr not.webm](https://github.com/nitolar/hsr-notifications/assets/73779998/e0f21b2a-4e52-47c5-a9b5-5a51f27496a6)


## How to use

Install [python](https://www.python.org)

Clone the project or download it

```bash
git clone https://github.com/nitolar/hsr-notifications
```

Go to the project directory

```bash
cd hsr-notifications
```

Install requirements.txt

```bash
pip install -r requirements.txt
```

Configure the settings.env file

Run file

```bash
python notifications.py
```


## Changelog

### 17.10.2024

**After this update you must reinstall requirements.txt! Or install win11toast using: pip install win11toast**
- Rewrote an entire project to use `win11toast` instead of `win10toast`
- Added `trailblaze_milestones_margin`, more information in `settings.env`
- Changed all `.ico` files in `/ico` to have the same width and height

### 24.09.2024

- Fixed Forgotten Hall reset reminder being sent even though it wasn't

### 22.09.2024

**After this update you must reinstall requirements.txt! Or install psutil using: pip install psutil**
- Added Shop, Forgotten Hall, Pure Fiction and Apocalyptic Shadow reset notification
- Added reminders when you turn on Honkai: Star Rail
- Added 180, 200, 220 Trailblaiz Power to `trailblaze_milestones`
- Added errors when incorrect values are set for `set_cookies_method` (not set to `auto` or `login`), `ltuid` (set to deafult 0), `ltoken` (empty), `server` (not set to one of those `eu`, `us`, `as`)

### 08.06.2023

- First release


## Thanks to

[thesadru](https://github.com/thesadru) for creating [genshin.py](https://github.com/thesadru/genshin.py).


## Feedback

Like what you see? Give a star if you don't mind.

Found any bugs? Report them here: https://github.com/nitolar/hsr-notifications/issues


## Authors

- [@nitolar](https://www.github.com/nitolar)

