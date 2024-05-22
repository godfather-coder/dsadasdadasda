

# <გარიგების_ტიპი>
def check_text1(text):
    keywords = ['ქირავდება დღიურად', 'ქირავდება', 'გირავდება', 'იყიდება', 'გაიცემა იჯარით']
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None
# </გარიგების_ტიპი>


# <მდგომარეობა>
def check_text2(text):
    keywords = ['ახალი აშენებული', 'ძველი აშენებული', 'მშენებარე',
                'ახალი გარემონტებული', 'ძველი გარემონტებული',
                'სარემონტო', 'შავი კარკასი', 'თეთრი კარკასი',
                'მიმდინარე რემონტი', 'მწვანე კარკასი']
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None

# <სახლი,აგარაკი>
def check_text(text):
    keywords = ['აგარაკი','სახლი','ბინა']
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None
# </სახლი,აგარაკი>

def map_producttype(word):
    mappings = {
        "ბინა": "1",
        "აგარაკი": "2",
        "სახლი": "2",


    }
    return mappings.get(word, "Unknown")


def get_estate_type_id(phrase):
    phrases_values = {
        'ძველი აშენებული': "3",
        'ახალი აშენებული': "1",
        'მშენებარე': "2",
    }

    return phrases_values.get(phrase)

def get_pr_type_from_string(text):
    phrases_values = {
        'იყიდება': 1,
        'გირავდება': 2,
        'ქირავდება': 3,
        'ქირავდება დღიურად': 7,
        'გაიცემა იჯარით': 8
    }

    for phrase, value in phrases_values.items():
        if phrase in text:
            return value
    return None


def decode_title(text):

    example = text
    lst = []

    garigeba = check_text1(text)
    lst.append(garigeba)
    example = example.replace(garigeba+' ','')

    mdgomareoba = check_text2(example)
    lst.append(mdgomareoba)
    if mdgomareoba is not None:
        example = example.replace(mdgomareoba + ' ', '')

    obieqti = check_text(example)
    lst.append(obieqti)
    if obieqti is not None:
        example = example.replace(obieqti + ' ', '')

    lst.append(example)


    return {
        'loc_urban_seo_title_ka': lst[-1],
        'loc_urban_seo_title_en': lst[-1],
        'loc_urban_seo_title_ru': lst[-1],
        "estate_type_id": get_estate_type_id(lst[1]),
        "product_type_id": map_producttype(lst[2]),
        "AdTypeID": str(get_pr_type_from_string(lst[0])),


    }


