# cameroon food prices, a scrollytelling data story

a single page, scroll driven narrative built on streamlit. dark cinematic
palette, fraunces and inter and jetbrains mono, css scroll-driven reveals,
big stat blocks, real code snippets from every notebook, and a one click
download of the whole project.

## the story

- hero
- prologue, the dataset and the missing south region
- 01 the data, four shapes (+ the cleaning code)
- 02 classification, the random forest journey from 63 to 77 percent (+ code)
- 03 clusters, k means rediscovers the country's crisis map (+ code)
- 04 forecasting, the move from 0.48 to 0.94 r squared (+ code)
- 05 patterns, 2008 and 2022 as system shocks (+ code)
- conclusion, four takeaways, then download the full project

every chart is computed live from `wfp_food_prices_clean.csv` in the parent
folder. the classifier and forecaster retrain on first load and then cache.
each chapter shows a short, faithful code snippet from the matching notebook,
so the page walks through all five notebooks, not just their results.

## the download bundle

the conclusion has a download button that zips, in memory, the complete
project: the five notebooks, the cleaned dataset, the original raw export,
and the written report. it is built at runtime (`utils/data.build_bundle`),
so nothing binary has to be committed and the download is always current.

to build the same archive by hand from the project root, in powershell:

```powershell
$files = @(
  '01_data_exploration.ipynb','02_classification.ipynb','03_clustering.ipynb',
  '04_prediction.ipynb','05_pattern_discovery.ipynb',
  'wfp_food_prices_clean.csv','wfp_food_prices_cameroon.csv','report 2.docx'
)
Compress-Archive -Path $files -DestinationPath 'cameroon_food_prices_project.zip' -Force
```

## how to run locally

from inside this folder:

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

opens at http://localhost:8501.

## how to deploy on streamlit community cloud

1. push the whole project folder (the parent of `dashboard/`, including the
   csv files and `report 2.docx`) to a public github repo. the data files and
   the report must be in the repo because the download button reads them at
   runtime.
2. go to share.streamlit.io and sign in with github.
3. click "new app", pick the repo and branch.
4. set the main file path to `dashboard/streamlit_app.py`.
5. deploy. streamlit installs `dashboard/requirements.txt` and reads the dark
   theme from `.streamlit/c onfig.toml` at the repo root.

the relative paths resolve from the repo root, so the charts and the download
bundle work without any change.

## design

- palette, dark cinematic: bg #0b0c0e, accent amber #f59e0b, brand green #1B4D3E
- type, fraunces serif for headings, inter for body, jetbrains mono for numbers and code
- motion, css scroll-driven reveals (`animation-timeline: view()`), a scroll
  progress bar, fade-up entrances, all js-free, respects prefers-reduced-motion
- charts, plotly with a custom dark template, centered with a fixed max width
  and responsive sizing so they never clip
