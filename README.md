# terraform-updater

I've chosen to use Python for its cross-platform capabilities. For maximum portability, I've also stuck to just using the standard library.
Because I was considering cross-platform, I have slightly exceeded the brief and made the script itself cross-platform.
I have confirmed that it runs on both a Windows 10 machine and a Raspberry Pi running Raspian (buster).

## Challenge 1
See the script file.

I've used an API I found to retrieve the latest version number more easily, though HTML scraping the release packages page would also work.
The script expects to be run with admin privilages and will exit with an error if it is denied permission at any point.

## Challenge 2
For a linux-based system, the easiest option for scheduling is probably cron.
If the following line is added to root's crontab, the command will execute at Monday 9am NZST (UTC+12)

`0 21 * * SUN python3 /path/to/script/terraform-updater.py`

## Challenge 3
Again see the attached script.

The script simply calls the existing install first for version info before renaming the binary by appending the version number to it.
