# -*- encoding: utf-8 -*-


from __future__ import unicode_literals
import unittest
import virastar
from config import configs

class VirastarTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_replace_Arabic_kaf(self):
       pe = virastar.PersianEditor()
       test = "ك" 
       test2 = "كمك"
       result = "ک"
       result2 = "کمک"
       self.assertEqual(pe.cleanup(test),result, "should replace Arabic Kaf with its Persian equivalent")
       self.assertEqual(pe.cleanup(test2),result2, "should replace Arabic kaf  with its Persian equivalent")
    
    def test_replace_Arabic_Yeh(self):
       """should replace Arabic Yeh with its Persian equivalent"""
       pe = virastar.PersianEditor()
       test = "ي"
       test2 = "بيني"
       result = "ی"
       result2 = "بینی"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)
   

    def test_replace_Arabic_numbers(self):
       """should replace Arabic numbers with their Persian equivalent"""
       pe = virastar.PersianEditor()
       test   = "٠١٢٣٤٥٦٧٨٩"
       result = "۰۱۲۳۴۵۶۷۸۹"
       self.assertEqual(pe.cleanup(test),result)


    def test_replace_English_numbers(self):
       """should replace English numbers with their Persian equivalent"""
       pe = virastar.PersianEditor()
       test   = "0123456789"
       result = "۰۱۲۳۴۵۶۷۸۹"
       self.assertEqual(pe.cleanup(test),result)


    def test_replace_English_comma_and_semicolon(self):
       """should replace English comma and semicolon with their Persian equivalent"""
       pe = virastar.PersianEditor()
       test   = ";,"
       result = "؛ ،"
       self.assertEqual(pe.cleanup(test),result)


    def test_correct_pnctuation_spacing(self):
       """should correct :;,.?! spacing (one space after and no space before)"""
       pe = virastar.PersianEditor()
       test   = "گفت : سلام"
       result = "گفت: سلام"
       test2 = "salam.\n\nkhoobi"
       result2 = "salam. \n\nkhoobi"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)
    

    def test_replace_English_quotes(self):
        """should replace English quotes with their Persian equivalent"""
        pe = virastar.PersianEditor()
        test  = "''تست''"
        test2 = "'تست'"
        test3 = "\"گفت: سلام\""
        test4 = "`تست`"
        test5 = "``تست``"
        result = result2 = result4 = result5 = "«تست»"
        result3 = "«گفت: سلام»"
        # not greedy
        test6 = '"this" or "that"'
        result6 = '«this» or «that»'
        self.assertEqual(pe.cleanup(test),result)
        self.assertEqual(pe.cleanup(test2),result2)
        self.assertEqual(pe.cleanup(test3),result3)
        self.assertEqual(pe.cleanup(test4),result4)
        self.assertEqual(pe.cleanup(test5),result5)
        self.assertEqual(pe.cleanup(test6),result6)
    

    def test_replace_three_dots(self):
        """should replace three dots with ellipsis"""
        pe = virastar.PersianEditor()
        test    = "..."
        result  = "…"
        test2   = "...."
        result2 = "…"
        test3   = "خداحافظ ... به به"
        result3 = "خداحافظ… به به"
        test4   = "........."
        result4 = "…"
        self.assertEqual(pe.cleanup(test),result)
        self.assertEqual(pe.cleanup(test2),result2)
        self.assertEqual(pe.cleanup(test3),result3)
        self.assertEqual(pe.cleanup(test4),result4)


    def test_convert_yeh_and_heh(self):
        u"should convert ه ی to هٔ"
        pe = virastar.PersianEditor()
        test = "خانه ی ما"
        test2 = "خانه ی ما"
        test3 = "خانه ي ما"
        result = result2 = result3 = "خانهٔ ما"
        self.assertEqual(pe.cleanup(test),result)
        self.assertEqual(pe.cleanup(test2),result2)
        self.assertEqual(pe.cleanup(test3),result3)
    

    def test_replace_double_triple_dash(self):
       """should replace double dash to ndash and triple dash to mdash"""
       pe = virastar.PersianEditor()
       test    = "--"
       test2   = "---"
       result  = "–"
       result2 = "—"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)


    def test_remove_duplicate_space(self):
       """should replace more than one space with just a single one"""
       pe = virastar.PersianEditor()
       test   = "  hello   world!  I'm virastar   "
       result = "hello world! I'm virastar"
       self.assertEqual(pe.cleanup(test),result)


    def test_remove_unnecessary_zwnj_and_space(self):
       """should remove unnecessary zwnj chars that are succeeded/preceded by a space"""
       pe = virastar.PersianEditor()
       test = "سلام‌ دنیا" # before
       result = "سلام دنیا"
       test2 = "سلام ‌دنیا" #after
       result2 = "سلام دنیا"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)


    def test_fix_spacing_for_braces(self):
       u"""should fix spacing for () [] {}  “” «» (one space outside, no space inside)"""    
       pe = virastar.PersianEditor()        
       # matched brackets
       pass
       for pair in [ ["(",")"],["[","]"],["{","}"],["“","”"],["«","»"] ]:
           test  = "this is{} a test{}".format(*pair)
           test2 = "this is {} a test  {}".format(*pair)
           test3 = "this is  {}  a test {}  yeah!".format(*pair)
           test4 = "this is   {}a test {}  yeah!".format(*pair)
           result  = "this is {}a test{}".format(*pair)
           result2 = "this is {}a test{}".format(*pair)
           result3 = "this is {}a test{} yeah!".format(*pair)
           result4 = "this is {}a test{} yeah!".format(*pair)
           self.assertEqual(pe.cleanup(test),result)
           self.assertEqual(pe.cleanup(test2),result2)
           self.assertEqual(pe.cleanup(test3),result3)
           self.assertEqual(pe.cleanup(test4),result4)
           
       #mismatched brackets
       for pair in [ ["(","]"],["[",")"],["{","”"],["(","}"],["«","]"] ]:
         test  = "mismatched brackets{} don't apply{}".format(*pair)
         test2 = "mismatched brackets {} don't apply {}".format(*pair)
         test3 = "mismatched brackets {} don't apply {} yeah!".format(*pair)
         test4 = "mismatched brackets {}don't apply {} yeah!".format(*pair)
         self.assertEqual(pe.cleanup(test),test)
         self.assertEqual(pe.cleanup(test2),test2)
         self.assertEqual(pe.cleanup(test3),test3)
         self.assertEqual(pe.cleanup(test4),test4)




    def test_replace_English_percent_sig(self):
       """should replace English percent sign to its Persian equivalent"""
       pe = virastar.PersianEditor()
       test = "%"
       result = "٪"
       self.assertEqual(pe.cleanup(test),result)


    def test_replace_multiple_line_breaks(self):
       """should replace more that one line breaks with just one"""
       pe = virastar.PersianEditor()
       test    = "this is \n \n \n     \n a test"
       result  = "this is \n\n\n\na test"
       test2   = "this is\n\n\n\na test"
       result2 = "this is\n\n\n\na test"
       test3   = "this is \n\n\n    a test"
       result3 = "this is \n\n\na test"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)
       self.assertEqual(pe.cleanup(test3),result3)


    def test_not_replace_line_breaks(self):
       """should not replace line breaks and should remove spaces after line break"""
       pe = virastar.PersianEditor()
       test  = "this is \n  a test"
       result = "this is \na test"
       self.assertEqual(pe.cleanup(test),result)


    def test_put_zwnj_between_word_and_suffix(self):
       """should put zwnj between word and prefix/suffix (ha haye* tar* tarin mi* nemi*)"""
       pe = virastar.PersianEditor()
       test    = "ما می توانیم"
       result  = "ما می‌توانیم"
       test2   = "ما نمی توانیم"
       result2 = "ما نمی‌توانیم"
       test3   = "این بهترین کتاب ها است"
       result3 = "این بهترین کتاب‌ها است"
       test4   = "بزرگ تری و قدرتمند ترین زبان های دنیا"
       result4 = "بزرگ‌تری و قدرتمند‌ترین زبان‌های دنیا"
       self.assertEqual(pe.cleanup(test),result)


    def test_not_replace_English_words_numbers(self):
        """should not replace English numbers in English phrases"""
        pe = virastar.PersianEditor()
        test = "عزیز ATM74 در IBM-96 085 B 95BCS"
        result = "عزیز ATM74 در IBM-96 ۰۸۵ B 95BCS"
        self.assertEqual(pe.cleanup(test),result)
  

    def test_not_create_spacing_sometimes(self):
        """should not create spacing for something like (,)"""
        pe = virastar.PersianEditor()
        test = "this is (,) comma"
        result = "this is (،) comma"
        self.assertEqual(pe.cleanup(test),result)
   

    def test_not_puts_space_after_time_colon(self):
       """should not puts space after time colon separator"""
       pe = virastar.PersianEditor()
       test = "12:34"
       result = "۱۲:۳۴"
       self.assertEqual(pe.cleanup(test),result)


    def test_not_destroy_URLs(self):
       """should not destroy URLs"""      
       pe = virastar.PersianEditor()
       test = "http://virastar.heroku.com"
       result = "http://virastar.heroku.com"
       test2 = "http://virastar.heroku.com\nhttp://balatarin.com"
       result2 = "http://virastar.heroku.com\nhttp://balatarin.com"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)


    def test_not_replace_line_breaks_when_the_line_ends_with_quotes(self):
       """should not replace line breaks when the line ends with quotes"""
       pe = virastar.PersianEditor()
       test = "salam \"khoobi\" \n chetori"
       result = "salam «khoobi» \nchetori"
       self.assertEqual(pe.cleanup(test),result)


    def test_not_put_space_afterbackets_before_punctuations(self):
       """should not put space after quotes, {}, () or [] if there's ,.; just after that"""
       pe = virastar.PersianEditor()
       test = "«This», {this}, (this), [this] or {this}. sometimes (this)."
       result = "«This»، {this}، (this)، [this] or {this}. sometimes (this)."
       self.assertEqual(pe.cleanup(test),result)


    def test_convert_numbers_with_dashes(self):
       """should be able to convert numbers with dashes"""
       pe = virastar.PersianEditor()
       test = "1- salam"
       result = "۱- salam"
       self.assertEqual(pe.cleanup(test),result)


    def test_remove_duplicate_onepunctuation_mark(self):
       """aggressive editing: should replace more than one ! or ? mark with just one"""      
       pe = virastar.PersianEditor()
       test    = "salam!!!"
       result  = "salam!"
       test2   = "چطور؟؟؟"
       result2 = "چطور؟"
       self.assertEqual(pe.cleanup(test),result)
       self.assertEqual(pe.cleanup(test2),result2)


    def test_remove_all_kashida(self):
       """aggressive editing: should remove all kashida"""      
       pe = virastar.PersianEditor()
       test   = "سلامـــت"
       result = "سلامت"
       self.assertEqual(pe.cleanup(test),result)
    
   

if __name__ == '__main__':
    unittest.main()