# Project Number 8: The Ultimate Playmaker 

**Interactive Data Visualization Final Project**

## Links
* **Project Website:** https://hachu04.github.io/final_datavis/
* **Screencast Video:** 
* **Process Book:** Located in this repository as `Process Book_ Project Number 8.pdf`.

## Project Overview
This project is an interactive, data-driven "scouting report" designed to find the ultimate vertical playmaking midfielder from the 2022 Men's World Cup. Using a scrollytelling format, it walks the user through a mathematical filtering funnel, eliminating players round-by-round based on passing volume, safety, and progressive threat. The final act visualizes the "Tactical DNA" of the top 4 players using normalized Pass Sonars and vertical Pitch Maps.

## Repository Contents

**My Code:**
* `index.html`: The main web page containing all the HTML, CSS, D3.js visualization logic, and Scrollama narrative triggers.
* `*.py` files (`funnel.py`, `sonars.py`, `pitch_passes.py`, etc.): The Python data engineering scripts I wrote to fetch, calculate, and clean the raw JSON data from StatsBomb into the final CSVs.

**Data:**
* `final_midfield_funnel.csv`: The cleaned dataset used for Acts 1 and 2.
* `act3_final_sonars.csv`: The processed pass angle and distance data for the Final 4 players.
* `act3_pitch_passes.csv`: The start and end pitch coordinates for the Final 4 players' threat passes.

**External Libraries:**
* `D3.js (v7)`: Used for all data visualizations (Scatterplot, Bubble Chart, Pass Sonars, Pitch Maps, Bar Chart). Loaded via CDN.
* `Scrollama.js`: Used to handle the scroll-driven narrative triggers and scene transitions. Loaded via CDN.

## Interface Instructions & Non-Obvious Features
The website is designed as a Scrollytelling experience. Simply scroll down to progress through the story. 

However, there are several interactive features:
* **Team Highlight Dropdown:** In Acts 1 and 2, there is a dropdown menu in the top right corner. You can use this to select a specific country and highlight only their midfielders on the charts, dimming the rest.
* **Interactive Tooltips:** 
  * In Act 1, hovering over a dot reveals a checklist explaining exactly why a player passed or failed the round. 
  * In Act 3, hovering over the slices of the Pass Sonar reveals the exact volume percentage and average yardage for that specific direction.
  * In Act 3, hovering over the passes on the Vertical Pitch Map highlights the line and shows the exact vertical yards gained.
* **Act 4 Voting:** At the very end of the page, you must click one of the four player buttons to cast your vote. Doing so will disable the buttons and trigger an animated community consensus bar chart. For the purpose of this project and time contraints, this will be hard coded data, not real vote data.

## References
* **Data Source:** [StatsBomb Open Data](https://github.com/statsbomb/open-data) (2022 World Cup).
* **Visualization Library:** [D3.js](https://d3js.org/)
* **Scrollytelling Library:** [Scrollama](https://github.com/russellgoldenberg/scrollama)