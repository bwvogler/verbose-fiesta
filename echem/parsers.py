from boxy import new_parser, Parsers

Parsers.list()  # ['echem']

parser = new_parser(Parsers.BiotekTimecourseXlsx)
parsed_data = parser.parse("uv/data/example.xlsx")
