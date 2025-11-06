<div align="left" style="position: relative;">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="right" width="30%" style="margin: -20px 0 0 20px;">
<h1>COVID19-DASHBOARD</h1>

<p align="left">
<img src="https://img.shields.io/github/license/Atharva0123/Covid19-dashboard?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/Atharva0123/Covid19-dashboard?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Atharva0123/Covid19-dashboard?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Atharva0123/Covid19-dashboard?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="left"><!-- default option, no dependency badges. -->
</p>
<p align="left">
<!-- default option, no dependency badges. -->
</p>
</div>
<br clear="right">

🔗 Table of Contents

📍 Overview

👾 Features

📁 Project Structure
  - 📂 Project Index

🚀 Getting Started
  - ☑️ Prerequisites
  - ⚙️ Installation
  - 🤖 Usage
  - 🧪 Testing

📌 Project Roadmap

🔰 Contributing

🎗 License

🙌 Acknowledgments

📍 Overview

This project is a Global COVID-19 Data Dashboard built using the Streamlit framework for rapid data visualization and analysis. This application provides a comprehensive, interactive, and visually striking dashboard for analyzing global COVID-19 data.

It is engineered with a separation of concerns strategy:

FDS_backend.py: Handles all data processing (loading, cleaning, calculating rates, filtering, and aggregation) using the Pandas and NumPy libraries.

FDS_app.py: Manages the user interface and visualization using Streamlit and Plotly for a dynamic, dark-themed experience.

👾 Features

Interactive Filtering: Users can filter the global data set by Country, Region, and Confirmed Case counts via an intuitive sidebar.

Key Performance Indicators (KPIs): Displays real-time totals for Confirmed Cases, Deaths, and Recovered based on the active filters.

Geographic Visualization: Features a Plotly Choropleth map to visualize the spread of confirmed cases worldwide.

Comparative Charts: Presents top 10 rankings for cases, deaths, and recoveries using interactive bar charts.

Predictive Analysis (Linear Regression): Includes a Linear Regression analysis (calculated manually using NumPy) that models the correlation between total Deaths and Confirmed Cases, complete with $R^2$ and RMSE metrics.

Visual Aesthetics: Utilizes custom CSS to implement a dramatic, dark mode theme with animated cinematic titles.

📁 Project Structure

└── Covid19-dashboard/
    ├── FDS_app.py
    ├── FDS_backend.py
    ├── README.md
    ├── country_wise_latest_covid.csv
    └── requirements.txt


📂 Project Index

<details open>
<summary><b><code>COVID19-DASHBOARD/</code></b></summary>
<details> <!-- root Submodule -->
<summary><b>root</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/Atharva0123/Covid19-dashboard/blob/master/FDS_backend.py'>FDS_backend.py</a></b></td>
<td><code>❯ Handles all data loading, cleaning, filtering, and aggregation logic.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Atharva0123/Covid19-dashboard/blob/master/requirements.txt'>requirements.txt</a></b></td>
<td><code>❯ Lists Python dependencies: Streamlit, Pandas, Plotly, NumPy, and scikit-learn.</code></td>
</tr>
<tr>
<td><b><a href='https://github.com/Atharva0123/Covid19-dashboard/blob/master/FDS_app.py'>FDS_app.py</a></b></td>
<td><code>❯ The main entry point. Defines the Streamlit UI, layout, and plots the visualizations.</code></td>
</tr>
<tr>
<td><b><a href='https://www.google.com/search?q=https://github.com/Atharva0123/Covid19-dashboard/blob/master/country_wise_latest_covid.csv'>country_wise_latest_covid.csv</a></b></td>
<td><code>❯ The primary dataset used by the application.</code></td>
</tr>
</table>
</blockquote>
</details>
</details>

🚀 Getting Started

☑️ Prerequisites

Before getting started with the COVID19-DASHBOARD, ensure your environment meets the following requirements:

Programming Language: Python 3.8+

Package Manager: Pip

⚙️ Installation

Install the dashboard using the following steps:

Clone the repository:

❯ git clone [https://github.com/Atharva0123/Covid19-dashboard](https://github.com/Atharva0123/Covid19-dashboard)


Navigate to the project directory:

❯ cd Covid19-dashboard


Install the project dependencies using the provided requirements.txt:

❯ pip install -r requirements.txt


🤖 Usage

Since this is a Streamlit application, run it using the streamlit run command, pointing to the main application file:

❯ streamlit run FDS_app.py


This command will open the dashboard automatically in your default web browser.

🧪 Testing

Run the test suite using the following command (assuming you have a test setup):

❯ pytest


📌 Project Roadmap

[X] Task 1: <strike>Implement feature one.</strike>

[ ] Task 2: Implement feature two.

[ ] Task 3: Implement feature three.

🔰 Contributing

💬 Join the Discussions: Share your insights, provide feedback, or ask questions.

🐛 Report Issues: Submit bugs found or log feature requests for the Covid19-dashboard project.

💡 Submit Pull Requests: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

Fork the Repository: Start by forking the project repository to your github account.

Clone Locally: Clone the forked repository to your local machine using a git client.
   sh    git clone [https://github.com/Atharva0123/Covid19-dashboard](https://github.com/Atharva0123/Covid19-dashboard)    

Create a New Branch: Always work on a new branch, giving it a descriptive name.
   sh    git checkout -b new-feature-x    

Make Your Changes: Develop and test your changes locally.

Commit Your Changes: Commit with a clear message describing your updates.
   sh    git commit -m 'Implemented new feature x.'    

Push to github: Push the changes to your forked repository.
   sh    git push origin new-feature-x    

Submit a Pull Request: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Review: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!

</details>

<details closed>
<summary>Contributor Graph</summary>





<p align="left">
   <a href="https://github.com{/Atharva0123/Covid19-dashboard/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Atharva0123/Covid19-dashboard">
   </a>
</p>
</details>

🎗 License

This project is protected under the SELECT-A-LICENSE License. For more details, refer to the LICENSE file.

🙌 Acknowledgments

The data source for this dashboard is based on publicly available WHO Global Reports.

Built with Streamlit and Plotly for dynamic data visualization.
