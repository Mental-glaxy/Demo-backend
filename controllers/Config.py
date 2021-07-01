class Config:
  __conf = {
    "mongo_url":"mongodb+srv://VlAdmin:22w99i@cluster0-pcusn.mongodb.net/",
    "secret": "ABOBA"
  }


  @staticmethod
  def data(name):
    return Config.__conf[name]