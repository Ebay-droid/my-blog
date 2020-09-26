import os


class  Config:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ebay:qwerty@localhost/blog'
  UPLOADED_PHOTOS_DEST ='app/static/photos'
  QUOTES_API ='http://quotes.stormconsultancy.co.uk/random.json'
  
class  ProdConfig(Config):
  pass


class DevConfig(Config):
  DEBUG = True
  
class TestConfig(Config):
  pass

config_options = {
  'development':DevConfig,
  'production':ProdConfig,
  'test':TestConfig
}    