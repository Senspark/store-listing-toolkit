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

def dumpUsage():
    print "usage:   ./populate (metadata|screenshots) -platform <platform> -prj-path <prj-path> <parameters>"
    print "\n"
    print "metadata command parameters"
    print "         -data-file-path <data-file-path>            xlsx data file path"
    print "         [-customized-metadata-path <customized-metadata-path>]"
    print "                                                     after populate metadata from xlsx data, will overwrite with this customized metadata"
    print "sample:  ./populate.py metadata -platform iOS -prj-path . -data-file-path ../src/data.xlsx -customized-metadata-path ../src/itunes/metadata"
    print "\n"
    print "screenshots command parameters"
    print "         -screenshots-path <screenshots-path>        screenshots path"
    print "         [-customized-screenshots-path <customized-screenshots-path>]"                                                                                                                    
    print "sample:  ./populate.py screenshots -platform android -prj-path . -screenshots-path ../src/screenshots -customized-screenshots-path"

def genFile(path, content):
    print path
    file = open(path, 'w')
    file.write(content)
    file.close()

def checkAndGenFile(path, content, max):
    if len(content) > max:
        print "%s is too long and greater than %d characters: %d" % (path, max, len(content))
        #sys.exit()
    genFile(path, content.encode('utf-8'))

def read_sheet_data(sheet_id):
    sheet_url = "http://docs.google.com/spreadsheets/d/%s/gviz/tq?&tq&gid=0&pref=2&pli=1" % sheet_id
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

def get_cell(data, row, column):
    # Convert 1-indexed to zero-indexed.
    row = row - 1
    column = column - 1

    table = data["table"]

    row_data = table["rows"][row]
    if row_data == None:
        return None

    col_data = row_data["c"][column]
    if col_data == None:
        return None

    result = col_data["v"]
    return result

def remove_dir_if_exists(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

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

# Populate metadata.
def populate_metadata(sheet_id, prj_dir, customized_dir, platform):
    print "populate metadata: sheet_id = %s prj_dir = %s customized_dir = %s platform = %s" % \
        (sheet_id, prj_dir, customized_dir, platform)

    metadata_dir = os.path.join(prj_dir, 'metadata')

    # Remove existing metadata directory.
    remove_dir_if_exists(metadata_dir)

    # Read sheet data.
    data = read_sheet_data(sheet_id)

    if platform.lower() =='ios':
        for key, value in IOS_LANGUAGES_CODES.iteritems():
            
            # Prepare language directory.
            language_dir = os.path.join(metadata_dir, key)

            # Create language directory.
            make_dir_if_not_exists(language_dir)
            
            # Write privacy_url, marketing_url, support_url files.
            genFile(os.path.join(language_dir, 'privacy_url.txt'), PRIVACY_URL)
            genFile(os.path.join(language_dir, 'marketing_url.txt'), MARKETING_URL)
            genFile(os.path.join(language_dir, 'support_url.txt'), SUPPORT_URL)
            
            # Check loading excel file
            # Print sheet.cell(row = 1, column = 2).value + " "
            
            # Write names, keywords, release notes, description
            foundLang = False
            for i in range(2, 29):
                if str(get_cell(data, row=1, column=i)).lower() == value.lower():
                    foundLang = True
                    checkAndGenFile(os.path.join(language_dir, 'name.txt'),          get_cell(data, row=2, column=i), 255)
                    checkAndGenFile(os.path.join(language_dir, 'keywords.txt'),      get_cell(data, row=4, column=i), 100)
                    checkAndGenFile(os.path.join(language_dir, 'release_notes.txt'), get_cell(data, row=5, column=i), 4000)
                    checkAndGenFile(os.path.join(language_dir, 'description.txt'),   get_cell(data, row=7, column=i), 4000)

            if not foundLang:
                print "Not found data for language %s %" % (value, key)
                sys.exit()
                     
    elif platform == 'android':
        for key, value in ANDROID_LANGUAGES_CODES.iteritems():

            # Prepare language directory.
            language_dir = os.path.join(metadata_dir, key)

            # Create language directory.
            make_dir_if_not_exists(language_dir)
                
            #write privacy_url, marketing_url, support_url files
            if len(get_cell(data, row=8, column=2)) > 4:
                genFile(os.path.join(language_dir, 'video.txt'), get_cell(data, row=8, column=2))
            
            #check loading excel file
            #print sheet.cell(row = 1, column = 2).value + " "
            
            #write title, short description, full description
            foundLang = False
            for i in range(2, 69):
                if str(get_cell(data, row=1, column=i)).lower() == value.lower(): # find the language in excel data
                    foundLang = True
                     
                    # Title.
                    if len(get_cell(data, row=2, column=i))<=30:
                        checkAndGenFile(os.path.join(language_dir, 'title.txt'), get_cell(data, row=2, column=i), 30)
                    else:
                        checkAndGenFile(os.path.join(language_dir, 'title.txt'), get_cell(data, row=3, column=i), 30)

                    # Short description and full description.
                    checkAndGenFile(os.path.join(language_dir, 'short_description.txt'), get_cell(data, row=6, column=i), 80)
                    checkAndGenFile(os.path.join(language_dir, 'full_description.txt'),  get_cell(data, row=7, column=i), 4000)

                    # Changelogs.
                    if get_cell(data, row=9, column=2) != "": # write changelog for android
                        changelog_dir = os.path.join(language_dir, 'changelogs')                        
                        make_dir_if_not_exists(changelog_dir)
                            
                        verCodes = str(get_cell(data, row=9, column=2)).split()
                        for verCode in verCodes:
                            checkAndGenFile(os.path.join(changelog_dir, verCode + '.txt'), get_cell(data, row=5, column=i), 500)

            if not foundLang:
                print "Not found data for language %s %" % (value, key)
                sys.exit()

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
