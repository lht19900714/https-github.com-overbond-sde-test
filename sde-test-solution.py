#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys


class Solution:

    def __init__(self, input_file, output_file):
        # read input file and initial data storages
        with open(input_file, "r") as f:
            self.data = json.load(f)
        self.output_file = output_file
        self.corp_list = []
        self.gov_list = []


    def preparation(self):
        # Traversal input data and save only valid data in desired data storage
        # convert data type to support further calculations
        for each_objects in self.data["data"]:
            if "id" in each_objects and each_objects["id"][0] == "c" and self._verify(each_objects):
                each_objects['yield'] = float(each_objects['yield'][:-1])
                temp = each_objects['tenor'].split(' ')
                each_objects['tenor'] = float(temp[0])
                self.corp_list.append(each_objects)
            elif "id" in each_objects and each_objects["id"][0] == "g" and self._verify(each_objects):
                each_objects['yield'] = float(each_objects['yield'][:-1])
                temp = each_objects['tenor'].split(' ')
                each_objects['tenor'] = float(temp[0])
                self.gov_list.append(each_objects)


    def calculation(self, corp, gov_list):
        # find appropriate government bond object for corporation bond
        gov_benchmark = None
        res = {}
        for gov in gov_list:
            if gov_benchmark is None:
                gov_benchmark = gov
            elif abs(corp['tenor'] - gov['tenor']) < abs(corp['tenor'] - gov_benchmark['tenor']):
                gov_benchmark = gov
            elif abs(corp['tenor'] - gov['tenor']) == abs(corp['tenor'] - gov_benchmark['tenor']) \
                    and gov_benchmark['amount_outstanding'] < gov['amount_outstanding']:
                gov_benchmark = gov

        # calculate spread for corporation bond and construct result
        res["corporate_bond_id"] = corp['id']
        res["government_bond_id"] = gov_benchmark['id']
        res["spread_to_benchmark"] = str(int(abs(corp['yield'] * 100 - gov_benchmark['yield'] * 100))) + ' bps'

        return res

    def output(self):
        # generate output by leveraging calculation()
        # construct final results and create output file
        res = []
        temp_corp_list = self.corp_list
        for corp in temp_corp_list:
            res.append(self.calculation(corp, self.gov_list))
        final_res = {'data': res}

        with open(self.output_file, "w") as f:
            json.dump(final_res, f)

    def _verify(self, dict):
        # helper function for data validation purpose.
        for k, v in dict.items():
            if v is None:
                return False
        return True


def main(arg1, arg2):
    sde = Solution(arg1, arg2)
    sde.preparation()
    sde.output()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
