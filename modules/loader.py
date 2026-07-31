import pandas as pd
from pathlib import Path
import numbers

# Central column mapping used across the application.
# Avoids hardcoding Excel column names in different modules.
from modules.config import COLUMNS

BASE_DIR = Path(__file__).resolve().parent.parent

# Main catalogue database file.
FILE_PATH = BASE_DIR / "data" / "book_catalogue.xlsx"


# ==================================================
# LOAD EXCEL CATALOGUE
# ==================================================

def load_books():
    """
    Load and prepare the bibliographic catalogue.

    Operations performed:
    - verify file existence
    - import Excel data
    - remove empty records
    - normalize column names
    - convert multi-value fields into lists
    - convert selected Excel dates
    - sort records according to library rules
    """

    if not FILE_PATH.exists():

        raise FileNotFoundError(
            "Catalogue file not found: data/book_catalogue.xlsx"
        )

    # Import catalogue sheet.
    df = pd.read_excel(
        FILE_PATH,
        sheet_name="data"
    )

    # Remove completely empty rows.
    df = df.dropna(
        how="all"
    )

    # Standardize column names.
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Convert Excel values into structured Python values.
    df = normalize_dataframe(
        df
    )

    # Apply OPAC-style sorting.
    df = sort_catalogue(
        df
    )

    return df


# ==================================================
# EXCEL DATE NORMALIZATION
# ==================================================

def normalize_excel_date(value):
    """
    Convert Excel numeric date serials into dd/mm/yyyy strings.

    Only numeric Excel serial values are converted.
    Text values remain unchanged.

    Example:
    46228 -> "29/07/2026"
    """

    if pd.isna(value):
        return None

    if isinstance(value, numbers.Number):

        # Avoid converting years like 1884, 1979, etc.
        # Excel dates are usually serials > 20000.
        if value > 20000:

            try:

                date = pd.to_datetime(
                    value,
                    unit="D",
                    origin="1899-12-30"
                )

                return date.strftime(
                    "%d/%m/%Y"
                )

            except Exception:

                return value

    return value


# ==================================================
# CELL NORMALIZATION
# ==================================================

def normalize_cell(value):
    """
    Normalize a single catalogue value.

    Rules:
    - empty cells become None
    - spaces are removed
    - semicolon-separated values become lists
    """

    if pd.isna(value):

        return None

    if isinstance(value, str):

        value = value.strip()

        if value == "":

            return None

        # Convert multi-value fields:
        # "Italian; English" -> ["Italian", "English"]
        if ";" in value:

            return [

                item.strip()

                for item in value.split(";")

                if item.strip()

            ]

        return value

    return value


# ==================================================
# DATAFRAME NORMALIZATION
# ==================================================

def normalize_dataframe(df):
    """
    Normalize the complete catalogue dataframe.

    Date conversion is applied only to:
    - loan_date
    - birth_date
    - death_date

    Numeric Excel serial dates are converted.
    All other columns are normalized normally.
    """

    date_columns = [

        COLUMNS["loan_date"],

        COLUMNS["birth_date"],

        COLUMNS["death_date"]

    ]

    for column in df.columns:

        if column in date_columns:

            df[column] = (
                df[column]
                .apply(normalize_excel_date)
            )

        else:

            df[column] = (
                df[column]
                .apply(normalize_cell)
            )

    return df


# ==================================================
# CATALOGUE SORTING
# ==================================================

def sort_catalogue(df):
    """
    Sort catalogue following library order.

    Priority:
    1. Author
    2. Volume
    3. Title
    """

    author_column = COLUMNS["author"]

    volume_column = COLUMNS["volume"]

    title_column = COLUMNS["owned_title"]

    # Temporary sorting fields.
    df["_sort_author"] = None

    df["_sort_volume"] = None

    df["_sort_title"] = None

    if author_column in df.columns:

        df["_sort_author"] = (

            df[author_column]

            .apply(

                lambda value:

                str(value[0])

                if isinstance(value, list)

                and len(value) > 0

                else str(value)

            )

            .str.lower()

        )

    if volume_column in df.columns:

        df["_sort_volume"] = (

            df[volume_column]

            .apply(

                lambda value:

                str(value[0])

                if isinstance(value, list)

                and len(value) > 0

                else str(value)

            )

            .str.lower()

        )

    if title_column in df.columns:

        df["_sort_title"] = (

            df[title_column]

            .apply(

                lambda value:

                str(value)

                if value is not None

                else ""

            )

            .str.lower()

        )

    df = df.sort_values(

        by=[

            "_sort_author",

            "_sort_volume",

            "_sort_title"

        ],

        ascending=True

    )

    # Remove internal sorting columns.
    df = df.drop(

        columns=[

            "_sort_author",

            "_sort_volume",

            "_sort_title"

        ]

    )

    return df.reset_index(
        drop=True
    )


# ==================================================
# DATA QUALITY REPORT
# ==================================================

def catalogue_quality_report(df):
    """
    Generate basic catalogue quality statistics.

    Returns:
    - total records
    - number of fields
    - missing values
    - duplicated copy identifiers
    """

    report = {

        "records":
            len(df),

        "fields":
            len(df.columns),

        "missing_values":
            df.isna()
            .sum()
            .sum()

    }

    copy_id_column = COLUMNS["copy_id"]

    if copy_id_column in df.columns:

        report["duplicate_copy_ids"] = (

            df[copy_id_column]

            .duplicated()

            .sum()

        )

    return report
