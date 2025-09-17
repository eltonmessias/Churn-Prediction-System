from abc import ABC, abstractmethod
from unittest.mock import numerics

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.pylabtools import figsize
from matplotlib.pyplot import subplots, figure


class DataQualityAnalysisTemplate(ABC):
    def analyze(self, df: pd.DataFrame):
        self.identify(df)
        self.visualize(df)

    @abstractmethod
    def identify(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def visualize(self, df: pd.DataFrame):
        pass

# ==== Missing Values ====
class MissingValuesAnalysis(DataQualityAnalysisTemplate):
    def identify(self, df: pd.DataFrame):
        print("\nMissing Values Count by Columns:")
        missing_values = df.isnull().sum()
        print(missing_values[missing_values > 0])

    def visualize(self, df: pd.DataFrame):
        print("\nVisualizing Missing Values...")
        plt.figure(figsize=(12, 8))
        sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
        plt.title("Missing Values Heatmap")
        plt.show()

# ==== DUPLICATED VALUES ====
class DuplicatedValuesAnalysis(DataQualityAnalysisTemplate):
    def identify(self, df: pd.DataFrame):
        print("\nNumber of duplicated rows:", df.duplicated().sum())

    def visualize(self, df: pd.DataFrame):
        duplicated = df[df.duplicated()]
        if duplicated.empty:
            print("No duplicated rows to display.")
        else:
            print("\nSample duplicated rows:")
            print(duplicated.head())

# ==== OUTLIERS (USING BOXPLOT) ====
class OutliersAnalysis(DataQualityAnalysisTemplate):
    def identify(self, df: pd.DataFrame):
        print("\nChecking for potential outliers (IQR method)...")
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bond = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bond)]
            print(f"{col}: {len(outliers)} outliers")

    def visualize(self, df: pd.DataFrame):
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols].plot(kind="box", subplots=True, layout=(1, len(numeric_cols)), figsize=(15, 6))
        plt.suptitle("Boxplots for Outlier Detection")
        plt.show()


# if __name__ == "__main__":
#     import seaborn as sns
#     df = sns.load_dataset("titanic")
#
#     checks = [
#         MissingValuesAnalysis(),
#         DuplicateValuesAnalysis(),
#         OutlierAnalysis()
#     ]
#
#     for check in checks:
#         check.analyze(df)
