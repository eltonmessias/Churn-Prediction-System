from abc import ABC, abstractmethod
import pandas as pd



class DataInspectionStrategy(ABC):
    @abstractmethod
    def inspect(self, df: pd.DataFrame):
        pass

class DataTypesInspectionsStrategy(DataInspectionStrategy):
    def inspect(self, df: pd.DataFrame):
        print("\nData type and Non-null Counts")
        print(df.info())


class SummaryStatisticsInspectionStrategy(DataTypesInspectionsStrategy):
    def inspect(self, df: pd.DataFrame):
        print("\n Summary Statistics (Numerical Features):")
        print(df.describe())
        
        print("\n Summary Statistics (Categorical Features):")
        print(df.describe(include=["0"]))


class DataInspector:
    def __init__(self, strategy: DataInspectionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: DataInspectionStrategy):
        self.strategy = strategy

    def execute_inspection(self, df: pd.DataFrame):
        self.strategy.inspect(df)