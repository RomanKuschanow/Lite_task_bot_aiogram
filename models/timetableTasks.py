# import json
# from datetime import datetime
#
#
# class Timetable_Task():
#     def __init__(self, text: str, stat_time: datetime, end_time: datetime, is_all_day: bool = False):
#         self.text = text
#         self.start_time = stat_time
#         self.end_time = end_time
#         self.is_all_day = is_all_day
#
#     def to_str(self) -> str:
#         return json.dumps(dict(self))
#
#     def from_str(self, json_str: str) -> Timetable_Task:
#         json_dict = json.loads(json_str)
#         return Timetable_Task(json_dict[text], json_dict[start_time], json_dict[end_time], json_dict[is_all_day])
#
#     def __repr__(self) -> str:
#         return self.to_str()
