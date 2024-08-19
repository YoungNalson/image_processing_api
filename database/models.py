from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Boolean, String, Column, ForeignKey


Base = declarative_base()

class DryersModels(Base):
    __tablename__ = 'dryers_models'

    Id = Column('id', Integer, primary_key=True, autoincrement=True)
    Description = Column('description', String)


class GoogleCloudStorage(Base):
    __tablename__ = 'google_cloud_storage'

    Id = Column('id', Integer, primary_key=True, autoincrement=True)
    GoogleId = Column('google_id', String)


class Images(Base):
    __tablename__ = 'images'

    Id = Column('id', Integer, primary_key=True, autoincrement=True)
    DryerModelId = Column('dryer_model_id', ForeignKey('dryers_models.id'))
    CorrectlyAssembled = Column('correctly_assembled', Boolean)
    GoogleCloudStorageId = Column('google_cloud_storage_id', ForeignKey('google_cloud_storage.id'))


class ProcessedImages(Base):
    __tablename__ = 'processed_images'

    Id = Column('id', Integer, primary_key=True, autoincrement=True)
    DataBlob = Column('data_blob', String)
    ImageReferenceId = Column('image_reference_id', ForeignKey('images.id'))
    UsedInTraining = Column('used_in_training', Boolean)