"""data and model loading with caching. mirrors what's in the notebooks."""
import io
import os
import base64
import zipfile
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error

# csv lives one directory up from /dashboard
ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "wfp_food_prices_clean.csv"

# everything that goes into the downloadable project bundle
BUNDLE_FILES = [
    "01_data_exploration.ipynb",
    "02_classification.ipynb",
    "03_clustering.ipynb",
    "04_prediction.ipynb",
    "05_pattern_discovery.ipynb",
    "wfp_food_prices_clean.csv",
    "wfp_food_prices_cameroon.csv",
    "report 2.docx",
    "presentation 3.pptx",
]


@st.cache_data(show_spinner=False)
def build_bundle():
    """zip the notebooks, both datasets, the report and the deck into one
    archive, built in memory. used to produce the encrypted bundle below."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in BUNDLE_FILES:
            path = ROOT / name
            if path.exists():
                z.write(path, arcname=name)
    buf.seek(0)
    return buf.getvalue()


# ---- encryption -------------------------------------------------------------
# the downloadable bundle is shipped encrypted (cryptography / fernet). the
# passphrase is NEVER stored in the source: only the salt + ciphertext live in
# the committed .enc file, and the app decrypts on demand when the user types
# the right passphrase. a wrong passphrase raises InvalidToken.
ENC_PATH = ROOT / "cameroon_food_prices_project.zip.enc"
PBKDF2_ITERATIONS = 480_000
SALT_BYTES = 16


def _derive_key(password: str, salt: bytes) -> bytes:
    """turn a human passphrase into a 32-byte fernet key via PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=PBKDF2_ITERATIONS)
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt_bytes(data: bytes, password: str) -> bytes:
    """encrypt with a fresh random salt; output is salt (16 bytes) + token."""
    salt = os.urandom(SALT_BYTES)
    token = Fernet(_derive_key(password, salt)).encrypt(data)
    return salt + token


def decrypt_bytes(blob: bytes, password: str) -> bytes:
    """reverse encrypt_bytes. raises cryptography.fernet.InvalidToken if the
    passphrase is wrong or the data was tampered with."""
    salt, token = blob[:SALT_BYTES], blob[SALT_BYTES:]
    return Fernet(_derive_key(password, salt)).decrypt(token)


@st.cache_data(show_spinner=False)
def load_encrypted_bundle():
    """read the committed encrypted bundle (salt + ciphertext) from disk."""
    return ENC_PATH.read_bytes() if ENC_PATH.exists() else None


def write_encrypted_bundle(password: str):
    """one-off: encrypt the current bundle with the given passphrase and write
    the .enc file. run this whenever the notebooks, data, report or deck change."""
    ENC_PATH.write_bytes(encrypt_bytes(build_bundle(), password))
    return ENC_PATH


@st.cache_data(show_spinner=False)
def load_prices():
    df = pd.read_csv(CSV)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


@st.cache_data(show_spinner=False)
def summary_stats(df):
    return {
        "rows":       len(df),
        "raw_rows":   74955,
        "regions":    df["admin1"].nunique(),
        "markets":    df["market"].nunique(),
        "commodities": df["commodity"].nunique(),
        "start":      df["date"].min().date(),
        "end":        df["date"].max().date(),
        "categories": df["category"].nunique(),
    }


# classification
@st.cache_resource(show_spinner=False)
def train_classifier(df):
    df = df.copy()
    thresh = df.groupby("commodity")["price"].quantile([0.33, 0.66]).unstack()
    thresh.columns = ["lo", "hi"]
    df = df.merge(thresh, on="commodity")
    df["cls"] = "Medium"
    df.loc[df["price"] <= df["lo"], "cls"] = "Low"
    df.loc[df["price"] > df["hi"], "cls"] = "High"

    for col in ["admin1", "commodity", "category", "market", "cls"]:
        df[col + "_e"] = LabelEncoder().fit_transform(df[col])

    df["commod_year_med"] = df.groupby(["commodity", "year"])["price"].transform("median")
    df["commod_recent_med"] = (
        df.groupby("commodity")["price"]
          .transform(lambda s: s.shift(1).rolling(50, min_periods=1).median())
          .fillna(df["price"].median())
    )

    rich = ["admin1_e", "commodity_e", "category_e", "year", "month",
            "latitude", "longitude", "market_e",
            "commod_year_med", "commod_recent_med"]
    X = df[rich]
    y = df["cls_e"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2,
                                          random_state=42, stratify=y)
    rf = RandomForestClassifier(n_estimators=200, max_depth=15,
                                random_state=42, n_jobs=-1)
    rf.fit(Xtr, ytr)
    yp = rf.predict(Xte)
    acc = accuracy_score(yte, yp)
    importances = pd.Series(rf.feature_importances_, index=rich).sort_values()
    return {
        "model": rf,
        "accuracy": acc,
        "y_test": yte,
        "y_pred": yp,
        "classes": ["High", "Low", "Medium"],
        "importances": importances,
        "labelled": df,
    }


