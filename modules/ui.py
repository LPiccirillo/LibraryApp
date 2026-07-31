import streamlit as st
import pandas as pd

from modules.config import COLUMNS

# ==================================================
# Helpers
# ==================================================

def flatten(value):

    """
    Convert list values into readable text.
    """

    if value is None:
        return ""

    if isinstance(value, list):

        return ", ".join(
            str(x)
            for x in value
        )

    return str(value)

def unique_values(df, column):

    """
    Extract unique values handling lists.

    Example:

    Italian
    English; Italian

    becomes:

    Italian
    English
    """

    values = set()

    if column not in df.columns:
        return []

    for value in df[column]:

        if isinstance(value, list):

            for item in value:
                values.add(str(item))

        elif value:

            values.add(str(value))

    return sorted(values)


# ==================================================
# Filters
# ==================================================

def show_filters(df):

    """
    OPAC dynamic filters.

    Features:
    - live update
    - incompatible values removed
    - record count per value
    - removes nan values
    - availability filter
    - hides impossible options
    """

    filtered = df.copy()

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def clean_value(value):

        if value is None:
            return False

        if isinstance(value, float) and pd.isna(value):
            return False

        if str(value).lower() == "nan":
            return False

        if str(value).strip() == "":
            return False

        return True

    def extract_selected(values):

        return [
            v.rsplit(
                " (",
                1
            )[0]
            for v in values
        ]

    def get_values_with_count(data, column):

        counts = {}

        if column not in data.columns:
            return []

        for value in data[column]:

            if isinstance(value, list):

                for item in value:

                    if clean_value(item):

                        item = str(item).strip()

                        counts[item] = (
                            counts.get(item, 0) + 1
                        )

            else:

                if clean_value(value):

                    value = str(value).strip()

                    counts[value] = (
                        counts.get(value, 0) + 1
                    )

        # elimina valori non disponibili
        counts = {
            key:value
            for key,value in counts.items()
            if value > 0
        }

        return [
            f"{key} ({value})"
            for key,value in sorted(
                counts.items()
            )
        ]

    def apply_list_filter(data, column, selected):

        if not selected:

            return data

        return data[
            data[column].apply(
                lambda x:

                any(
                    str(item) in selected
                    for item in x
                )
                if isinstance(x,list)

                else str(x) in selected
            )
        ]

    def apply_simple_filter(data, column, selected):

        if not selected:

            return data

        return data[
            data[column]
            .astype(str)
            .isin(selected)
        ]

    # --------------------------------------------------
    # Filters
    # --------------------------------------------------

    with st.expander(
        "⚙ Filters"
    ):

        col1,col2,col3,col4,col5,col6 = st.columns(6)

        # ==============================================
        # Original language
        # ==============================================

        with col1:

            options = get_values_with_count(
                filtered,
                COLUMNS["original_language"]
            )

            selected = st.multiselect(
                "Original language",
                options
            )

            filtered = apply_list_filter(
                filtered,
                COLUMNS["original_language"],
                extract_selected(selected)
            )

        # ==============================================
        # Copy language
        # ==============================================

        with col2:

            options = get_values_with_count(
                filtered,
                COLUMNS["copy_language"]
            )

            selected = st.multiselect(
                "Copy language",
                options
            )

            filtered = apply_list_filter(
                filtered,
                COLUMNS["copy_language"],
                extract_selected(selected)
            )

        # ==============================================
        # Author
        # ==============================================

        with col3:

            options = get_values_with_count(
                filtered,
                COLUMNS["author"]
            )

            selected = st.multiselect(
                "Author",
                options
            )

            filtered = apply_list_filter(
                filtered,
                COLUMNS["author"],
                extract_selected(selected)
            )

        # ==============================================
        # Publisher
        # ==============================================

        with col4:

            options = get_values_with_count(
                filtered,
                COLUMNS["publisher"]
            )

            selected = st.multiselect(
                "Publisher",
                options
            )

            filtered = apply_simple_filter(
                filtered,
                COLUMNS["publisher"],
                extract_selected(selected)
            )

        # ==============================================
        # Series
        # ==============================================

        with col5:

            options = get_values_with_count(
                filtered,
                COLUMNS["series"]
            )

            selected = st.multiselect(
                "Series",
                options
            )

            filtered = apply_list_filter(
                filtered,
                COLUMNS["series"],
                extract_selected(selected)
            )

        # ==============================================
        # Availability
        # ==============================================

        with col6:

            borrowed = (
                filtered[
                    COLUMNS["borrowed_by"]
                ]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            available_count = (
                borrowed == ""
            ).sum()

            loan_count = (
                borrowed != ""
            ).sum()

            options = []

            if available_count > 0:

                options.append(
                    f"Available ({available_count})"
                )

            if loan_count > 0:

                options.append(
                    f"On loan ({loan_count})"
                )

            selected = st.multiselect(
                "Availability",
                options
            )

            selected_clean = extract_selected(
                selected
            )

            if "Available" in selected_clean and "On loan" not in selected_clean:

                filtered = filtered[
                    filtered[
                        COLUMNS["borrowed_by"]
                    ]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    ==
                    ""
                ]

            elif "On loan" in selected_clean and "Available" not in selected_clean:

                filtered = filtered[
                    filtered[
                        COLUMNS["borrowed_by"]
                    ]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    !=
                    ""
                ]

    return filtered

# ==================================================
# Results
# ==================================================

def show_results(df):

    """
    Display search results.
    Opens popup only when a result button is clicked.
    """

    if df.empty:

        st.warning(
            "No books found."
        )

        return

    st.subheader(
        f"Results ({len(df)})"
    )

    # Local variable:
    # Only exists during this run.
    # No automatic pop-ups.

    selected_book = None

    for index, row in df.iterrows():

        title = flatten(
            row[COLUMNS["owned_title"]]
        )

        author = flatten(
            row[COLUMNS["author"]]
        )

        if st.button(
            f"📖 {title} — {author}",
            key=f"book_{index}"
        ):

            selected_book = index

    # Pop-up only if the button has been pressed
    if selected_book is not None:

        show_book_dialog(
            df.loc[selected_book]
        )


# ==================================================
# Book popup dialog
# ==================================================

@st.dialog(
    "Bibliographic record",
    width="large"
)
def show_book_dialog(book):

    """
    Display book record inside popup.
    """

    def clean_display(value):

        """
        Clean values before displaying them.

        Handles:
        - empty values
        - NaN values
        - datetime values
        - lists
        """

        if value is None:
            return ""

        if isinstance(value, float) and pd.isna(value):
            return ""

        # Dates are already formatted during import.
        # Keep them as dd/mm/yyyy strings.

        text = flatten(value).strip()

        if text.lower() == "nan":
            return ""

        if text == "":
            return ""

        return text

    def clean_isbn(value):

        """
        Remove ISBN separators.

        Example:
        978-88-17-08089-7
        becomes:
        9788817080897
        """

        if not value:
            return ""

        return (
            str(value)
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

    # ------------------------------------------
    # Main bibliographic data
    # ------------------------------------------

    title = clean_display(
        book[COLUMNS["owned_title"]]
    )

    author = clean_display(
        book[COLUMNS["author"]]
    )

    st.title(title)

    if author:

        st.subheader(
            author
        )

    # ------------------------------------------
    # Availability information
    # ------------------------------------------

    borrower = clean_display(
        book[COLUMNS["borrowed_by"]]
    )

    location = clean_display(
        book[COLUMNS["location"]]
    )

    loan_date = ""

    if "loan_date" in COLUMNS:

        loan_date = clean_display(
            book[COLUMNS["loan_date"]]
        )

    if not borrower:

        if location:

            st.success(
                f"Available | 📍 {location}"
            )

        else:

            st.success(
                "Available"
            )

    else:

        if loan_date:

            st.error(
                f"On loan to {borrower} (since {loan_date})"
            )

        else:

            st.error(
                f"On loan to {borrower}"
            )

    st.divider()

    # ------------------------------------------
    # Bibliographic information fields
    # ------------------------------------------

    info = {

        "ISBN":
            COLUMNS["isbn"],

        "Pages":
            COLUMNS["pages"],

        "Publisher":
            COLUMNS["publisher"],

        "Edition year":
            COLUMNS["edition_year"],

        "Edition number":
            COLUMNS["edition_number"],

        "Series":
            COLUMNS["series"],

        "Editor / Curator":
            COLUMNS["editor"],

        "Translator":
            COLUMNS["translator"],

        "Illustrator":
            COLUMNS["illustrator"],

        "Additional contributions":
            COLUMNS["additional_contributions"],

        "Original title":
            COLUMNS["original_title"],

        "Original publication year":
            COLUMNS["original_year"],

        "Cover price":
            COLUMNS["cover_price"]

    }

    for label, column in info.items():

        if column not in book.index:

            continue

        value = clean_display(
            book[column]
        )

        if value:

            # ------------------------------
            # Special ISBN formatting
            # ------------------------------

            if label == "ISBN":

                isbn_clean = clean_isbn(
                    value
                )

                if isbn_clean != value:

                    st.write(
                        f"**{label}:** {value} ({isbn_clean})"
                    )

                else:

                    st.write(
                        f"**{label}:** {value}"
                    )

            # ------------------------------
            # Cover price with EUR conversion
            # ------------------------------

            elif label == "Cover price":

                price_eur = ""

                if "price_eur" in COLUMNS:

                    price_eur = clean_display(
                        book[COLUMNS["price_eur"]]
                    )

                if price_eur:

                    st.write(
                        f"**{label}:** {value} (€ {price_eur})"
                    )

                else:

                    st.write(
                        f"**{label}:** {value}"
                    )

            # ------------------------------
            # Standard fields
            # ------------------------------

            else:

                st.write(
                    f"**{label}:** {value}"
                )

    st.divider()

    # ------------------------------------------
    # Close dialog button
    # ------------------------------------------

    if st.button(
        "Close"
    ):

        st.session_state[
            "open_book_dialog"
        ] = False

        st.session_state[
            "selected_book"
        ] = None

        st.rerun()
