import pandas as pd
from rapidfuzz import fuzz

# ==================================================
# VALUE NORMALIZATION
# ==================================================

def flatten_value(value):
    """
    Convert catalogue values into searchable text.

    The loader converts multi-value Excel fields into lists.
    This function creates a single lowercase string suitable
    for fuzzy comparison.

    Examples:
        ["Italian", "English"]
        becomes:
        "italian english"
    """

    if value is None:
        return ""

    if isinstance(value, list):

        return " ".join(
            str(item)
            for item in value
        ).lower()

    return str(value).lower()


# ==================================================
# ISBN NORMALIZATION
# ==================================================

def normalize_isbn(value):
    """
    Normalize ISBN identifiers before comparison.

    ISBNs can appear with different formatting:
        978-88-214-5629-9
        9788821456299

    Removing separators allows the search engine
    to compare the actual identifier.
    """

    if value is None:
        return ""

    return (
        str(value)
        .replace("—", "") # Em Dashes (—)
        .replace("–", "") # En Dashes (–)
        .replace("-", "") # Hyphens (-)
        .replace(" ", "")
        .strip()
    )


# ==================================================
# SEARCH INDEX CREATION
# ==================================================

def build_search_index(df):
    """
    Create additional columns used by the search engine.

    _search_text:
        Complete textual representation of the record.
        It allows searching across all metadata fields.

    _isbn_clean:
        Normalized ISBN used for exact identifier matching.
    """

    df = df.copy()

    searchable_columns = list(df.columns)

    # Combine every catalogue field into a single
    # searchable text index.
    #
    # This provides a fallback when the query does not
    # directly match title or author.
    df["_search_text"] = (
        df[searchable_columns]
        .apply(
            lambda row:
            " ".join(
                flatten_value(value)
                for value in row
            ),
            axis=1
        )
    )

    # ISBN receives a dedicated index because it is
    # an exact bibliographic identifier.
    if "ISBN" in df.columns:

        df["_isbn_clean"] = (
            df["ISBN"]
            .apply(normalize_isbn)
        )

    else:

        df["_isbn_clean"] = ""

    return df


# ==================================================
# FIELD SCORE
# ==================================================

def calculate_field_score(query, value):
    """
    Calculate similarity between a query and one field.

    Two RapidFuzz methods are combined:

    partial_ratio:
        Useful for incomplete searches.
        Example:
            "tolst"
            matches:
            "lev tolstoy"

    token_set_ratio:
        Ignores word order.
        Example:
            "tolstoy lev"
            matches:
            "lev tolstoy"

    The highest score is returned.
    """

    text = flatten_value(value)

    if not text:
        return 0

    return max(
        fuzz.partial_ratio(
            query,
            text
        ),
        fuzz.token_set_ratio(
            query,
            text
        )
    )


# ==================================================
# OPAC FUZZY SEARCH
# ==================================================

def search_books(df, query, threshold=35):
    """
    Weighted fuzzy search engine.

    Each catalogue record receives a relevance score.

    Ranking weights:

    ISBN:
        Exact match = +150 points
        Partial match = +100 points

    Title:
        Similarity score x 1.8

        Title has the highest weight because it is
        the primary bibliographic access point.

    Author:
        Similarity score x 1.5

        Author is a strong secondary identifier.

    Publisher:
        Similarity score x 0.8

        Useful but less distinctive.

    General metadata:
        Similarity score x 0.5

        Searches all remaining catalogue fields.

    Results below the threshold are discarded.
    Returned records are sorted from highest
    relevance to lowest.
    """

    if not query:
        return df

    query = query.lower().strip()

    # Normalize query in case it contains an ISBN.
    query_isbn = normalize_isbn(query)

    results = []

    for index, row in df.iterrows():

        score = 0

        # ------------------------------------------
        # ISBN PRIORITY MATCH
        # ------------------------------------------
        #
        # ISBN is the strongest possible identifier.
        # A correct ISBN should always rank above
        # textual similarities.

        isbn_score = 0

        if query_isbn:

            stored_isbn = normalize_isbn(
                row.get(
                    "_isbn_clean",
                    ""
                )
            )

            if stored_isbn:

                if query_isbn == stored_isbn:
                    isbn_score = 150

                elif query_isbn in stored_isbn:
                    isbn_score = 100

        score += isbn_score


        # ------------------------------------------
        # TITLE MATCH
        # ------------------------------------------
        #
        # Titles receive the highest textual weight
        # because users usually search by title.

        title_score = calculate_field_score(
            query,
            row.get(
                "Owned Copy Title",
                ""
            )
        )

        score += title_score * 1.8


        # ------------------------------------------
        # AUTHOR MATCH
        # ------------------------------------------
        #
        # Authors are highly relevant in library
        # catalogues, but less unique than ISBNs.

        author_score = calculate_field_score(
            query,
            row.get(
                "Author",
                ""
            )
        )

        score += author_score * 1.5


        # ------------------------------------------
        # PUBLISHER MATCH
        # ------------------------------------------

        publisher_score = calculate_field_score(
            query,
            row.get(
                "Publisher",
                ""
            )
        )

        score += publisher_score * 0.8


        # ------------------------------------------
        # GLOBAL METADATA MATCH
        # ------------------------------------------
        #
        # Searches the complete record as a fallback.
        # This catches queries involving:
        # - translators
        # - series
        # - keywords
        # - notes
        # - other metadata.

        general_score = fuzz.partial_ratio(
            query,
            row.get(
                "_search_text",
                ""
            )
        )

        score += general_score * 0.5


        # Keep only meaningful matches.
        if score >= threshold:

            results.append(
                {
                    "index": index,
                    "score": score
                }
            )


    # Highest relevance first.
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    indexes = [
        item["index"]
        for item in results
    ]


    output = df.loc[indexes].copy()


    # Store the final score in the dataframe.
    # Useful for debugging and future UI features
    # such as displaying match confidence.

    score_map = {
        item["index"]:
        round(
            item["score"],
            2
        )
        for item in results
    }

    output["_match_score"] = (
        output.index
        .map(score_map)
    )

    return output.reset_index(
        drop=True
    )