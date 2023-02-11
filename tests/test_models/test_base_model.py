#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the style and documentation of the base model class"""
    @classmethod
    def setUpClass(self):
        """Set up for docstring test"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8"""
        for path in ['models/base_model.py', 'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, 'base_model.py needs a docstring')
        self.assertTrue(len(module_doc) > 1, 'base_model.py needs a docstring')

    def test_class_docstring(self):
        """Test if the BaseModel class has docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the existence of docstring in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__, None, "{:s} method needs a docstring".format(func[0]))
                self.assertTrue(
                    len(func[1].__doc__) > 1, "{:s} method needs a docstring".format(func[0]))


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typs in attrs_types.items():
            with self.subTest(attr=attr, typs=typs):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typs)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """
        Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at value
        """
        tac = datetime.now()
        instal1 = BaseModel()
        tec = datetime.now()
        self.assertTrue(tac <= instal1.created_at <= tec)
        time.sleep(1e-4)
        tac = datetime.now()
        instal2 = BaseModel()
        tec = datetime.now()
        self.assertTrue(tac <= instal2.created_at <= tec)
        self.assertEqual(instal1.created_at, instal1.updated_at)
        self.assertEqual(instal2.created_at, instal2.updated_at)
        self.assertNotEqual(instal1.created_at, instal2.created_at)
        self.assertNotEqual(instal1.updated_at, instal2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        instal1 = BaseModel()
        instal2 = BaseModel()
        for inst in [instal1, instal2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(instal1.id, instal2.id)

    def test_to_dict(self):
        """Test conversion of objects attributes to dictionary for json"""
        t_model = BaseModel()
        t_model.name = "Holberton"
        t_model.my_number = 89
        d = t_model.to_dict()
        expected_attrs = ["id", "created_at",
                          "updated_at", "name", "my_number", "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_str(self):
        """Test that the str method has the correct output"""
        instal = BaseModel()
        string = "[BaseModel] ({}) {}".format(instal.id, instal.__dict__)
        self.assertEqual(string, str(instal))

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        l_format = "%Y-%m-%dT%H:%M:%S.%f"
        mb = BaseModel()
        new_c = mb.to_dict()
        self.assertEqual(new_c["__class__"], "BaseModel")
        self.assertEqual(type(new_c["created_at"]), str)
        self.assertEqual(type(new_c["updated_at"]), str)
        self.assertEqual(new_c["created_at"], mb.created_at.strftime(l_format))
        self.assertEqual(new_c["updated_at"], mb.updated_at.strftime(l_format))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls storage.save"""
        instal = BaseModel()
        old_created_at = instal.created_at
        old_updated_at = instal.updated_at
        instal.save()
        new_created_at = instal.created_at
        new_updated_at = instal.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
