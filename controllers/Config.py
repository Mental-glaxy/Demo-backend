class Config:
  __conf = {
    "mongo_url":"mongodb://mongo:27017/",
    "secret": "ABOBA"
  }


  @staticmethod
  def data(name):
    return Config.__conf[name]