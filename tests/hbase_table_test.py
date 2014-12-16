#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `hbase_table` module.
"""
import pytest

from HBaseBoard.hbase_table import HBaseTable
from HBaseBoard.hbase_wrapper import HBaseWrapper
import happybase as hb


class TestHBaseTableClass(object):
    def setup(self):
        self.hbase_con = hb.Connection()
        self.hb_wrapper = HBaseWrapper()
        self.hb_wrapper.delete_all_tables()
        self.hb_wrapper.create_default_table("test_table")

    def teardown(self):
        self.hb_wrapper.delete_all_tables()
        self.hb_wrapper.close_connection()
        self.hbase_con.close()

    def test_raises_error_if_no_table_exists(self):
        with pytest.raises(ValueError):
            HBaseTable("ghost", self.hb_wrapper)

    def test_scan_returns_iterable_that_scans_a_table(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1", {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2", {"cf:first_name": "daffy", "cf:last_name": "duck"})
        my_table.put([test_val1, test_val2])
        table_scanner = my_table.scan()

        assert test_val1 == table_scanner.next()
        assert test_val2 == table_scanner.next()
