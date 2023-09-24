from __future__ import annotations

MISTA_ASIAKKAAT_COL = "Mistä asiakkaat ovat?"
IKA_COL = "Ikä"
KAUPUNKI_COL = "Kaupunki"
KIKY_COL = "Onko palkkasi nykyroolissasi mielestäsi kilpailukykyinen?"
KIKY_OTHER_COL = (
    "Onko palkkasi nykyroolissasi mielestäsi kilpailukykyinen? (muut vastaukset)"
)
KKPALKKA_COL = "Kuukausipalkka"
PALKANSAAJA_VAI_LASKUTTAJA_COL = "Palkansaaja vai laskuttaja"
PALVELUT_COL = "Palvelut"
ROOLI_COL = "Rooli"
SIIRTYNYT_COL = (
    "Oletko siirtynyt palkansaajasta laskuttajaksi tai päinvastoin 1.10.2022 jälkeen?"
)
SUKUPUOLI_COL = "Sukupuoli"
TYOAIKA_COL = "Työaika"
TYOKOKEMUS_COL = "Työkokemus alalta (vuosina)"
TYOPAIKKA_COL = "Työpaikka"
VUOSITULOT_COL = "Vuositulot"
MILLAISESSA_COL = "Millaisessa yrityksessä työskentelet?"
LAHITYO_COL = "Kuinka suuren osan ajasta teet lähityönä toimistolla?"
LANG_COL = "Vastauskieli"
KK_TULOT_COL = "Kk-tulot (laskennallinen)"
KK_TULOT_NORM_COL = "Kk-tulot (laskennallinen, normalisoitu)"
ROOLI_NORM_COL = "Rooli (normalisoitu)"

COLUMN_MAP_2023 = {
    "Timestamp": "Timestamp",
    "Oletko palkansaaja vai laskuttaja?": PALKANSAAJA_VAI_LASKUTTAJA_COL,
    "Oletko siirtynyt palkansaajasta laskuttajaksi tai päinvastoin 1.10.2022 jälkeen?": SIIRTYNYT_COL,
    "Ikä": "Ikä",
    "Sukupuoli": "Sukupuoli",
    "Työkokemus alalta (vuosina)": TYOKOKEMUS_COL,
    "Koulutustaustasi": "Koulutustaustasi",
    "Tulojen muutos viime vuodesta (%)": "Tulojen muutos viime vuodesta (%)",
    "Montako vuotta olet tehnyt laskuttavaa työtä alalla?": "Montako vuotta olet tehnyt laskuttavaa työtä alalla?",
    "Mitä palveluja tarjoat?": PALVELUT_COL,
    "Tuntilaskutus (ALV 0%, euroina)": "Tuntilaskutus (ALV 0%, euroina)",
    "Vuosilaskutus (ALV 0%, euroina)": "Vuosilaskutus (ALV 0%, euroina)",
    "Hankitko asiakkaasi itse suoraan vai käytätkö välitysfirmojen palveluita?": "Hankitko asiakkaasi itse suoraan vai käytätkö välitysfirmojen palveluita?",
    "Mistä asiakkaat ovat?": MISTA_ASIAKKAAT_COL,
    "Työpaikka": "Työpaikka",
    "Missä kaupungissa työpaikkasi pääasiallinen toimisto sijaitsee?": KAUPUNKI_COL,
    "Millaisessa yrityksessä työskentelet?": MILLAISESSA_COL,
    "Työaika": TYOAIKA_COL,
    "Kuinka suuren osan ajasta teet lähityönä toimistolla?": LAHITYO_COL,
    "Rooli / titteli": ROOLI_COL,
    "Kuukausipalkka (brutto, euroina)": KKPALKKA_COL,
    "Vuositulot (sis. bonukset, osingot yms, euroina)": VUOSITULOT_COL,
    "Vapaa kuvaus kokonaiskompensaatiomallista": "Vapaa kuvaus kokonaiskompensaatiomallista",
    "Onko palkkasi nykyroolissasi mielestäsi kilpailukykyinen?": KIKY_COL,
    "Vapaa sana": "Vapaa sana",
    "Palautetta kyselystä ja ideoita ensi vuoden kyselyyn": "Palautetta kyselystä ja ideoita ensi vuoden kyselyyn",
}

