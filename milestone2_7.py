ABC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
       't', 'u', 'v', 'w', 'x', 'y', 'z', '@', '.', ' ']


def read_file(file_path):
    """Reads the text from a file
    :param file_path: the path of the file to read from
    :type file_path: string
    :return: The text that the file contains
    :rtype: string
    """
    input_file = open(file_path, "r")
    info_list = input_file.read()
    input_file.close()
    return info_list


def decrypt_text(encrypted_text, key):
    """Decrypt the encrypted text with the given key (by Vigenere encryption algorithm)
    :param encrypted_text: the encrypted text to decrypt
    :param key: the key for decryption
    :type encrypted_text: string
    :type key: string
    :return: The decrypted text
    :rtype: string
    """
    decoded_text = ""
    count_k = 0  # for the length of the key
    # finding the length of the key
    length_k = key
    while length_k > 0:
        count_k += 1
        length_k //= 10
    # finding the amount of chars that in the file
    lines = read_file(encrypted_text)
    length_c = len(lines)
    # the current part will be for the amount of groups
    amount_groups = length_c // count_k
    rest = length_c % count_k  # if there is rest we'll add to the number of groups 1 so chars wont be missed
    if rest > 0:
        amount_groups += 1
    # for the slicing(so we'll be able to divide for groups as needed) We will define:
    spliting_to_groups = count_k
    start_p = 0  # the start place of every slicing(will get bigger according to the key length)
    for i in range(amount_groups):  # for each group
        # here the function decrypt_group get in.
        decoded_text += decrypt_group(lines[start_p:spliting_to_groups], key)
        # for the slicing:
        spliting_to_groups += count_k
        start_p += count_k
    return decoded_text


def decrypt_group(group_text, key):
    """Decrypt the encrypted group with the given key (by Vigenere encryption algorithm)
    :param group_text: the encrypted group from the text to decrypt
    :param key: the key for decryption
    :type group_text: string
    :type key: string
    :return: The decrypted group text
    :rtype: string
    """
    decrypt_word = ""
    s_key = str(key)
    for i in range(len(group_text)):
        index_in_table =ABC.index(group_text[i])
        index_key = (s_key[i])
        index_decrypt_char_p = ((index_in_table - (int(index_key))) + len(ABC)) % len(ABC)
        decrypt_word += ABC[index_decrypt_char_p]
    return decrypt_word


def extract_mails_from_text(text):
    """Gets all the valid mails from the given text
    :param text: the text that should contain the mail addresses
    :type text: str
    :return: The mail addresses that we need to save
    :rtype: list of strings
    """
    list_mails = []
    count = 0  # for the length of the loop
    for i in text:
        if i.isspace():
            count += 1
    count += 1  # for the last email/string
    list_text = text.split()
    for i in range(len(list_text)):
        email = list_text[i]
        if email.find('@') != -1 and email.find('.') != -1:
            index_strudel = email.index('@')
            index_point = email.index('.')
            if is_mail(email):
                if email[index_strudel + 1:] == "gmail.com" or email[index_strudel + 1:] == "yahoo.com" or email[index_strudel + 1:] == "hotmail.com":
                    list_mails.append(email)
    return list_mails


def is_mail(text):
    """Checks if the given mail is valid
    :param text: the mail address to check
    :type text: str
    :return: True if the mail is valid, and False if not
    :rtype: bool
    """
    if text.find('@') != -1 and text.find('.') != -1: # check if the chars even exist in the list
        index_strudel = text.index('@')
        index_point = text.index('.')
    else:
        return False  # if the chars does not exist , its not an email either way so the other check not relevant
    return index_strudel != 0 and text.count('@') == 1 and index_point > index_strudel and not text.isspace()


def write_to_file(file_path, list_to_write):
    """Writes the given list to a file in the given path
    :param file_path: the path of the file to write to
    :param list_to_write: the list to write to the file
    :type file_path: string
    :type list_to_write: list of strings
    """
    file = open(file_path, "w")
    file.writelines("%s\n" % t for t in list_to_write)  # write to the file and get new line after every email
    file.close()


def amount_mails_from_supplier(list_mails, supplier):
    """ Count the amount of emails from the specific supplier
    :param list_mails: the list of the mails that we discovered
    :param supplier: the name of the supplier of the email
    :type list_mails: list of strings
    :type supplier: string
    :return: the amount of mails
    :rtype : int
    """
    count = 0
    for mail in list_mails:
        index_strudel = mail.index('@')  # after the @ char the name of the supplier will show up
        if mail[index_strudel+1:] == supplier:
            count += 1
    return count


def no_duplicates(file_path):
    """ Reread the file of the emails and remove duplicates
    :param file_path: the file of the emails we discovered
    :type file_path : string
    """
    content = open(file_path, "r").readlines()
    content_set = set(content)  # will delete the duplicates mails
    no_duplicates_content = open(file_path, "w")
    for line in content_set:
        no_duplicates_content.write(line)


def count_mails(file_path):
    """ Count the amount of emails in the file
    :param file_path: the file of the emails (built for the one that have no duplications)
    :type file_path : string
    :return: the amount of emails in the file
    :rtype: int
    """
    with open(file_path, "r") as fp:
        count = len(fp.readlines())
    return count


def main():
    # file_path_keys = r"C:/python_course/keys.txt"  # keys.txt
    keys = read_file(r"C:/python_course/keys.txt").split(',')
    print(keys)
    file_path = input("please enter file path you would like to open")
    while file_path != '-999':
        for i in keys:  # it will move every key in the list(keys) and take the mails that found
            text = decrypt_text(file_path, int(i))
            list_mails = extract_mails_from_text(text)
            #if list_mails is not None:
                #if len(list_mails) > 0:
            write_to_file(r"C:/python_course/emails.txt", list_mails)
            no_duplicates(r"C:/python_course/emails.txt")
        file_path = input("please enter file path you would like to open")
    print("the amount of mails that found: ", len(list_mails))
    amount = count_mails(r"C:/python_course/emails.txt")
    print("the amount of mails that found no duplicates: ", amount)
    print("""the amount of mails from "gmail.com" is:""", amount_mails_from_supplier(list_mails, "gmail.com"))
    print("""the amount of mails from "yahoo.com" is:""", amount_mails_from_supplier(list_mails, "yahoo.com"))
    print("""the amount of mails from "hotmail.com" is:""", amount_mails_from_supplier(list_mails, "hotmail.com"))


if __name__ == '__main__':
    main()
