#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import json
import shutil
import urllib2
import argparse
import cgi

from PIL import Image

PRIVACY_URL = "http://senspark.com/privacy-policy"
MARKETING_URL = "http://senspark.com"
SUPPORT_URL = "http://fb.com/teamsenspark"

IOS_LANGUAGES_CODES   = {       'en-US'     :   'english',
                                'en-AU'     :   'english',
                                'en-CA'     :   'english',
                                'en-GB'     :   'english',
                                'zh-Hans'   :   'chinese simplified',
                                'zh-Hant'   :   'chinese traditional',
                                'da'        :   'danish',
                                'de-DE'     :   'german',
                                'el'        :   'greek',
                                'fi'        :   'finnish',
                                'fr-CA'     :   'french',
                                'fr-FR'     :   'french',
                                'id'        :   'indonesian',
                                'it'        :   'italian',
                                'ja'        :   'japanese',
                                'ko'        :   'korean',
                                'ms'        :   'malay',
                                'nl-NL'     :   'dutch',
                                'no'        :   'norwegian',
                                'pt-BR'     :   'portuguese brazil',
                                'pt-PT'     :   'portuguese portugal',
                                'ru'        :   'russian',
                                'es-MX'     :   'spanish',
                                'es-ES'     :   'spanish',
                                'sv'        :   'swedish',
                                'th'        :   'thai',
                                'tr'        :   'turkish',
                                'vi'        :   'vietnamese'
}

ANDROID_LANGUAGES_CODES   = {   'en-US'     :   'english',
                                'zh-CN'     :   'chinese simplified',
                                'zh-TW'     :   'chinese traditional',
                                'ar'        :   'arabic',
                                'be'        :   'belarusian',
                                'bg'        :   'bulgarian',
                                'cs-CZ'     :   'czech',
                                'da-DK'     :   'danish',
                                'de-DE'     :   'german',
                                'el-GR'     :   'greek',
                                'es-ES'     :   'spanish',
                                'fi-FI'     :   'finnish',
                                'fil'       :   'filipino',
                                'fr-FR'     :   'french',
                                'hi-IN'     :   'hindi',
                                'hr'        :   'croatian',
                                'hu-HU'     :   'hungarian',
                                'id'        :   'indonesian',
                                'it-IT'     :   'italian',
                                'ja-JP'     :   'japanese',
                                'ko-KR'     :   'korean',
                                'lv'        :   'latvian',
                                'ms'        :   'malay',
                                'nl-NL'     :   'dutch',
                                'no-NO'     :   'norwegian',
                                'pl-PL'     :   'Polish',
                                'pt-BR'     :   'portuguese brazil',
                                'pt-PT'     :   'portuguese portugal',
                                'ro'        :   'romanian',
                                'ru-RU'     :   'russian',
                                'sr'        :   'serbian',
                                'sk'        :   'slovak',
                                'sl'        :   'slovenian',
                                'sv-SE'     :   'swedish',
                                'th'        :   'thai',
                                'tr-TR'     :   'turkish',
                                'uk'        :   'ukrainian',
                                'vi'        :   'vietnamese',
                                'af'        :   'afrikaans',
                                'am'        :   'amharic',
                                'hy-AM'     :   'armenian',
                                'az-AZ'     :   'azerbaijani',
                                'eu-ES'     :   'basque',
                                'bn-BD'     :   'bengali',
                                'my-MM'     :   'burmese',
                                'ca'        :   'catalan',
                                'et'        :   'estonian',
                                'gl-ES'     :   'galician',
                                'ka-GE'     :   'georgian',
                                'iw-IL'     :   'hebrew',
                                'is-IS'     :   'icelandic',
                                'kn-IN'     :   'kannada',
                                'km-KH'     :   'khmer',
                                'ky-KG'     :   'kyrgyz',
                                'lo-LA'     :   'lao',
                                'lt'        :   'lithuanian',
                                'mk-MK'     :   'macedonian',
                                'ml-IN'     :   'malayalam',
                                'mr-IN'     :   'marathi',
                                'mn-MN'     :   'mongolian',
                                'ne-NP'     :   'nepali',
                                'fa'        :   'persian',
                                'si-LK'     :   'Sinhala',
                                'sw'        :   'swahili',
                                'ta-IN'     :   'tamil',
                                'te-IN'     :   'telugu',
                                'zu'        :   'zulu',
}

