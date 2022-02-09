import psycopg2

from config import host, user, password, db_name


class Bmsg:
    def select_db(self, whatis, fromis, whereis):
        db = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        cursor = db.cursor()
        cursor.execute("""SELECT {} FROM {} WHERE {} ORDER BY id ASC;""".format(whatis, fromis, whereis))
        return cursor.fetchall()

    def __init__(self, lenguage):
        pass
        alls_code = [
            "give_link",
            "about_me",
            "all_files",
            "not_files",
            "support",
            "send_discripion",
            "send_name_file",
            "name",
            "discription",
            "all_data_files",
            "no_changes",
            "sorry",
            "attention",
            "what",
            "i_agree",
            "disagree",
            "edit_description",
            "edit_name",
            "my_files",
            "reload",
            "delete",
            "support_msg",
            "i_can_not",
            "success"
        ]

        for i in alls_code:
            if lenguage == "ru":
                leng = "russian"
            elif lenguage == "be":
                leng = "belorussian"
            elif lenguage == "uk":
                leng = "ukrainian"
            else:
                leng = "english"

            data = self.select_db(whatis=leng, fromis="lenguage",
                                  whereis=f"code = '{i}'")  # (f'{leng}', "lenguage", f"code = '{i}'")
            globals()[i] = data[0][0].replace("\\n", "\n")

        self.give_link = give_link
        self.about_me = about_me
        self.all_files = all_files
        self.not_files = not_files
        self.support = support
        self.send_discripion = send_discripion
        self.send_name_file = send_name_file
        self.name = name
        self.discription = discription
        self.all_data_files = all_data_files
        self.no_changes = no_changes
        self.sorry = sorry
        self.attention = attention
        self.what = what
        self.i_agree = i_agree
        self.disagree = disagree
        self.edit_description = edit_description
        self.edit_name = edit_name
        self.my_files = my_files
        self.reload = reload
        self.delete = delete
        self.support_msg = support_msg
        self.i_can_not = i_can_not
        self.success = success
