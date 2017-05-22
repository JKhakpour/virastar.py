#coding:utf-8
#virastar version 0.0.1

from __future__ import unicode_literals

import re
import sys

    

class PersianEditor:
    default_options = {
        "fix_dashes": True,
        "fix_three_dots": True,
        "fix_english_quotes": True,
        "fix_hamzeh": True,
        "cleanup_zwnj": True,
        "fix_spacing_for_braces_and_quotes": True,
        "fix_arabic_numbers": True,
        "fix_english_numbers": True,
        "fix_misc_non_persian_chars": True,
        "fix_perfix_spacing": True,
        "fix_suffix_spacing": True,
        "aggresive": True,
        "cleanup_kashidas": True,
        "cleanup_extra_marks": True,
        "cleanup_spacing": True,
        "cleanup_begin_and_end": True
    }
    
    def __init__(self, custom_options = {}):
        self.options = self.default_options.copy()
        self.options.update(custom_options)
        
    def tr(self, intab, outtab, txt):
        return txt.translate( {ord(k):v for k,v in zip(intab, outtab)})
        
    def cleanup(self, text):
        # removing URLS bringing them back at the end of process
        urls = []
        urls_pattern = re.compile(r"((http|https):\/\/[-\w\.]+(:\d+)?(\/([\w\/_\.]*(\?\S+)?)?)?)")
        for matched_url in urls_pattern.findall(text):
            text = text.replace(matched_url[0], u"__URL__PLACEHOLDER__".format(len(urls)))
            urls.append(matched_url[0])

        # replace double dash to ndash and triple dash to mdash
        if self.options['fix_dashes']:
            text = re.sub(r"-{3}",'—', text)
            text = re.sub(r"-{2}",'–', text)

        # replace three dots(or more) with ellipsis
        if self.options['fix_three_dots']:
            text = re.sub(r"""\s*\.{3,}""", u'…', text) 

        # replace English quotes with their Persian equivalent
        if self.options['fix_english_quotes']:
            text = re.sub(r"""(["'`]+)(.+?)(\1)""", ur'«\2»', text) 

        # should convert ه ی to ه
        if self.options['fix_hamzeh']:
            text = re.sub(r"""(\S)(ه[\s‌]+[یي])(\s)""", ur'\1هٔ\3', text, flags=re.UNICODE) 

        # remove unnecessary zwnj char that are succeeded/preceded by a space
        if self.options['cleanup_zwnj']:
            text = re.sub(r"""\s+‌|‌\s+""", r' ', text) 

        # character replacement
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        arabic_numbers  = "١٢٣٤٥٦٧٨٩٠"
        english_numbers = "1234567890"
        bad_chars  = ",;كي%"
        good_chars = "،؛کی٪"
        if self.options['fix_english_numbers']:
            text = self.tr(english_numbers, persian_numbers, text)
        if self.options['fix_arabic_numbers']:
            text = self.tr(arabic_numbers,persian_numbers, text)
        if self.options['fix_misc_non_persian_chars']:
            text = self.tr(bad_chars,good_chars, text)

        # should not replace exnglish chars in english phrases
        eng_char_eng_num = re.compile(r"""([a-zA-Z\-_]{2,}[۰-۹]+|[۰-۹]+[a-zA-Z\-_]{2,})""", re.IGNORECASE)
        for en_phrase in eng_char_eng_num.findall(text):
            text = text.replace(en_phrase, self.tr(persian_numbers,english_numbers, en_phrase))

        # put zwnj between word and prefix (mi* nemi*)
        # there's a possible bug here: می and نمی could be separate nouns and not prefix
        if self.options['fix_perfix_spacing']:
            text = re.sub(r"""\s+(ن?می)\s+""", ur' \1‌', text)

        # put zwnj between word and suffix (*tar *tarin *ha *haye)
        # there's a possible bug here: های and تر could be separate nouns and not suffix
        if self.options['fix_suffix_spacing']:
            text = re.sub(r"""\s+(تر(ی(ن)?)?|ها(ی)?)\s+""", r'‌\1 ', text) # in case you can not read it: \s+(tar(i(n)?)?|ha(ye)?)\s+

        # -- Aggressive Editing ------------------------------------------
        if self.options['aggresive']:
            # replace more than one ! or ? mark with just one
            if self.options['cleanup_extra_marks']:
              text = re.sub(r"""(!){2,}""", r'\1', text)
              text = re.sub(r"""(؟){2,}""", r'\1', text)

            # should remove all kashida
            if self.options['cleanup_kashidas']:
                text = re.sub(r"""ـ+""","", text) 

        # ----------------------------------------------------------------

        # should fix outside and inside spacing for () [] {}  “” «»
        if self.options['fix_spacing_for_braces_and_quotes']:
            text = re.sub(r"""[ \t‌]*(\()\s*([^)]+?)\s*?(\))[ \t‌]*""", r' \1\2\3 ', text)
            text = re.sub(r"""[ \t‌]*(\[)\s*([^\]]+?)\s*?(\])[ \t‌]*""", r' \1\2\3 ', text)
            text = re.sub(r"""[ \t‌]*(\{)\s*([^}]+?)\s*?(\})[ \t‌]*""", r' \1\2\3 ', text)
            text = re.sub(r"""[ \t‌]*(“)\s*([^”]+?)\s*?(”)[ \t‌]*""", r' \1\2\3 ', text)
            text = re.sub(r"""[ \t‌]*(«)\s*([^»]+?)\s*?(»)[ \t‌]*""", r' \1\2\3 ', text)

        # : ; , . ! ? and their persian equivalents should have one space after and no space before
        if self.options['fix_spacing_for_braces_and_quotes']:
            text = re.sub(r"""[ \t‌]*([:;,؛،.؟!]{1})[ \t‌]*""", r'\1 ', text)
            # do not put space after colon that separates time parts
            text = re.sub(r"""([۰-۹]+):\s+([۰-۹]+)""", r'\1:\2', text)

        # should fix inside spacing for () [] {}  “” «»
        if self.options['fix_spacing_for_braces_and_quotes']:
            text = re.sub(r"""(\()\s*([^)]+?)\s*?(\))""", r'\1\2\3', text)
            text = re.sub(r"""(\[)\s*([^\]]+?)\s*?(\])""", r'\1\2\3', text)
            text = re.sub(r"""(\{)\s*([^}]+?)\s*?(\})""", r'\1\2\3', text)
            text = re.sub(r"""(“)\s*([^”]+?)\s*?(”)""", r'\1\2\3', text)
            text = re.sub(r"""(«)\s*([^»]+?)\s*?(»)""", r'\1\2\3', text)

        # should replace more than one space with just a single one
        if self.options['cleanup_spacing']:
            text = re.sub(r"""[ ]+""", r' ', text)
            text = re.sub(r"""([\n]+)[ \t‌]*""", r'\1', text)

        # remove spaces, tabs, and new lines from the beginning and enf of file
        if self.options['cleanup_begin_and_end']:
            text = text.strip()

        # bringing back urls
        for i, url in enumerate(urls):
            text = text.replace("__URL__PLACEHOLDER__", urls[i], 1)
        self.cleaned_text = text
        return text