import src.idea1 as idn
import src.userinput as usn

db_name = usn.get_user_dbname()
min_sup = usn.get_user_supnum()
idn.idea1fun(db_name, min_sup)