def generate_file(path, content):
    print path
    with open(path, 'w') as file:
        file.write(content)

def check_and_generate_file(path, content, max):
    content_length = len(content)
    if content_length > max:
        print "%s is too long and greater than %d characters: %d" % (path, max, content_length)
    generate_file(path, content.encode('utf-8'))

def read_sheet_data(sheet_id):
    # https://developers.google.com/chart/interactive/docs/spreadsheets
    # https://developers.google.com/chart/interactive/docs/querylanguage
    sheet_url = "http://docs.google.com/spreadsheets/d/%s/gviz/tq?&gid=0&headers=0" % sheet_id
    request = urllib2.urlopen(sheet_url)

    content = request.read()

    # Find the first opening parenthesis.
    first_parenthesis = content.find('{')

    # Find the last closing parenthesis.
    last_parenthesis = content.rfind('}')

    # Retrieve the JSON formatted string.
    result = content[first_parenthesis:last_parenthesis + 1]

    # Convert string to JSON.
    data = json.loads(result)
    return data

def get_number_of_rows(data):
    table = data["table"]
    rows = table["rows"]
    return len(rows)

def get_number_of_columns(data):
    table = data["table"];
    cols = table["cols"]
    return len(cols)

def get_cell(data, row, column):
    table = data["table"]

    row_data = table["rows"][row]
    if row_data == None:
        return None

    col_data = row_data["c"][column]
    if col_data == None:
        return None

    result = col_data["v"]
    return result

# Removes the specified directory if it exists.
def remove_dir_if_exists(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

# Creates the specified directory if it does not exist.
def make_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def copy_and_overwrite_with_closure(src_root_dir, dst_root_dir, closure):
    if src_root_dir == dst_root_dir:
        return

    for src_dir, dirs, files in os.walk(src_root_dir):
        dst_dir = src_dir.replace(src_root_dir, dst_root_dir, 1)

        make_dir_if_not_exists(dst_dir)

        for file in files:
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)

            if os.path.exists(dst_file):
                os.remove(dst_file)

            closure(src_file, dst_file)

def copy_and_overwrite(src_root_dir, dst_root_dir):
    copy_and_overwrite_with_closure(src_root_dir, dst_root_dir, shutil.copy)

def get_tag_row(data, tag):
    tag_column = 0
    max_rows = get_number_of_rows(data)
    for row in range(0, max_rows):
        cell = get_cell(data, row, tag_column)
        if str(cell) == tag:
            return row

    print "Missing tag: %s" % tag
    assert(False)

def get_language_column(data, language):
    language_row = 0
    max_columns = get_number_of_columns(data)
    for col in range(0, max_columns):
        cell = get_cell(data, language_row, col)
        if str(cell).lower() == language.lower():
            return col

    print "Missing language: %s" % language
    assert(False)

def generate_file_with_tag_and_language(data, path, tag, language, max_size):
    tag_row = get_tag_row(data, tag)
    language_col = get_language_column(data, language)
    content = get_cell(data, tag_row, language_col)
    check_and_generate_file(path, content, max_size)

