import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

def clean_company_name(x, ignore_words=[]):
    # Convert x to a pandas series
    x = pd.Series(np.atleast_1d(x))

    # Swap & for AND
    x = x.str.replace('[\&]', ' AND ')

    # Remove ' (avoids splitting words)
    x = x.str.replace('[\']', '')

    # Swap other punctuation with a space (keeps words separate)
    x = x.str.replace('[^\w\s]', ' ')

    # Build regex pattern to remove ignore_words
    pattern = r'\b(?:{})\b'.format('|'.join(ignore_words))

    # Remove ignore_words
    x = x.str.replace(pattern, '')

    # Remove multiple spaces and trim white space
    x = x.str.replace(' +', ' ').str.strip().str.upper()

    return x


def prepare_data(filename, ignore_words=[]):
    columns_to_load = [
        'CompanyName',
        'CompanyNumber',
    ]

    df = pd.read_csv(
        filename,
        usecols=columns_to_load,
        skipinitialspace=True,
    )

    ignore_words = ['LIMITED', 'LTD', 'PLC', 'LLP', 'GROUP', 'CO', 'COMPANY', 'UK']

    df['CompanyName_clean'] = clean_company_name(df['CompanyName'], ignore_words)

    return df


def build_model(df, n_neighbors):
    # Method to convert strings to a design matrix
    vectorizer = CountVectorizer(
        analyzer='char',
        lowercase=False,
        ngram_range=(3, 3),
    )

    # Vectorise the source data
    X_train = vectorizer.fit_transform(df['CompanyName_clean'])

    # Specify the model
    model = NearestNeighbors(
        n_neighbors=n_neighbors,
        metric='cosine',
    ).fit(X_train)

    return vectorizer, model


def match_companies_knn(test_companies, vectorizer, model, df, ignore_words=[]):
    df_test_companies = pd.DataFrame({'CompanyName': np.atleast_1d(test_companies)})

    df_test_companies['CompanyName_clean'] = clean_company_name(df_test_companies['CompanyName'], ignore_words)

    X_test = vectorizer.transform(df_test_companies['CompanyName_clean'])

    distances, indices = model.kneighbors(X_test)

    for i in range(model.get_params()['n_neighbors']):
        df_test_companies[f'match.{i}.Distance'] = [x[i] for x in distances]
        df_test_companies[f'match.{i}.CompanyName'] = [df['CompanyName'].iloc[x[i]] for x in indices]
        df_test_companies[f'match.{i}.CompanyNumber'] = [df['CompanyNumber'].iloc[x[i]] for x in indices]

    return df_test_companies