from __future__ import annotations

IKA_COL = "Ikä"
KAUPUNKI_COL = "Kaupunki"
KIKY_COL = "Onko palkkasi nykyroolissasi mielestäsi kilpailukykyinen?"
KKPALKKA_COL = "Kuukausipalkka"
KK_TULOT_COL = "Kk-tulot (laskennallinen)"
KK_TULOT_NORM_COL = "Kk-tulot (laskennallinen, normalisoitu)"
LAHITYO_COL = "Kuinka suuren osan ajasta teet lähityönä toimistolla?"
LANG_COL = "Vastauskieli"
MILLAISESSA_COL = "Millaisessa yrityksessä työskentelet?"
MISTA_ASIAKKAAT_COL = "Mistä asiakkaat ovat?"
PALAUTE_COL = "Palaute"
PALKANSAAJA_VAI_LASKUTTAJA_COL = "Palkansaaja vai laskuttaja"
PALVELUT_COL = "Palvelut"
ROOLI_COL = "Rooli"
ROOLI_NORM_COL = "Rooli (normalisoitu)"
SIIRTYNYT_COL = "Siirtynyt palkansaaja/laskuttaja"
SUKUPUOLI_COL = "Sukupuoli"
TUNTILASKUTUS_ALV0_COL = "Tuntilaskutus (ALV 0%, euroina)"
TYOAIKA_COL = "Työaika"
TYOKOKEMUS_COL = "Työkokemus alalta (vuosina)"
TYOPAIKKA_COL = "Työpaikka"
VUOSILASKUTUS_ALV0_COL = "Vuosilaskutus (ALV 0%, euroina)"
VUOSITULOT_COL = "Vuositulot"
ID_COL = "Vastaustunniste"

COMMISSION_COL = "Provisio (kk, brutto)"
LOMARAHA_COL = "Lomaraha (EUR)"
BONUS_COL = "Bonus (EUR)"
EQUITY_COL = "Osakkeet/optiot (EUR)"
SENIORITY_COL = "Seniority"

COLUMN_MAP_2025 = {
    "Timestamp": "Timestamp",
    "Employee or entrepreneur": PALKANSAAJA_VAI_LASKUTTAJA_COL,
    "Switched from employment to entrepreneurship, or vice versa, in 2025?": SIIRTYNYT_COL,
    "Age": IKA_COL,
    "Gender": SUKUPUOLI_COL,
    "Finnish fluency": "Suomen kielen taito",
    "Work language": "Työkieli",
    "Relevant work experience from the industry (in years)": TYOKOKEMUS_COL,
    "Years at current employer": "Vuosia nykyisellä työnantajalla",
    "Companies worked for": "Työpaikkojen lukumäärä",
    "Company size": "Yrityksen koko",
    "Education": "Koulutustaustasi",
    "Field of Study": "Opintoala",
    "Change in pay rate from last year (%)": "Tulojen muutos viime vuodesta (%)",
    "Years as entrepreneur": "Montako vuotta olet tehnyt laskuttavaa työtä alalla?",
    "What services do you offer?": PALVELUT_COL,
    "Hourly rate (VAT 0%, in euros)": TUNTILASKUTUS_ALV0_COL,
    "Yearly billing (VAT 0%, in euros)": VUOSILASKUTUS_ALV0_COL,
    "Billable hours per week": "Laskutettavat tunnit viikossa",
    "Weeks not billing": "Viikot ilman laskutusta",
    "Billing methods": "Laskutustavat",
    "Contract length": "Sopimuksen pituus",
    "Do you use agencies or find your clients yourself?": "Hankitko asiakkaasi itse suoraan vai käytätkö välitysfirmojen palveluita?",
    "Where are your clients from?": MISTA_ASIAKKAAT_COL,
    "Company": TYOPAIKKA_COL,
    "City": KAUPUNKI_COL,
    "What kind of a company you work in?": MILLAISESSA_COL,
    "Working time (h/week)": TYOAIKA_COL,
    "Time in office (%)": LAHITYO_COL,
    "Role / title": ROOLI_COL,
    "Seniority level": SENIORITY_COL,
    "Formal Seniority": "Virallinen senioriteetti",
    "Base salary (gross, monthly EUR)": KKPALKKA_COL,
    "Commission (gross, monthly EUR)": COMMISSION_COL,
    "Lomaraha (Holiday bonus, in EUR)": LOMARAHA_COL,
    "Bonus (EUR)": BONUS_COL,
    "Equity (EUR)": EQUITY_COL,
    "Free description of your compensation model": "Vapaa kuvaus kokonaiskompensaatiomallista",
    "Competitive salary": KIKY_COL,
    "Bonus": "Bonukset (kuvaus)",
    "Non-fringe benefits": "Edut (ei luontoisedut)",
    "Yearly Tax-Free Benefits (EUR)": "Vuosittaiset verovapaat edut (EUR)",
    "Fringe benefits (luontoisedut)": "Luontoisedut",
    "Operating system": "Käyttöjärjestelmä",
    "Language": "Ohjelmointikieli",
    "Web Frameworks": "Web-kehykset",
    "Data Engineering & Machine Learning": "Data & ML",
    "DevOps & Cloud Platforms": "DevOps & pilvi",
    "Databases": "Tietokannat",
    "What was left unasked that you want to answer to?": "Vapaa sana",
    "Feedback of the survey": PALAUTE_COL,
}

