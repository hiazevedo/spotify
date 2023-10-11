import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu



st.set_page_config(
    page_title='Spotify Dashboards',
    page_icon=':bar_chart:',
    layout='wide'
)

with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=['Key Features', 'Dashboard']
    )

if selected == 'Key Features':
    st.write('ola')

elif selected == 'Dashboard':
    df = pd.read_csv("spotify-2023.csv", encoding = "ISO-8859-1")

    st.subheader('Dataframe contains')

    st.write(df)

    csv = df.to_csv(index = False).encode('utf-8')

    st.download_button("Download Dataframe", data = csv, file_name = "dataframe.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    df['in_deezer_playlists'] = pd.to_numeric(df['in_deezer_playlists'], errors='coerce')
    df['in_shazam_charts'] = pd.to_numeric(df['in_shazam_charts'], errors='coerce')

    sort_by_streams = df.sort_values(by="streams", ascending=False)

    top_20_songs = sort_by_streams.head(50)

    fig1 = px.bar(top_20_songs, x='track_name', y='streams',
                  title='Most Streamed Songs of 2023',
                  color='track_name',
                  color_continuous_scale = 'viridis',
                  hover_name = 'artist(s)_name'
                  )

    fig1.update_xaxes(categoryorder='total descending')
    fig1.update_xaxes(title_text='Track Name')
    fig1.update_yaxes(title_text='Total Streams')

    fig1.update_layout(width=1000, height=800)

    plt.tight_layout()

    st.write(fig1)

    artist_stats = df.groupby('artist(s)_name').agg({'track_name': 'count', 'streams': 'sum'}).reset_index()

    artist_stats.columns = ['Artist', 'Number of Songs', 'Total Streams']

    artist_stats['Avg Streams per Song'] = (artist_stats['Total Streams'] / artist_stats['Number of Songs']) / 1e9

    artist_stats = artist_stats.sort_values(by='Total Streams', ascending=False)

    top_20_artists = artist_stats.head(20)

    fig1 = px.bar(top_20_artists, x='Artist', y='Total Streams',
                  title='Most Streamed Artists of 2023',
                  color='Artist',
                  color_continuous_scale='viridis')

    fig1.update_xaxes(categoryorder='total descending')
    fig1.update_xaxes(title_text='Artist')
    fig1.update_yaxes(title_text='Total Streams')

    fig2 = px.bar(top_20_artists, x='Artist', y='Number of Songs',
                  title='Number of Songs per Artist (Top 20)',
                  color='Artist',
                  color_continuous_scale='viridis')

    fig2.update_xaxes(categoryorder='total descending')
    fig2.update_xaxes(title_text='Artist')
    fig2.update_yaxes(title_text='Number of Songs')

    fig3 = px.bar(top_20_artists, x='Artist', y='Avg Streams per Song',
                  title='Average Streams per Song (Top 20)',
                  color='Artist',
                  color_continuous_scale='viridis')

    fig3.update_xaxes(categoryorder='total descending')
    fig3.update_xaxes(title_text='Artist')
    fig3.update_yaxes(title_text='Average Streams per Song')

    st.write(fig1)
    st.write(fig2)
    st.write(fig3)

