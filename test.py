from sqlalchemy import select

peter = Group.query.filter_by(Group.group_id == 99)#
print(peter.group_name)

#stmt = select(Group).where(Group.group_id == 99)
#result = session.execute(stmt)