# -*- coding: utf-8 -*-
import xlsxwriter


class Xlsx(object):
    def __init__(self, filename=None, sheet2headers=None, sheet2lines=None):
        """
        :param sheet2headers: excel头，与sheet名称对应; 如：
            {
                'Sheet1': [ 'h1', 'h2', 'h3' ]
            }
        :param sheet2lines: excel内容，与sheet名称对应; 如：
            {
                'Sheet1': [
                    [ 'l1', 'l2', 'l3' ]
                ]
            }
        """
        self._filename = filename
        self._sheet2headers = sheet2headers
        self._sheet2lines = sheet2lines

    def make(self):
        with xlsxwriter.Workbook(self._filename) as workbook:
            for sheet, headers in self._sheet2headers.items():
                start = 2
                lines = self._sheet2lines[sheet]
                worksheet = workbook.add_worksheet(name=sheet)
                self._write_and_style_headers(workbook, worksheet, headers)
                for row_no, l in enumerate(lines, start=start):
                    worksheet.write_row(row_no, 0, l)

    def _write_and_style_headers(self, workbook, worksheet, headers):
        start = 0
        for header in headers:
            worksheet.set_column(start, start, 10 * len(header))

            cell_range = "{start}1:{start}2".format(
                start=xlsxwriter.utility.xl_col_to_name(start)
            )
            start += 1

            header_format = self._header_format(workbook)
            worksheet.merge_range(cell_range, header, header_format)

    def _header_format(self, workbook):
        return workbook.add_format({"align": "center", "valign": "vcenter"})