def populate_ios_metadata(data, metadata_dir):
    for language_code, language_name in IOS_LANGUAGES_CODES.iteritems():            
        # Prepare language directory.
        language_dir = os.path.join(metadata_dir, language_code)
        make_dir_if_not_exists(language_dir)

        privacy_url_path   = os.path.join(language_dir, 'privacy_url.txt')
        marketing_url_path = os.path.join(language_dir, 'marketing_url.txt')
        support_url_path   = os.path.join(language_dir, 'support_url.txt')
        name_path          = os.path.join(language_dir, 'name.txt')
        keywords_path      = os.path.join(language_dir, 'keywords.txt')
        release_notes_path = os.path.join(language_dir, 'release_notes.txt')
        description_path   = os.path.join(language_dir, 'description.txt')
        
        # Write privacy_url, marketing_url, support_url files.
        generate_file(privacy_url_path,   PRIVACY_URL)
        generate_file(marketing_url_path, MARKETING_URL)
        generate_file(support_url_path,   SUPPORT_URL)
        
        # Write names, keywords, release notes, description
        generate_file_with_tag_and_language(data, name_path,          'ios_name',          language_name, 255)
        generate_file_with_tag_and_language(data, keywords_path,      'ios_keywords',      language_name, 100)
        generate_file_with_tag_and_language(data, release_notes_path, 'ios_release_notes', language_name, 4000)
        generate_file_with_tag_and_language(data, description_path,   'ios_description',   language_name, 4000)

def populate_android_metadata(data, metadata_dir):
    for language_code, language_name in ANDROID_LANGUAGES_CODES.iteritems():
        # Prepare language directory.
        language_dir = os.path.join(metadata_dir, language_code)
        make_dir_if_not_exists(language_dir)

        title_path             = os.path.join(language_dir, 'title.txt')
        short_description_path = os.path.join(language_dir, 'short_description.txt')
        full_description_path  = os.path.join(language_dir, 'full_description.txt')

        # Title, short description and full description.
        generate_file_with_tag_and_language(data, title_path,             'android_title',             language_name, 30)
        generate_file_with_tag_and_language(data, short_description_path, 'android_short_description', language_name, 80)
        generate_file_with_tag_and_language(data, full_description_path,  'android_full_description',  language_name, 4000)

        # Video
        video_tag_row = get_tag_row(data, 'android_video')
        video_tag_col = 2 # Fix column.
        video_cell = get_cell(data, video_tag_row, video_tag_col)
        if video_cell != None and len(video_cell) > 4:
            video_path = os.path.join(language_dir, 'video.txt')
            generate_file(video_path, video_cell)

        # Changelogs.
        version_codes_tag_row = get_tag_row(data, 'android_apk_version_codes')
        version_codes_tag_col = 2 # Fixed column
        version_codes_cell = get_cell(data, version_codes_tag_row, version_codes_tag_col)
        if version_codes_cell != None:
            changelogs_dir = os.path.join(language_dir, 'changelogs')
            make_dir_if_not_exists(changelogs_dir)

            # Iterate all version codes and generate the corresponding files.
            version_codes = version_codes_cell.split()
            for version_code in version_codes:
                version_code_path = os.path.join(changelogs_dir, version_code + '.txt')
                generate_file_with_tag_and_language(data, version_code_path, 'android_changelogs', language_name, 500)

# Populate metadata.
def populate_metadata(sheet_id, prj_dir, customized_dir, platform):
    print "populate metadata: sheet_id = %s prj_dir = %s customized_dir = %s platform = %s" % \
        (sheet_id, prj_dir, customized_dir, platform)

    metadata_dir = os.path.join(prj_dir, 'metadata')

    # Remove existing metadata directory.
    remove_dir_if_exists(metadata_dir)

    # Read sheet data.
    data = read_sheet_data(sheet_id)

    if platform == 'iOS':
        populate_ios_metadata(data, metadata_dir)
    elif platform == 'android':
        populate_android_metadata(data, metadata_dir)

    if customized_dir != None:
        copy_and_overwrite(customized_dir, metadata_dir)

