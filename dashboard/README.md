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

## the download bundle (encrypted)

the conclusion has a passphrase gate. the complete project — the five
notebooks, the cleaned dataset, the original raw export, the written report,
and the slide deck — is zipped and encrypted with the python `cryptography`
library (fernet, with a PBKDF2-HMAC-SHA256 key derived from a passphrase).
only the encrypted file `cameroon_food_prices_project.zip.enc` is committed;
the passphrase is never stored in the source. when a visitor types the
correct passphrase the app decrypts the bundle in memory and reveals the
download; a wrong passphrase raises `InvalidToken` and stays locked.

to regenerate the encrypted bundle after changing the notebooks, data, report
or deck, from inside `dashboard/`:

```python
from utils.data import write_encrypted_bundle
write_encrypted_bundle("YOUR-PASSPHRASE")   # rewrites the .enc file
```

(the project files themselves still live in the repo so the app can run and
rebuild the bundle; the encryption protects the packaged download.)

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
