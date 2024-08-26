import codecs
from argparse import ArgumentParser


class Websites:
    def __init__(self, name, url, login_name, login, password, comment):
        self.website = name
        self.url = url
        self.login_name = login_name
        self.login = login
        self.password = password
        self.comment = comment

    def prepare_print(self, delimiter):
        output_list = []
        for key, value in self.__dict__.items():
            output_list.append(field_mapping.get(key, key) + delimiter + value)
        return ",".join(output_list) + "\n"


class Applications:
    def __init__(self, app, login_name, login, password, comment):
        self.app = app
        self.login_name = login_name
        self.login = login
        self.password = password
        self.comment = comment

    def prepare_print(self, delimiter):
        output_list = []
        for key, value in self.__dict__.items():
            output_list.append(field_mapping.get(key, key) + delimiter + value)
        return ",".join(output_list) + "\n"


class Note:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def prepare_print(self, delimiter):
        output_list = []
        for key, value in self.__dict__.items():
            output_list.append(field_mapping.get(key, key) + delimiter + value)
        return ",".join(output_list) + "\n"


def main():

    argsParser = ArgumentParser(description='Kaspersky Password Manager converter to CSV')
    argsParser.add_argument('-i', '--input_file', help='Kaspersky Password Manager export file')
    argsParser.add_argument('-o', '--output_file', default='converted_passwords.csv', type=str, help='Custom CSV file name')

    args = argsParser.parse_args()

    file = args.input_file
    documento = args.output_file

    if file is None:
        argsParser.print_help()
        exit(1)

    delimiter = "---"
    websiteslist = []
    applicationslist = []
    noteslist = []
    fd = codecs.open(file, 'r', "utf-8")
    buf = fd.readline()

    # Field mapping for Bitdefender
    field_mapping = {
        "Website name": "name",
        "Website URL": "url",
        "Login name": "username",
        "Login": "username",  # Combine Login and Login name
        "Password": "password",
        "Comment": "notes"
    }

    # Start by reading Websites attributes until Applications section
    while buf != "Applications\n":
        website_data = {}
        website_data["website"] = buf[14:-1]  # Extract website name
        website_data["url"] = fd.readline()[13:-1]  # Extract website URL
        website_data["username"] = fd.readline()[7:-1]  # Combine Login and Login name
        website_data["password"] = fd.readline()[10:-1]  # Extract password
        website_data["notes"] = fd.readline()[9:-1]  # Extract comment
        websiteslist.append(website_data)
        buf = fd.readline()  # Skip the separator line

    while buf != "Notes\n":
        application_data = {}
        application_data["app"] = buf[13:-1]
        application_data["username"] = fd.readline()[12:-1]
        application_data["password"] = fd.readline()[10:-1]
        application_data["notes"] = fd.readline()[9:-1]
        applicationslist.append(application_data)
        buf = fd.readline()

    while buf:
        note_data = {}
        note_data["name"] = buf[6:-1]
        note_data["text"] = fd.readline()[6:-1]
        noteslist.append(note_data)
        buf = fd.readline()

    # CSV output
    fd = codecs.open(documento, 'wb', 'utf-8')
    fd.write("name;url;username;password;notes\n")

    for aux in websiteslist:
        fd.write(aux.prepare_print(delimiter) + '\n')

    for aux in applicationslist:
        fd.write(aux.prepare_print(delimiter) + '\n')

    for aux in noteslist:
        fd.write(aux.prepare_print(delimiter) + '\n')

    print("Conversion finished - %d converted accounts" % (len(websiteslist) + len(applicationslist) + len(noteslist)))


if __name__ == '__main__':
    main()
