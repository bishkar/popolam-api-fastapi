from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, List

Model = TypeVar("Model")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")


class BaseCRUD(ABC, Generic[Model, CreateSchema, UpdateSchema]):
    @abstractmethod
    async def create(self, data: CreateSchema) -> Model: ...

    @abstractmethod
    async def retrieve(self, unique_id: int) -> Optional[Model]: ...

    @abstractmethod
    async def get(self) -> List[Model]: ...

    @abstractmethod
    async def update(self, unique_id: int, data: UpdateSchema) -> Model: ...

    @abstractmethod
    async def delete(self, unique_id: int) -> None: ...