def copy_image_or_convert_if_possible(src_path, dst_path):
    if src_path.endswith(".png"):
        # The current image is in PNG format.
        # Copy and convert to JPG format.                
        im = Image.open(src_path)
        new_dst_path = dst_path[:-3] + 'jpg'
        im.save(new_dst_path, "JPEG")
        print "Convert %s to %s" % (src_path, new_dst_path)
    elif src_path.endswith('.jpg'):
        # The current image is already in JPG format.
        # Copy directly.
        shutil.copyfile(src_path, dst_path)
        print "Copy %s to %s" % (src_path, dst_path)
    else:
        print "Ignore %s" % src_path

# populate screenshots, TODO: code for android
def populate_screenshots(screenshots_input_dir, prj_dir, customized_dir, platform):
    print "populate screenshots: screenshots_input_dir = %s prj_dir = %s customized_dir = %s platform = %s" % \
        (screenshots_input_dir, prj_dir, customized_dir, platform)

    temp_dir = os.path.join(prj_dir, 'screenshots_temp')

    remove_dir_if_exists(temp_dir)
    make_dir_if_not_exists(temp_dir)

    copy_and_overwrite_with_closure(screenshots_input_dir, temp_dir, copy_image_or_convert_if_possible)

    # Output screenshots directory.
    screenshots_dir = os.path.join(prj_dir, 'screenshots')

    # Remove existing screenshots dir.
    remove_dir_if_exists(screenshots_dir)
    
    for key, value in IOS_LANGUAGES_CODES.iteritems():
        # Prepare languages folders.
        language_dir = os.path.join(screenshots_dir, key)

        remove_dir_if_exists(language_dir)
        make_dir_if_not_exists(language_dir)

        copy_and_overwrite(temp_dir, language_dir)

    remove_dir_if_exists(temp_dir)

    if customized_dir != None:        
        make_dir_if_not_exists(temp_dir)

        copy_and_overwrite_with_closure(customized_dir, temp_dir, copy_image_or_convert_if_possible)
        copy_and_overwrite(temp_dir, screenshots_dir)

        remove_dir_if_exists(temp_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Metadata / screenshots.
    parser.add_argument(
        'populate_type',
        choices = ['metadata', 'screenshots']
    )

    # Platform.
    parser.add_argument(
        '-platform',
        nargs = 1,
        choices = ['android', 'iOS'],
        required = True        
    )

    # Project directory.
    parser.add_argument(
        '-prj-path',
        nargs = 1,
        required = True
    )

    # Input sheet for metadata.
    parser.add_argument(
        '-sheet-id',
        nargs = 1,
        required = False
    )

    # Customized directory for metadata.
    parser.add_argument(
        '-customized-metadata-path',
        nargs = 1,
        required = False,
        help = 'after populate metadata from xlsx data, will overwrite with this customized metadata'
    )

    # Input screenshots.
    parser.add_argument(
        '-screenshots-path',
        nargs = 1,
        required = False,
    )

    # Customized directory for screenshots.
    parser.add_argument(
        '-customized-screenshots-path',
        nargs = 1,
        required = False
    )

    args = parser.parse_args()

    platform                    = args.platform[0]
    project_path                = args.prj_path[0]
    populate_type               = args.populate_type

    sheet_id                    = args.sheet_id
    if args.customized_metadata_path == None:
        customized_metadata_path = None
    else:
        customized_metadata_path = args.customized_metadata_path[0]

    screenshots_path            = args.screenshots_path
    if args.customized_screenshots_path == None:
        customized_screenshots_path = None
    else:
        customized_screenshots_path = args.customized_screenshots_path[0]

    if populate_type == 'metadata':
        if sheet_id == None:
            dumpUsage()
            sys.exit()
        else:
            populate_metadata(sheet_id[0], project_path, customized_metadata_path, platform)

    elif populate_type == 'screenshots':
        if screenshots_path == None:
            dumpUsage()
            sys.exit()
        else:
            populate_screenshots(screenshots_path[0], project_path, customized_screenshots_path, platform)

    else:
        assert(False)
