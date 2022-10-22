def get_data(model_object, model_class):
    data = {}
    for column in model_class.__table__.columns:
        try:
            data[column.name] = getattr(model_object, column.name)
        except:
            pass
    return data
