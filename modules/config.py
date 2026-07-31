# Mapping between internal Python keys and Excel catalogue columns.
# This avoids hardcoding column names throughout the application.
# If an Excel column changes, only this dictionary must be updated.

COLUMNS = {

    # Identification
    "copy_id": "Copy ID",
    "owned_title": "Owned Copy Title",

    # Work information
    "original_title": "Original First Edition Title",
    "genre": "Book Genre",
    "subgenre": "Book Subgenre",
    "keywords": "Keywords",
    "original_year": "Original First Edition Year",
    "original_language": "Original Language",

    # Author information
    "author": "Author",
    "birth_date": "Birth Date",
    "death_date": "Death Date",
    "author_nationality": "Author Nationality",
    "author_gender": "Author Gender",
    "nobel": "Nobel Prize",
    "pulitzer": "Pulitzer Prize",

    # Edition contributors
    "editor": "Editor / Curator",
    "additional_contributions": "Additional Contributions",
    "translator": "Translator",
    "illustrator": "Illustrator",

    # Edition information
    "owned_first_publication": "Owned Edition First Publication Year",
    "edition_year": "Edition Year",
    "edition_number": "Edition Number",
    "copy_language": "Copy Language",
    "publisher": "Publisher",
    "publication_city": "Publication City",

    # Collection information
    "series": "Series / Collection",
    "series_number": "Series Number",

    # Physical description
    "isbn": "ISBN",
    "pages": "Pages",
    "volume": "Volume",
    "binding": "Binding",
    "condition": "Physical Condition",

    # Economic information
    "cover_price": "Cover Price",
    "price_eur": "Price in EUR",
    "price_conversion_note": "EUR Conversion Note",

    # Personal information
    "signature": "Signature / Dedication",
    "location": "Location",
    "reading_status": "Reading Status",
    "notes": "Notes",

    # Loan management
    "borrowed_by": "Borrowed By",
    "loan_date": "Loan Date",
    "loan_history": "Loan History"
}


# Description of catalogue fields.
# Used for metadata reports, documentation and future OPAC features.

COLUMN_DESCRIPTIONS = {

    # Identification
    "copy_id":
        "Unique identifier assigned to the physical copy.",

    "owned_title":
        "Exact title written on the owned physical copy.",

    # Work information
    "original_title":
        "Original title of the work at first publication.",

    "genre":
        "Main literary or subject classification.",

    "subgenre":
        "More specific classification inside the main genre.",

    "keywords":
        "Keywords used for retrieval and thematic analysis.",

    "original_year":
        "Year of first publication of the work.",

    "original_language":
        "Language in which the work was originally written.",

    # Author information
    "author":
        "Author or authors responsible for the work.",

    "birth_date":
        "Birth date of the author.",

    "death_date":
        "Death date or current status of the author.",

    "author_nationality":
        "Nationality associated with the author.",

    "author_gender":
        "Gender information related to the author.",

    "nobel":
        "Nobel Prize information related to the author.",

    "pulitzer":
        "Pulitzer Prize information related to the author.",

    # Edition information
    "editor":
        "Person responsible for editing or supervising the edition.",

    "additional_contributions":
        "Additional contributions such as introductions, essays or comments.",

    "translator":
        "Translator responsible for the owned edition.",

    "illustrator":
        "Illustrator responsible for graphical elements.",

    "owned_first_publication":
        "First publication year of the owned edition.",

    "edition_year":
        "Year of the specific edition or reprint.",

    "edition_number":
        "Edition or reprint number.",

    "copy_language":
        "Language of the physical copy.",

    "publisher":
        "Publishing house responsible for the edition.",

    "publication_city":
        "City where the edition was published.",

    # Collection information
    "series":
        "Editorial series or collection.",

    "series_number":
        "Position of the volume inside the series.",

    # Physical description
    "isbn":
        "International identifier of the edition.",

    "pages":
        "Total number of pages.",

    "volume":
        "Volume number for multi-volume works.",

    "binding":
        "Physical binding type.",

    "condition":
        "Physical conservation state.",

    # Economic information
    "cover_price":
        "Original printed price of the book.",

    "price_eur":
        "Converted price expressed in euros.",

    "price_conversion_note":
        "Explanation of currency conversion.",

    # Personal information
    "signature":
        "Signatures, dedications or handwritten annotations.",

    "location":
        "Physical location inside the library.",

    "reading_status":
        "Personal reading status of the copy.",

    "notes":
        "Additional notes and observations.",

    # Loan management
    "borrowed_by":
        "Current borrower of the copy.",

    "loan_date":
        "Date when the current loan started.",

    "loan_history":
        "Historical list of previous loans."
}