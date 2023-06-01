def read_file(file_path):
    """Reads the text from a file
    :param file_path: the path of the file to read from
    :type file_path: string
    :return: The text that the file contains
    :rtype: string
    """
    input_file = open(file_path, "r")
    info_list = input_file.read().splitlines()
    input_file.close()
    return info_list


def removing_spaces_from_list(info_list):  # work on the list itself
    """Remove irrelevant spaces from the list
    :param info_list: the list of the log file
    :type info_list: list of strings
    :return: list without spaces
    :rtype: list of strings
    """
    new_list = []
    for line in info_list:
        if line.strip():
            new_list.append(line.strip())
    return new_list


def removing_irrelevant_space_from_string(info_list):  # work on the strings that in the list
    """Remove irrelevant spaces from strings in the list
    :param info_list: the list of the log file after removing from her the irrelevant spaces
    :type info_list: list of strings
    :return: list without irrelevant spaces in the strings
    :rtype list of strings
    """
    new_list = []
    list_work_on = removing_spaces_from_list(info_list)
    for i in range(2, len(list_work_on)):
        new_list.append(" ".join(list_work_on[i].split()))
    return new_list


def extract_information(file_path):
    """Extract the relevant information(Image Name,Mem Usage) from the log file into list
    :param file_path: the path of the log file
    :type file_path: string
    :return: list of the relevant information
    :rtype list of strings
    """
    extract_info = []
    list_info = removing_irrelevant_space_from_string(read_file(file_path))
    for i in range(len(list_info)):
        first_index_of_space = list_info[i].index(' ')
        last_index_of_space = list_info[i].rindex(' ')
        extract_info.append([list_info[i][:first_index_of_space], list_info[i][last_index_of_space+1:]])
    return extract_info


def data_crossing(file_path, info_list):
    """Find suspicious processes in the list of the log file
    :param file_path: the path of the log file that contains information of the regular processes
    :type file_path: string
    :param info_list: the list we get in the function extract_information
    :type info_list: list of strings
    """
    standard_processes = read_file(file_path)
    suspicious_processes = []
    for i in range(len(standard_processes)):
        for j in range(len(info_list)):
            space_index = standard_processes[i].index(' ')
            process = standard_processes[i][:space_index]
            if process == info_list[j][0]:
                standard_mem = standard_processes[i][space_index+1:][:-1]  # without the K
                log_f_mem = info_list[j][1][:-1]
                if ',' in standard_mem:
                    standard_mem = standard_mem.replace(',', "")
                if ',' in log_f_mem:
                    log_f_mem = log_f_mem.replace(',', "")
                if int(log_f_mem) - int(standard_mem) > 50000:
                    suspicious_processes.append(info_list[j])
    print(suspicious_processes)


def main():
    info_list = read_file(r"C:/python_course/common_processes.txt")
    print(info_list)
    info_list_new = removing_irrelevant_space_from_string(read_file(r"C:/python_course/log_file.txt"))
    list_process_from_log = extract_information(r"C:/python_course/log_file.txt")
    print(list_process_from_log)
    print("the suspicion process are:")
    data_crossing(r"C:/python_course/common_processes.txt", list_process_from_log)


if __name__ == '__main__':
    main()
