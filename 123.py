from __future__ import print_function
import httplib2
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
import json
import datetime
import time
import telepot
import sys
import schedule
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
client_secret_calendar=(r"C:\Users\Pimonov\Desktop\new\secret.json") #указываем путь к скачанному Json
def job():
    def main():
        vk = vk_api.VkApi(token="2d5eb40cbd14bec3c54e61279db374dbd75e270d8e10b65ecc878cd5f1de988e27791e738e387b2dacbc2")
        vk._auth_token()
        vk.get_api()
        longpoll = VkBotLongPoll(vk, 170644194)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret_calendar, 'https://www.googleapis.com/auth/calendar.readonly')
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        now_1day = round(time.time())+86400 #плюс сутки
        now_1day = datetime.datetime.fromtimestamp(now_1day).isoformat() + 'Z'
        print('Берем 100 событий')
        eventsResult = service.events().list(
            calendarId='p86u8onqnnirbf2ih6gi559rpk@group.calendar.google.com', timeMin=now, timeMax=now_1day, maxResults=50, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items',[])

        if not events:
            print('Нет событий на ближайшие сутки')
        else:
            stdoutOrigin=sys.stdout 
            sys.stdout = open("log.txt", "w")
            print('Расписание занятий на завтрашний день:\n')
            for event in events:
                start = 'ДАТА  '+ ' ',event['start'].get('dateTime').split('T')
                print(start,'-', event['summary'])
                sys.stdout.close()
                sys.stdout=stdoutOrigin
                with open("log.txt") as file:
                    int_number = file.read()
            for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW:
                            if "РАСПИСАНИЕ" in event.object.text:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": " " + str(int_number)+ " ", "random_id": 0
                                            })
                            if event.object.text.lower() == "расписание" or event.object.text.lower() == "распес" or event.object.text.lower() == "распес." :
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": " " + str(int_number)+ " ", "random_id": 0})
                            if event.object.text.lower() == "номер модератора":
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "Никита Иорданян +7-913-382-21-68" , "random_id": 0})
    if __name__ == '__main__':
        main()
    

print('Listening ...')
schedule.every(5).seconds.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("11:15").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

