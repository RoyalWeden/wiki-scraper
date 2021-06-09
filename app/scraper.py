import requests
from app.constants import STOPWORDS, DEFAULT_WEBSITE


class Scraper:
    def __init__(self, website=DEFAULT_WEBSITE):
        """Creates a Scraper object with a website.

            Args:
                website (str): Wikipedia website [if none inputted, uses default websites].
        """
        self.website = website
        self.wiki_request = requests.get(self.website)
        self.wiki_text = self.wiki_request.text

    def get_main_title(self):
        """Returns the main title of the wikipedia page.

            Returns:
                wiki_main_title (str): String that contains the main title
        """
        wiki_main_title = self.wiki_text[self.wiki_text.find("<h1 id=\"firstHeading\" class=\"firstHeading\" >")+len("<h1 id=\"firstHeading\" class=\"firstHeading\" >"):self.wiki_text.find("</h1>")]
        return wiki_main_title

    def get_titles(self):
        """Returns all the sub titles of the wikipedia page.

            Returns:
                wiki_titles (list): List of strings, each string being a title.
        """
        titles_find_start_ind = self.wiki_text.find("<div id=\"toc\" class=\"toc\" role=\"navigation\" aria-labelledby=\"mw-toc-heading\"><input type=\"checkbox\" role=\"button\" id=\"toctogglecheckbox\" class=\"toctogglecheckbox\" style=\"display:none\" /><div class=\"toctitle\" lang=\"en\" dir=\"ltr\"><h2 id=\"mw-toc-heading\">Contents</h2><span class=\"toctogglespan\"><label class=\"toctogglelabel\" for=\"toctogglecheckbox\"></label></span></div>")
        titles_find_start_ind += len("<div id=\"toc\" class=\"toc\" role=\"navigation\" aria-labelledby=\"mw-toc-heading\"><input type=\"checkbox\" role=\"button\" id=\"toctogglecheckbox\" class=\"toctogglecheckbox\" style=\"display:none\" /><div class=\"toctitle\" lang=\"en\" dir=\"ltr\"><h2 id=\"mw-toc-heading\">Contents</h2><span class=\"toctogglespan\"><label class=\"toctogglelabel\" for=\"toctogglecheckbox\"></label></span></div>")
        which_title = 1
        wiki_titles = []
        while self.wiki_text.find("<span class=\"toctext\">".format(which_title), titles_find_start_ind) != -1:
            titles_find_start_ind = self.wiki_text.find("<span class=\"toctext\">".format(which_title), titles_find_start_ind) + len("<span class=\"toctext\">".format(which_title))
            wiki_titles.append(str(self.wiki_text[titles_find_start_ind:self.wiki_text.find("</span>", titles_find_start_ind)]))
            which_title += 1
        return wiki_titles

    def find_most_frequent_words(self, section):
        """Returns the most frequent words in the section.

            Args:
                section (str): Title of a section

            Returns:
                 freq_words (list): List of the five most frequent words
        """
        section_start = self.wiki_text.find("<span class=\"mw-headline\" id=\"{0}\">{0}".format(section))
        paragraph_start = self.wiki_text.find("<p>", section_start) + len("<p>")
        paragraph_end = self.wiki_text.find("<h", paragraph_start)
        paragraph = self.wiki_text[paragraph_start:paragraph_end]
        count = 0
        # Remove html content from paragraph
        while paragraph.__contains__("<") and count < 5000:
            count += 1
            html_removal_start = paragraph.find("<")
            html_removal_end = paragraph.find(">", html_removal_start) + len(">")
            if html_removal_start > 0:
                paragraph = paragraph[:html_removal_start] + paragraph[html_removal_end:]
            else:
                paragraph = paragraph[html_removal_end:]
        count = 0
        # Remove codes from paragraph
        while paragraph.__contains__("&#") and count < 1000:
            count += 1
            code_removal_start = paragraph.find("&#")
            code_removal_end = paragraph.find(";", code_removal_start) + len(";")
            if code_removal_start > 0:
                paragraph = paragraph[:code_removal_start] + " " + paragraph[code_removal_end:]
                if paragraph.__contains__("  "):
                    paragraph = paragraph[:paragraph.find("  ")] + paragraph[paragraph.find("  ") + len("  ") - 1:]
            else:
                paragraph = paragraph[code_removal_end:]
        count = 0
        # Remove commas and periods
        while (paragraph.__contains__(",") or paragraph.__contains__(".")) and count < 1000:
            count += 1
            comma_removal_start = paragraph.find(",")
            comma_removal_end = comma_removal_start + len(",")
            period_removal_start = paragraph.find(".")
            period_removal_end = period_removal_start + len(".")
            if comma_removal_start < period_removal_start:
                if comma_removal_start > 0:
                    paragraph = paragraph[:comma_removal_start] + paragraph[comma_removal_end:]
                else:
                    paragraph = paragraph[comma_removal_end:]
            else:
                if period_removal_start > 0:
                    paragraph = paragraph[:period_removal_start] + paragraph[period_removal_end:]
                else:
                    paragraph = paragraph[period_removal_end:]
        count = 0
        # Goes through whole paragraph to remove any non alphabetic or space characters
        temp_paragraph = ""
        while count < len(paragraph):
            if paragraph[count].isalpha() or paragraph[count].isspace():
                temp_paragraph += paragraph[count]
            count += 1
        paragraph = temp_paragraph.lower()
        split_words = paragraph.split(' ')
        # Fix newline combined words
        for word in split_words:
            if word.__contains__("\n"):
                both_words = word.split("\n")
                split_words.remove(word)
                if not STOPWORDS.__contains__(both_words[0]):
                    split_words.append(both_words[0])
                if not STOPWORDS.__contains__(both_words[1]):
                    split_words.append(both_words[1])
        # Remove empty strings in list
        while split_words.__contains__(''):
            split_words.remove('')
        # Remove "stop words"
        for i in range(len(split_words)-1, -1, -1):
            if STOPWORDS.__contains__(split_words[i]):
                split_words.pop(i)
        # Create frequency dictionary
        frequency_dict = {}
        for word in split_words:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
        frequency_dict = dict(sorted(frequency_dict.items(), key=lambda x: -x[1]))

        return list(frequency_dict)[:5]

# print("MAIN TITLE:\t" + str(get_main_title()))
# print("TITLES:\t" + str(get_titles()))


# print("\n-----TEXT------\n\n" + wiki_request.text)
