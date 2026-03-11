from app.models.base_model import db


class Repository:
    """
    In-memory repository (kept temporarily for non-user entities
    until all models are fully migrated).
    """
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        class_name = obj.__class__.__name__
        if class_name not in self._storage:
            self._storage[class_name] = {}
        self._storage[class_name][obj.id] = obj

    def get(self, obj_id, class_name):
        return self._storage.get(class_name, {}).get(obj_id)

    def get_all(self, class_name):
        return list(self._storage.get(class_name, {}).values())

    def update(self, obj):
        class_name = obj.__class__.__name__
        if class_name in self._storage and obj.id in self._storage[class_name]:
            self._storage[class_name][obj.id] = obj

    def delete(self, obj_id, class_name):
        if class_name in self._storage and obj_id in self._storage[class_name]:
            del self._storage[class_name][obj_id]

    def find_by_attribute(self, class_name, attr_name, attr_value):
        for obj in self._storage.get(class_name, {}).values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None


class SQLAlchemyRepository:
    """Generic SQLAlchemy repository for one model."""
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True

    def find_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
