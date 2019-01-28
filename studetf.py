#!/usr/bin/env python3

import os
import time
import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery

from transliterate import translit

from bs4 import BeautifulSoup

import config

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(config.LOGLEVEL))
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(config.LOGFORMAT))
stream_handler.setLevel(logging.getLevelName(config.LOGLEVEL))
logger.addHandler(stream_handler)


def build_service(certificate_path=config.CERTIFICATE_PATH):
    logger.debug('Setting up calendar service')
    scope = 'https://www.googleapis.com/auth/calendar'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(certificate_path, scope)
    service = discovery.build('calendar', 'v3', credentials=credentials)
    return service


def fetch_exams(username=config.STUDENT_USERNAME, password=config.STUDENT_PASSWORD,
                geckodriver_path=config.GECKODRIVER_PATH) -> list:
    logger.debug('Fetching exams')
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=geckodriver_path)
    driver.get('http://student.etf.bg.ac.rs')

    username_field = driver.find_element_by_id('j_username')
    username_field.send_keys(username)
    password_field = driver.find_element_by_id('j_password')
    password_field.send_keys(password)
    driver.find_element_by_id('login').click()

    element = driver.find_element_by_id('menu_nav1_txt4')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = [x for x in soup.find_all('h1') if 'Пријављени' in x.text][0]
    table = title.next_element.next_element

    driver.close()

    exams = []
    for row in table.findAll('tr'):
        exams.append([x.text for x in row.findAll('td')])
    return [exam_to_dict(x) for x in exams[2:]]


def exam_to_dict(exam):
    raw_date = exam[7].strip()
    raw_time = exam[8].strip()

    date = None

    if raw_date:
        date = datetime.datetime.strptime(raw_date, "%d.%m.%Y.")

    if raw_time:
        h, m = raw_time.split(':')
        date = date.replace(hour=int(h), minute=int(m))

    return {
        'acronym': translit(exam[2].strip(), reversed=True, language_code='sr'),
        'name': translit(exam[3].strip(), reversed=True, language_code='sr'),
        'date': date,
        'location': translit(exam[9].strip(), reversed=True, language_code='sr')
    }


def get_event(exam, service, calendar_id=config.CALENDAR_ID):
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=(exam['date'] - datetime.timedelta(hours=24)).isoformat() + 'Z',
        timeMax=(exam['date'] + datetime.timedelta(hours=24)).isoformat() + 'Z'
    ).execute()

    for item in events['items']:
        if item['summary'] == exam['name']:
            return item

    return None


def upsert_event(exam, service, calendar_id=config.CALENDAR_ID):
    if exam['date'] is None:
        return
    elif exam['date'].hour == 0 and exam['date'].minute == 0:
        start = {'date': exam['date'].strftime('%Y-%m-%d')}
        end = {'date': exam['date'].strftime('%Y-%m-%d')}
    else:
        start = {
            'dateTime': exam['date'].isoformat(),
            'timeZone': 'Europe/Belgrade'
        }
        end = {
            'dateTime': (exam['date'] + datetime.timedelta(hours=3)).isoformat(),
            'timeZone': 'Europe/Belgrade'
        }

    body = {
        'summary': exam['name'],
        'start': start,
        'end': end,
        'location': exam['location']
    }

    event = get_event(exam, service, calendar_id)

    if event is None:
        service.events().insert(
            calendarId=calendar_id,
            body=body
        ).execute()
    else:
        x = service.events().update(
            calendarId=calendar_id,
            eventId=event['id'],
            body=body
        ).execute()


def run():
    logger.debug(f'Starting with config: '
                 f'STUDENT_USERNAME = {config.STUDENT_USERNAME}, '
                 f'STUDENT_PASSWORD = {config.STUDENT_PASSWORD}, '
                 f'CALENDAR_ID = {config.CALENDAR_ID}, '
                 f'GECKODRIVER_PATH = {config.GECKODRIVER_PATH}, '
                 f'CERTIFICATE_PATH = {config.CERTIFICATE_PATH}, '
                 f'LOGLEVEL = {config.LOGLEVEL}')
    exams = fetch_exams()
    service = build_service()
    for exam in exams:
        logger.debug('Upserting "%s"' % exam['name'])
        upsert_event(exam, service)
    logger.debug('Done!')


if __name__ == '__main__':
    run()
