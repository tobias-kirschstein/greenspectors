from typing import List

import altair as alt
import hydralit_components as hc
import numpy as np
import pandas as pd
import streamlit as st
from altair import Scale

from greenspectors.env import COMPANY_NAMES, LABELED_COMPANY_SUSTAINABILITY_PATH, LABELED_KEYWORDS_PATH, KEYWORDS


def streamlit_theme():
    font = "sans-serif"
    primary_color = "#6aa84f"
    font_color = "#FAFAFA"
    grey_color = "#262730"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75

    config = {
        "config": {
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "gridColor": grey_color,
                "domainColor": font_color,
                "tickColor": "#fff",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": ["#6aa84f", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                "diverging": [
                    "#6aa84f",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#6aa84f",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#d9ead3",
                    "#6aa84f"
                ],
                "ordinal": [
                    "#6aa84f",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config


# =========================================================================
# Data Fetchers
# =========================================================================

COMPANY_TO_CSV = {
    'Bank of America': 'BAC',
    'Exxon Mobile': 'Exxon',
    'General Motors': 'GM',
    'Johnson Johnson': 'J&J',
    'JP Morgan': 'JPMorgan',
    'Mc Donalds': 'McD',
    'TD Bank': 'TDBank',
    'JetBlue': 'Jetblue'
}

CSV_TO_COMPANY = {
    'BAC': 'Bank of America',
    'Exxon': 'Exxon Mobile',
    'GM': 'General Motors',
    'J&J': 'Johnson Johnson',
    'JPMorgan': 'JP Morgan',
    'McD': 'Mc Donalds',
    'TDBank': 'TD Bank',
    'Jetblue': 'JetBlue'
}


def get_company_rankings(company_names: List[str] = COMPANY_NAMES) -> List[float]:
    company_ratings = get_company_sustainability_ratings()
    company_rankings = []

    for company_name in company_names:
        if company_name in company_ratings['Company name'].values:
            df_company_name = company_name
        else:
            df_company_name = COMPANY_TO_CSV[company_name]
        ranking = company_ratings.iloc[(company_ratings['Company name'].values == df_company_name).argmax()][
            'Final Rating']
        company_rankings.append(ranking / 5)

    return company_rankings


def get_company_perceptions(company_names: List[str] = COMPANY_NAMES) -> List[float]:
    perceptions = []
    for company_name in company_names:
        company_sustainability_tweets = get_company_sustainability_tweets(company_name)
        perceptions.append(
            (company_sustainability_tweets['Label'] * company_sustainability_tweets['weight']).sum() /
            company_sustainability_tweets['weight'].sum())
    return perceptions


@st.cache
def get_company_sustainability_ratings() -> pd.DataFrame:
    return pd.read_csv(f"rating/Numeric Rating - Sheet1.csv", skiprows=1)


@st.cache
def get_company_sustainability_tweets(company_name: str) -> pd.DataFrame:
    company_sustainability_tweets = pd.read_csv(
        f"{LABELED_COMPANY_SUSTAINABILITY_PATH}/labeled_{company_name}_Sustainability.csv")
    company_sustainability_tweets['Label'] /= 2
    company_sustainability_tweets['weight'] = 1 + company_sustainability_tweets['likes_count'] \
                                              + company_sustainability_tweets['likes_count'] \
                                              + company_sustainability_tweets['retweet_count']

    return company_sustainability_tweets


@st.cache
def get_keyword_tweets(keyword: str) -> pd.DataFrame:
    if keyword == 'net zero carbon':
        file_name = f"net zero carbon_labeled"
    else:
        file_name = f"labeled_{keyword}"
    keyword_tweets = pd.read_csv(f"{LABELED_KEYWORDS_PATH}/{file_name}.csv")

    keyword_tweets['Label'] /= 2
    keyword_tweets['weight'] = 1 + keyword_tweets['likes_count'] \
                               + keyword_tweets['likes_count'] \
                               + keyword_tweets['retweet_count']

    return keyword_tweets


@st.cache
def get_combined_tweets() -> pd.DataFrame:
    dataframes = []

    for company in COMPANY_NAMES:
        dataframes.append(get_company_sustainability_tweets(company))

    for keyword in KEYWORDS:
        dataframes.append(get_keyword_tweets(keyword))

    return pd.concat(dataframes)


@st.cache
def get_company_pca_clustering() -> pd.DataFrame:
    return pd.read_csv("rating/clustering_pca_results.csv")


# =========================================================================
# Pages
# =========================================================================

# -------------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------------

def build_dashboard_page():
    # Ranking of the companies
    st.header("Company Greenliness vs Public Perception")

    chosen_companies = st.multiselect(
        'Companies',
        COMPANY_NAMES,
        COMPANY_NAMES)

    company_rankings = get_company_rankings(company_names=chosen_companies)
    company_perceptions = get_company_perceptions(company_names=chosen_companies)

    company_rankings_and_perceptions_df = pd.DataFrame([
        {'Company': company, 'Ranking': ranking, 'Perception': perception, 'Discrepancy': ranking - perception}
        for company, ranking, perception in zip(chosen_companies, company_rankings, company_perceptions)
    ])
    company_rankings_and_perceptions_df.set_index('Company')
    st.subheader("Discrepancy of Greenliness / Public Perception")

    st.altair_chart(
        alt.Chart(company_rankings_and_perceptions_df).mark_circle(size=100).encode(
            x=alt.X('Ranking', scale=alt.Scale(domain=[-0.1, 1.1])),
            y=alt.Y('Perception', scale=alt.Scale(domain=[-0.1, 1.1])),
            color=alt.Color('Discrepancy', scale=alt.Scale(scheme='redyellowgreen')),
            tooltip=['Company', 'Ranking', 'Perception']
        ).interactive(), use_container_width=True)

    # bar charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Greenliness Ranking")
        st.altair_chart(
            alt.Chart(company_rankings_and_perceptions_df).mark_bar().encode(
                x=alt.X('Ranking', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('Ranking', legend=None, scale=alt.Scale(scheme='redyellowgreen')),
                y=alt.Y("Company", sort='-x')
            ).properties(height=700, width=300))

    with col2:
        st.subheader("Public Perception Ranking")
        st.altair_chart(
            alt.Chart(company_rankings_and_perceptions_df).mark_bar().encode(
                x=alt.X('Perception', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('Perception', legend=None, scale=alt.Scale(scheme='redyellowgreen')),
                y=alt.Y("Company", sort='-x')
            ).properties(height=700, width=300))

    # Company Clustering
    st.header("Company Clustering")
    company_pca_clustering = get_company_pca_clustering().copy()
    company_pca_clustering['Public Perception'] = ''
    company_pca_clustering['Ranking'] = ''
    company_pca_clustering['Selected'] = False
    for idx, row in company_pca_clustering.iterrows():
        company_name = row['Company name']
        if company_name in CSV_TO_COMPANY:
            company_name = CSV_TO_COMPANY[company_name]

        is_selected = company_name in chosen_companies
        company_pca_clustering.loc[idx, 'Selected'] = is_selected
        if is_selected:
            company_idx = chosen_companies.index(company_name)
            company_perception = company_perceptions[company_idx]
            company_ranking = company_rankings[company_idx]

            company_pca_clustering.loc[idx, 'Public Perception'] = company_perception
            company_pca_clustering.loc[idx, 'Ranking'] = company_ranking

    company_pca_clustering = company_pca_clustering[company_pca_clustering['Selected'] == True]

    st.altair_chart(
        alt.Chart(company_pca_clustering).mark_point().encode(
            x='0',
            y='1',
            color=alt.Color('Ranking', scale=alt.Scale(scheme='redyellowgreen')),
            shape=alt.Shape('kmeans:O', legend=None),
            tooltip=['Company name', 'Ranking']
        ),
        use_container_width=True
    )


# -------------------------------------------------------------------------
# Company Insights
# -------------------------------------------------------------------------


def build_company_insights_page():
    selected_company = st.selectbox(
        'Which company do you wish to analyze?',
        COMPANY_NAMES)

    company_sustainability_tweets = get_company_sustainability_tweets(selected_company)

    company_ranking = get_company_rankings([selected_company])[0]

    company_perception = (company_sustainability_tweets['Label'] * company_sustainability_tweets['weight']).sum() / \
                         company_sustainability_tweets['weight'].sum()

    st.header(f"Public Sustainability Opinion of {selected_company}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sustainability Ranking", company_ranking)

    with col2:
        st.metric("Public Perception", f"{company_perception: 0.2f}")

    company_sustainability_ratings = get_company_sustainability_ratings().copy(True)
    company_name_csv = selected_company
    if selected_company in COMPANY_TO_CSV:
        company_name_csv = COMPANY_TO_CSV[selected_company]

    company_sustainability_rating = company_sustainability_ratings.iloc[[
        (company_sustainability_ratings['Company name'] == company_name_csv).argmax()]]

    columns_to_drop = []
    for column in company_sustainability_rating.columns:
        value = company_sustainability_rating.iloc[0][column]
        if isinstance(value, np.float) and np.isnan(value) or isinstance(value, str):
            columns_to_drop.append(column)

    company_sustainability_rating = company_sustainability_rating.drop(columns=columns_to_drop)

    company_sustainability_rating = company_sustainability_rating.astype(int)

    def color_cells(s):
        if isinstance(s, int) or isinstance(s, float):
            if s <= 0:
                return 'color: red'
            elif s <= 1:
                return 'color: orange'
            elif s <= 2:
                return 'color: yellow'
            elif s <= 3:
                return 'color: white'
            elif s <= 4:
                return 'color: lightgreen'
            elif s >= 5:
                return 'color: darkgreen'
        else:
            return 'color: white'

    company_sustainability_rating = company_sustainability_rating.style.applymap(color_cells)
    st.table(company_sustainability_rating)

    st.header("Historical development of Public Perception")

    perception_by_time = company_sustainability_tweets[['Label']]
    perception_by_time['time'] = pd.to_datetime(company_sustainability_tweets['created_at'])

    st.altair_chart(
        alt.Chart(perception_by_time).transform_window(
            smoothed_label='mean(Label)'
        ).mark_line().encode(
            x='time:T',
            y=alt.Y('smoothed_label:Q', title='Public Perception', scale=Scale(domain=[0, 1])),
        ), use_container_width=True)

    company_sustainability_tweets = company_sustainability_tweets.sort_values('Label')
    top_negative_tweets = company_sustainability_tweets.iloc[:5]
    top_positive_tweets = company_sustainability_tweets.iloc[-5:]

    st.header("Top Positive Tweets")

    positive_tweets_container = st.container()
    for idx, tweet in top_positive_tweets.iterrows():
        positive_tweets_container.info(tweet['tweet'])

    st.header("Top Negative Tweets")

    negative_tweets_container = st.container()
    for idx, tweet in top_negative_tweets.iterrows():
        negative_tweets_container.info(tweet['tweet'])


# -------------------------------------------------------------------------
# Sustainability Topics
# -------------------------------------------------------------------------


def build_sustainability_topics_page():
    # Keywords and perceptions
    st.header("Public Perception of Sustainability Topics")

    public_perception_per_keyword = dict()
    for keyword in KEYWORDS:
        df = get_keyword_tweets(keyword)
        public_perception_per_keyword[keyword] = (df['Label'] * df['weight']).sum() / df['weight'].sum()

    keywords_and_perceptions = pd.DataFrame(
        [{'Topic': keyword, 'Public Perception': perception} for keyword, perception in
         public_perception_per_keyword.items()])
    keywords_and_perceptions.set_index('Topic')

    st.altair_chart(alt.Chart(keywords_and_perceptions).mark_bar().encode(
        x=alt.X('Topic', sort='y'),
        y=alt.Y('Public Perception', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('Public Perception', scale=alt.Scale(scheme='redyellowgreen', domain=[0, 1]))
    ).properties(
        height=400
    ), use_container_width=True)

    # Search own
    st.header("Search for Keywords")
    search_keyword = st.text_input("Keyword", "Sustainability")
    all_tweets = get_combined_tweets()
    filtered_tweets = all_tweets[all_tweets['tweet'].str.contains(search_keyword)]
    n_filtered_tweets = len(filtered_tweets)
    keyword_perception = (filtered_tweets['Label'] * filtered_tweets['weight']).sum() / filtered_tweets['weight'].sum()

    if n_filtered_tweets > 0:

        filtered_tweets = filtered_tweets.sort_values('Label')
        top_positive_tweets = filtered_tweets.iloc[-5:]
        top_negative_tweets = filtered_tweets.iloc[:5]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Matching Tweets", n_filtered_tweets)

        with col2:
            st.metric(f"Public Perception of '{search_keyword}'", f"{keyword_perception:0.2f}")

        st.header("Top Positive Tweets")

        positive_tweets_container = st.container()
        for idx, tweet in top_positive_tweets.iterrows():
            positive_tweets_container.info(tweet['tweet'])

        st.header("Top Negative Tweets")

        negative_tweets_container = st.container()
        for idx, tweet in top_negative_tweets.iterrows():
            negative_tweets_container.info(tweet['tweet'])

    else:
        st.info(f"No Tweets found for '{search_keyword}'")


# =========================================================================
# MAIN
# =========================================================================


if __name__ == '__main__':
    alt.themes.register("streamlit", streamlit_theme)
    alt.themes.enable("streamlit")

    # specify the primary menu definition
    menu_data = [
        {'icon': "fas fa-tachometer-alt", 'label': "Dashboard", 'id': 'dashboard'},
        {'icon': "fas fa-building", 'label': "Company Insights", 'id': 'company_insights'},
        {'icon': "fas fa-tree", 'label': "Sustainability Topics", 'id': 'sustainability_topics'},
    ]
    # we can override any part of the primary colors of the menu
    # over_theme = {'txc_inactive': '#FFFFFF','menu_background':'red','txc_active':'yellow','option_active':'blue'}
    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(menu_definition=menu_data, override_theme=over_theme)

    # get the id of the menu item clicked
    if menu_id.lower() == 'dashboard':
        build_dashboard_page()
    elif menu_id == 'company_insights':
        build_company_insights_page()
    elif menu_id == 'sustainability_topics':
        build_sustainability_topics_page()

    # try:
    #     df = get_UN_data()
    #     countries = st.multiselect(
    #         "Choose countries", list(df.index), ["China", "United States of America"]
    #     )
    #     if not countries:
    #         st.error("Please select at least one country.")
    #     else:
    #         data = df.loc[countries]
    #         data /= 1000000.0
    #         st.write("### Gross Agricultural Production ($B)", data.sort_index())
    #
    #         data = data.T.reset_index()
    #         data = pd.melt(data, id_vars=["index"]).rename(
    #             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #         )
    #         chart = (
    #             alt.Chart(data)
    #                 .mark_area(opacity=0.3)
    #                 .encode(
    #                 x="year:T",
    #                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #                 color="Region:N",
    #             )
    #         )
    #         st.altair_chart(chart, use_container_width=True)
    # except URLError as e:
    #     st.error(
    #         """
    #         **This demo requires internet access.**
    #
    #         Connection error: %s
    #     """
    #         % e.reason
    #     )
