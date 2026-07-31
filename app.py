import streamlit as st

# Application modules
# Each module handles a specific part of the OPAC system:
# - loader: imports and prepares the catalogue
# - search: builds the search engine and ranking system
# - catalogue: displays the complete catalogue
# - metadata: analyses catalogue quality
# - ui: manages filters and result interfaces

from modules.loader import load_books

from modules.search import (
    build_search_index,
    search_books
)

from modules.catalogue import show_catalogue

from modules.metadata import (
    generate_metadata_report,
    show_metadata
)

from modules.ui import (
    show_filters,
    show_results
)

# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

# Define Streamlit page properties.
# Wide layout is used because catalogue tables
# contain many bibliographic fields.

st.set_page_config(
    page_title="Library Catalogue",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# CATALOGUE LOADING
# ==================================================

@st.cache_data
def load_catalogue():
    """
    Load and prepare the complete catalogue.

    The function is cached by Streamlit:
    the Excel file is read only once and reused
    during the application session.

    Processing steps:
    1. Load Excel database.
    2. Normalize catalogue data.
    3. Create optimized search indexes.
    """

    df = load_books()

    df = build_search_index(df)

    return df


# Load catalogue dataset.
# All application pages use this dataframe.

df = load_catalogue()


# ==================================================
# APPLICATION NAVIGATION
# ==================================================

# Sidebar navigation between the main OPAC sections.

page = st.sidebar.radio(
    "Navigation",
    [
        "🔎 Search",
        "📖 Catalogue",
        "🗂 Metadata"
    ]
)


# ==================================================
# SEARCH PAGE
# ==================================================

if page == "🔎 Search":

    st.title(
        "Search Catalogue"
    )

    # User query:
    # searches titles, authors, ISBN and metadata fields
    # using the fuzzy ranking algorithm.

    query = st.text_input(
        "🔎 Search catalogue",
        placeholder="Title, author, ISBN, publisher..."
    )

    # Dynamic filters:
    # selected values reduce the dataframe before searching.

    filtered_df = show_filters(
        df
    )

    # Execute ranked OPAC search.

    results = search_books(
        filtered_df,
        query
    )

    # Display matching records
    # and open bibliographic popup when selected.

    show_results(
        results
    )


# ==================================================
# COMPLETE CATALOGUE PAGE
# ==================================================

elif page == "📖 Catalogue":

    st.title(
        "Complete Catalogue"
    )

    # Number of physical copies currently registered.

    st.caption(
        f"{len(df)} physical copies registered"
    )

    # Display complete dataframe
    # with export functionality.

    show_catalogue(
        df
    )


# ==================================================
# METADATA DASHBOARD PAGE
# ==================================================

elif page == "🗂 Metadata":

    st.title(
        "Catalogue Metadata"
    )

    # Generate quality analysis report
    # from the current catalogue structure.

    report = generate_metadata_report(
        df
    )

    # Display metadata dashboard.

    show_metadata(
        report
    )