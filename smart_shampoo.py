import requests
import json
import os
import urllib.parse
import html.parser
import lxml.html
import lxml.cssselect
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_srt( path ):
    timestamp = ''
    subtitle = ''

    skip_num_line = True
    subtitles = []
    with open( path, 'rt', encoding='UTF8' ) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line:                            # separation line
                if len( timestamp ) > 0 and len( subtitle ) > 0:
                    subtitles.append( ( timestamp, subtitle ) )
                    timestamp, subtitle, skip_num_line = '', '', True
            elif skip_num_line:                     # line num
                skip_num_line = False
            elif not timestamp:                     # timestamp
                timestamp = line
            else:                                   # subtitle
                subtitle = line if not subtitle else subtitle + '\n' + line

    if len( timestamp ) > 0 and len( subtitle ) > 0:
        subtitles.append( ( timestamp, subtitle ) )

    return subtitles


def read_txt( file_path ):
    subtitles = []
    with open( file_path, 'rt', encoding='UTF8' ) as file:
        subtitles = file.read().split( '\n\n' )

    return subtitles


def translate_file( file_path, source_lang, target_lang ):
    uri = 'https://translate.googleusercontent.com/translate_f'

    files = { 'file': (file_path, open(file_path, 'rb'), 'plan/text') }
    data = {
        'hl': (None, source_lang),
        'sl': (None, source_lang),
        'tl': (None, target_lang),
    }

    # print( requests.Request( 'POST', url=uri, files=data, headers=headers).prepare().body.decode('UTF-8') )
    r = requests.request('POST', verify=False, url=uri, files=files, data=data)

    if r.status_code != 200:
        return None

    tree = lxml.html.fromstring( r.text )
    pre = tree.cssselect( 'pre' )
    return html.parser.unescape( pre[0].text )


def write_srt( file_path, subtitles ):
    with open( file_path, 'w', encoding='UTF8' ) as file:
        line_num = 1
        NEW_LINE = '\n'
        for subtitle in subtitles:
            file.write( str(line_num) + NEW_LINE )
            file.write( subtitle[0] + NEW_LINE )
            file.write( subtitle[1] + NEW_LINE )
            file.write( NEW_LINE )
            line_num += 1


def write_txt( file_path, subtitles ):
    with open( file_path, 'w', encoding='UTF8' ) as file:
        NEW_LINE = '\n'
        for subtitle in subtitles:
            file.write( subtitle[1] + NEW_LINE )
            file.write( NEW_LINE )


def srt_to_txt( srt_path, txt_path ):
    subtitles = read_srt( srt_path )
    write_txt( txt_path, subtitles )


def txt_to_srt( txt_path, srt_path, subtitles ):
    translations = read_txt( txt_path )
    save_translated_srt( subtitles, translations )


def save_translated_srt( srt_path, subtitles, translations ):
    translated_subtitles = []
    if len( subtitles ) == len( translations ):
        for index in range( 0, len( subtitles ) ):
            subtitle = subtitles[index]
            translated_subtitles.append( ( subtitle[0], translations[index] ) )
            #print( index, subtitle[0], subtitle[1], translations[index] )
        write_srt( srt_path, translated_subtitles )
    else:
        print( '[SShampoo] error. size mismatch' )


def create_translated_srt( srt_path, source_lang, lanuages ):
    source_srt = srt_path
    source_lang = source_lang
    target_langs = lanuages
    temp_txt = 'temp.txt'
    srt_name = os.path.splitext( source_srt )[0]

    subtitles = read_srt( source_srt )
    write_txt( temp_txt, subtitles )

    srt_name_format = '{0}_{1}.srt'
    for target_lang in target_langs:
        target_srt_name = srt_name_format.format( srt_name, target_lang )
        translations = list( filter( None, translate_file( temp_txt, source_lang, target_lang ).split( '\r\n\r\n' ) ) )
        save_translated_srt( target_srt_name, subtitles, translations )
        print( '[SShampoo] {0} generated'.format( target_srt_name ) )
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # without dash(-) means positional arguments
    parser.add_argument('srt', metavar='source.srt', help='srt file path that you want to translate.')
    parser.add_argument('-sl', '--sl', metavar='ko', default='ko', help='language code of input srt file')
    parser.add_argument('-l', '--language', nargs='+', metavar='en zh-TW', default=['en', 'zh-TW'], help='language codes those you want to translate.')
    args = parser.parse_args()
    #args = parser.parse_args( ['db_kr.srt'] )

    if None == args.srt:
        print( 'Please, input srt file path. ex) python smart_shampoo.py source.srt' )
    else:
        create_translated_srt( args.srt, args.sl, args.language )
        print( '[SShampoo] Done!' )
    