COLUMN_MAP_2023_EN_TO_FI = {
    "Timestamp": "Timestamp",
    "Employee or entrepreneur": "Oletko palkansaaja vai laskuttaja?",
    "Have you switched from employment to entrepreneurship or vice versa after 1.10.2022?": "Oletko siirtynyt palkansaajasta laskuttajaksi tai päinvastoin 1.10.2022 jälkeen?",
    "Age": "Ikä",
    "Gender": "Sukupuoli",
    "Relevant work experience from the industry (in years)": "Työkokemus alalta (vuosina)",
    "Education": "Koulutustaustasi",
    "Change in income from last year (in %)": "Tulojen muutos viime vuodesta (%)",
    "How many years have you worked as an entrepreneur in this industry?": "Montako vuotta olet tehnyt laskuttavaa työtä alalla?",
    "What services do you offer?": "Mitä palveluja tarjoat?",
    "Hourly rate (VAT 0%, in euros)": "Tuntilaskutus (ALV 0%, euroina)",
    "Yearly billing (VAT 0%, in euros)": "Vuosilaskutus (ALV 0%, euroina)",
    "Do you use agencies or find your clients yourself?": "Hankitko asiakkaasi itse suoraan vai käytätkö välitysfirmojen palveluita?",
    "Where are your clients from?": "Mistä asiakkaat ovat?",
    "Company": "Työpaikka",
    "In which city is your office?": "Missä kaupungissa työpaikkasi pääasiallinen toimisto sijaitsee?",
    "What kind of a company you work in?": "Millaisessa yrityksessä työskentelet?",
    "Full time / part time": "Työaika",
    "How much of your work time you spend in company office? (in %)": "Kuinka suuren osan ajasta teet lähityönä toimistolla?",
    "Role / title": "Rooli / titteli",
    "Monthly salary (gross, in EUR)": "Kuukausipalkka (brutto, euroina)",
    "Yearly income (incl. bonuses, etc; in EUR)": "Vuositulot (sis. bonukset, osingot yms, euroina)",
    "Free description of your compensation model": "Vapaa kuvaus kokonaiskompensaatiomallista",
    "Is your salary competitive?": "Onko palkkasi nykyroolissasi mielestäsi kilpailukykyinen?",
    "What was left unasked that you want to answer to?": "Vapaa sana",
    "Feedback of the survey": "Palautetta kyselystä ja ideoita ensi vuoden kyselyyn",
}

# ensure all columns have translations
assert set(COLUMN_MAP_2023.keys()) == set(COLUMN_MAP_2023_EN_TO_FI.values())

VALUE_MAP_2023_EN_TO_FI = {
    PALKANSAAJA_VAI_LASKUTTAJA_COL: {
        "Employee": "Palkansaaja",
        "Entrepreneur": "Laskuttaja",
    },
    SIIRTYNYT_COL: {
        "No": "Ei",
        "En": "Ei",
        "Kyllä, palkansaajasta laskuttajaksi": "palkansaaja → laskuttaja",
        "Kyllä, laskuttajasta palkansaajaksi": "laskuttaja → palkansaaja",
        "Yes, from employee to entrepreneur": "palkansaaja → laskuttaja",
        "Yes, from entrepreneur to employee": "laskuttaja → palkansaaja",
    },
    IKA_COL: {
        "< 15 yrs": "< 15v",
        "> 55 yrs": "> 55v",
    },
    MISTA_ASIAKKAAT_COL: {
        "Finland": "Suomesta",
    },
    KAUPUNKI_COL: {
        "PK-Seutu (Helsinki, Espoo, Vantaa)": "PK-seutu",
        "Capital region (Helsinki, Espoo, Vantaa)": "PK-seutu",
    },
    MILLAISESSA_COL: {
        "Product company with softaware as their core business": "Tuotetalossa, jonka core-bisnes on softa",
    },
}

BOOLEAN_TEXT_TO_BOOLEAN_MAP = {
    "Kyllä": True,
    "Ei": False,
    "Yes": True,
    "No": False,
}

COMPANY_MAP = {
    "Mavericks Software": "Mavericks",
    "Mavericks: a Witted company": "Mavericks",
    "Netum Groupj": "Netum",
    "Siili Solutions": "Siili",
    "Vincitj": "Vincit",
}

FULL_STACK_ROLE = "*Full-stack Developer"
SENIOR_DEVELOPER_ROLE = "*Senior Developer"
DEVOPS_CONSULTANT_ROLE = "*Devops Consultant"

ROLE_MAP = {
    "DevOps Consult": DEVOPS_CONSULTANT_ROLE,
    "DevOps Consultant": DEVOPS_CONSULTANT_ROLE,
    "Devops consultant": DEVOPS_CONSULTANT_ROLE,
    "Devops konsultti": DEVOPS_CONSULTANT_ROLE,
    "Full Stack": FULL_STACK_ROLE,
    "Full stack developer": FULL_STACK_ROLE,
    "Full stack engineer": FULL_STACK_ROLE,
    "Full stack web developer": FULL_STACK_ROLE,
    "Full-stack Developer": FULL_STACK_ROLE,
    "Full-stack developer": FULL_STACK_ROLE,
    "Full-stack kehittäjä": FULL_STACK_ROLE,
    "Full-stack ohjelmistokehittäjä": FULL_STACK_ROLE,
    "Full-stack software developer": FULL_STACK_ROLE,
    "Full-stack web developer": FULL_STACK_ROLE,
    "Full-stack-kehittäjä": FULL_STACK_ROLE,
    "Fullstack developer": FULL_STACK_ROLE,
    "Fullstack web developer": FULL_STACK_ROLE,
    "Fullstack": FULL_STACK_ROLE,
    "Ohjelmistokehittäjä (full-stack)": FULL_STACK_ROLE,
    "Ohjelmistokehittäjä, full-stack": FULL_STACK_ROLE,
    "Senior developer": SENIOR_DEVELOPER_ROLE,
    "Senior software developer": SENIOR_DEVELOPER_ROLE,
    "Software engineer, fullstack": FULL_STACK_ROLE,
    "Full-stack cloud developer": FULL_STACK_ROLE,
    "Fullstack developer, web apps": FULL_STACK_ROLE,
}
NO_GENDER_VALUES = {
    "-",
    "ei liity asiaan",
    "epärelevantti",
    "jänis",
    "kyllä, kiitos",
    "leppäkerttu",
    "taisteluhelikopteri",
    "tihkutympönen",
    "yes",
}
OTHER_GENDER_VALUES = {
    "muu",
    "muu/ei",
    "non-binary, afab",
}