VALUE_MAP_2025 = {
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
        "Asun Porissa, toimisto Helsingissä, sijainnilla ei vaikutusta palkkaan": "Pori",
        "Capital region (Helsinki, Espoo, Vantaa)": "PK-seutu",
        "Firmalla ei ole toimistoa": "Etätyöfirma",
        "Hajautettu": "Etätyöfirma",
        "New York City": "New York",
        "New York, NY, USA": "New York",
        "PK-Seutu (Helsinki, Espoo, Vantaa)": "PK-seutu",
        "Tampere (etänä Berliiniin)": "Tampere",
        "Turku/remote (HQ Austin, TX)": "Turku",
        "Ulkomailla": "Ulkomaat",
        "Remote": "Etätyö",
        "remote": "Etätyö",
        "Fully remote": "Etätyö",
        "Fully remote work": "Etätyö",
        "100% remote, no main office": "Etätyö",
        "Completely distributed and remote": "Etätyö",
        "Remote without HQ": "Etätyö",
        "Remote (US)": "Ulkomaat",
        "Outside Finland": "Ulkomaat",
        "Abroad": "Ulkomaat",
        "No centrla office, multiple locations with employees": "Etätyö",
    },
    MILLAISESSA_COL: {
        "Product company with softaware as their core business": "Tuotetalossa, jonka core-bisnes on softa",
        "Product company with software as their core business": "Tuotetalossa, jonka core-bisnes on softa",
        "A company where software is a support role (for example banks or healthcare)": "Yritys, jossa softa tukirooli",
        "Consulting": "Konsultointi",
        "Public or third sector": "Julkinen/kolmas sektori",
    },
    SUKUPUOLI_COL: {
        "Male": "mies",
        "Female": "nainen",
        "Non-binary": "muu",
        "Prefer not to say": None,
    },
    KIKY_COL: {
        "Above market": "Yli markkinatason",
        "Average market": "Markkinataso",
        "Below market": "Alle markkinatason",
        "Not sure": "En osaa sanoa",
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
    "on",
    "yes",
}

OTHER_GENDER_VALUES = {
    "muu",
    "muunsukupuolinen",
}

FEMALE_GENDER_VALUES = (
    "f",
    "n",
    "women",
)

MALE_GENDER_VALUES = (
    "he / him / male",
    "ihminen. kikkelillä.",
    "m i ä s",
    "m",
    "mail",  # probably a typo
    "male presenting",
    "male",
    "man",
    "meis",
    "mie",  # probably mies?
    "miekkonen",
    "mies",
    "miesoletettu",
    "miäs",
    "ukko",
    "äiä",
)

IDS_TO_DROP_2025 = {
    "18121abbdb13303c",  # duplicate of d5ac88f64a922e6c (submitted 3 min later)
}
EXPECTED_ROW_COUNT_2025 = 683