# clustering
@st.cache_resource(show_spinner=False)
def fit_clusters(df, k=4):
    pivot = (df.pivot_table(index="market", columns="commodity",
                             values="price", aggfunc="median"))
    pivot = pivot.dropna(thresh=int(0.3 * len(pivot)), axis=1)
    pivot = pivot.fillna(pivot.median())
    X = StandardScaler().fit_transform(pivot)
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = km.fit_predict(X)
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X)
    pivot = pivot.copy()
    pivot["cluster"] = labels
    return {
        "pivot": pivot,
        "coords": coords,
        "ev": pca.explained_variance_ratio_,
        "X": X,
    }


# prediction
@st.cache_resource(show_spinner=False)
def train_forecaster(df):
    top10 = df["commodity"].value_counts().head(10).index.tolist()
    sub = df[df["commodity"].isin(top10)].copy()
    mo = sub.groupby(["commodity", "date"])["price"].mean().reset_index()
    mo = mo.sort_values(["commodity", "date"]).reset_index(drop=True)
    mo["logp"] = np.log(mo["price"])

    for lag in range(1, 7):
        mo[f"lag_{lag}"] = mo.groupby("commodity")["logp"].shift(lag)
    mo["rolling_3"]  = mo.groupby("commodity")["logp"].transform(
        lambda s: s.shift(1).rolling(3).mean())
    mo["rolling_12"] = mo.groupby("commodity")["logp"].transform(
        lambda s: s.shift(1).rolling(12).mean())
    mo["year"] = mo["date"].dt.year
    mo["month"] = mo["date"].dt.month
    mo["month_sin"] = np.sin(2 * np.pi * mo["month"] / 12)
    mo["month_cos"] = np.cos(2 * np.pi * mo["month"] / 12)
    mo["commod_e"] = LabelEncoder().fit_transform(mo["commodity"])
    mo = mo.dropna().reset_index(drop=True)

    feat = [f"lag_{i}" for i in range(1, 7)] + \
           ["rolling_3", "rolling_12", "month_sin", "month_cos", "commod_e"]

    mo = mo.sort_values("date").reset_index(drop=True)
    cutoff = mo["date"].quantile(0.8)
    train = mo[mo["date"] <= cutoff]
    test  = mo[mo["date"] >  cutoff]

    model = HistGradientBoostingRegressor(
        max_iter=500, max_depth=8, learning_rate=0.05, random_state=42)
    model.fit(train[feat], train["logp"])
    test = test.copy()
    test["pred"] = np.exp(model.predict(test[feat]))

    r2_all = r2_score(test["price"], test["pred"])
    mae_all = mean_absolute_error(test["price"], test["pred"])
    mape = np.mean(np.abs((test["price"] - test["pred"]) / test["price"])) * 100

    per = []
    for c in top10:
        cd = test[test["commodity"] == c]
        if len(cd) < 3:
            continue
        per.append({
            "commodity": c,
            "r2": r2_score(cd["price"], cd["pred"]),
            "mae": mean_absolute_error(cd["price"], cd["pred"]),
        })
    per = pd.DataFrame(per).sort_values("r2", ascending=False)

    return {
        "test": test,
        "train": train,
        "r2": r2_all,
        "mae": mae_all,
        "mape": mape,
        "per_commodity": per,
        "feat": feat,
        "top10": top10,
    }
