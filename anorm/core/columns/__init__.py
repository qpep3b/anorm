from abc import ABC, abstractmethod
from anorm.core.expceptions import DataTypeException
from typing import Any


class BaseColumn(ABC):
    def __init__(
        self,
        primary_key: bool = False,
        db_index: bool = False,
        default_value: Any = None,
        nullable: bool = True,
    ):
        if not (nullable and default_value is None):
            raise Exception
        if primary_key:
            db_index = True

        self.primary_key = primary_key
        self.db_index = db_index
        self.nullable = nullable
        self.default_value = default_value

    @abstractmethod
    def cast_python_value(self, value):
        """
        Try to cast value to column type
        """
        pass

    @abstractmethod
    def sql_type(self):
        """
        SQL type for CREATE TABLE
        """
        pass

    @abstractmethod
    def to_db(self):
        """
        Function which prepares field as sql
        """
        pass

    @abstractmethod
    def to_python(self, value):
        """
        Represent db value as python value
        """
        pass


class Varchar(BaseColumn):
    def __init__(
        self, max_length: int, *args, **kwargs
    ):  # This breaks other params intellisense
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def sql_type(self) -> str:
        return "VARCHAR"

    def cast_python_value(self, value) -> str:
        return str(value)

    def to_db(self):
        pass

    def to_python(self, value) -> str:
        return str(value)


class Integer(BaseColumn):
    def sql_type(self) -> str:
        return "INTEGER"

    def cast_python_value(self, value) -> int:
        try:
            return int(value)
        except ValueError:
            raise DataTypeException(f"Value {value} is not integer")

    def to_db(self):
        pass

    def to_python(self, value) -> int:
        return int(value)


class Boolean(BaseColumn):
    def sql_type(self) -> str:
        return "BOOLEAN"

    def cast_python_value(self, value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return bool(value)
        if isinstance(value, str):
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False

        raise DataTypeException(f"Value {value} cannot be presented like boolean")

    def to_db(self):
        pass

    def to_python(self, value) -> bool:
        return bool(value)


class Serial(Integer):
    def __init__(self, *args, **kwargs):
        kwargs["primary_key"] = True
        kwargs["db_index"] = True

        super().__init__(*args, **kwargs)

    def sql_type(self) -> str:
        return "SERIAL"

    def cast_python_value(self, value) -> int:
        if value is None:
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, str) and value.isdigit():
            return int(value)

        raise DataTypeException(
            f"Only integer value can be used as serial ({value} is not integer)"
        )
